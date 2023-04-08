#!/usr/bin/env python
# coding: utf-8

import sys
import time
import logging
import logging.handlers
import os
import glob
import argparse
import requests
from .__init__ import __version__

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
from ytmusicapi import YTMusic


class DeduplicateApi:
    def __init__(self, uri: str) -> None:
        self.uri = uri

    def exists(self, file_path: str) -> bool:
        result = requests.request('GET', self.uri + "/", data={"path": file_path})
        return result.status_code == 200 or result.status_code == 204

    def save(self, file_path: str) -> None:
        requests.request('POST', self.uri + "/", data={"path": file_path})

    def remove(self, file_path: str) -> None:
        requests.request('DELETE', self.uri + "/", data={"path": file_path})


class MusicToUpload(FileSystemEventHandler):
    def on_created(self, event) -> None:
        global last_snapshot
        self.logger.info("Detected new files!")
        if os.path.isdir(self.path):
            curr_snapshot = DirectorySnapshot(self.path)
            files = [file for file in DirectorySnapshotDiff(last_snapshot, curr_snapshot).files_created]
            last_snapshot = curr_snapshot
            for file_path in files:
                upload_file(
                    api=self.api,
                    file_path=file_path,
                    logger=self.logger,
                    remove=self.remove,
                    deduplicate_api=self.deduplicate_api,
                )
        else:
            upload_file(
                api=self.api,
                file_path=event.src_path,
                logger=self.logger,
                remove=self.remove,
                deduplicate_api=self.deduplicate_api,
            )


def upload_file(
    api: YTMusic,
    file_path: str,
    logger: logging.Logger,
    remove: bool = False,
    deduplicate_api: DeduplicateApi = None,
) -> None:
    """
    Uploads a specific file by its path
    :param api: YTMusic. object to upload file though
    :param file_path: Path to MP3 file to upload
    :param logger: logging.Logger object for logs
    :param remove: Boolean. should remove file? False by default
    :param deduplicate_api: DeduplicateApi. Api for deduplicating uploads. None by default
    :raises Exception:
    :return:
    """
    retry = 5
    while retry > 0:
        try:
            if os.path.isfile(file_path):
                logger.info("Should upload %s? " % file_path)
                if deduplicate_api:
                    exists = deduplicate_api.exists(file_path)
                    logger.info("Deduplicate API: file exists? %s" % ("yes" if exists else "no"))
                    if exists:
                        return
                logger.info("Uploading %s" % file_path)
                status = api.upload_song(file_path)
                uploaded = 'STATUS_SUCCEEDED' in status
                if uploaded is False:
                    logger.info("Not uploaded %s: %s" % (file_path, status))
                    if ((status.status_code == 503) or (status.status_code == 408)): # Service unavailable or timeout; retry
                        retry -= 1
                        time.sleep(30)
                        continue
                    elif (status.status_code == 409) and deduplicate_api: # Already uploaded; deduplicate
                        logger.info("Deduplicate API: saving %s" % file_path)
                        deduplicate_api.save(file_path)
                if uploaded and deduplicate_api:
                    logger.info("Deduplicate API: saving %s" % file_path)
                    deduplicate_api.save(file_path)
                if remove and uploaded:
                    logger.info("Removing %s" % file_path)
                    os.remove(file_path)
            retry = 0
        except Exception as e:
            error_message = str(e)
            logger.info("Exception: Not uploaded %s: %s" % (file_path, error_message))
            if error_message.find("Supported file types are") != -1:
                retry = 0
                if deduplicate_api: # Save unsupported files so that we don't attempt upload again
                    logger.info("Deduplicate API: saving %s" % file_path)
                    deduplicate_api.save(file_path)
            elif error_message.find("401") != -1:
                retry -= 1
            elif error_message.find("502") != -1:
                retry -= 1
                time.sleep(30)
            else:
                raise e


def upload(
    directory: str = '.',
    oauth: str = os.environ['HOME'] + '/oauth',
    remove: bool = False,
    oneshot: bool = False,
    listener_only: bool = False,
    deduplicate_api: str = None,
    log: str = None,
) -> None:
    global last_snapshot

    handler = logging.handlers.WatchedFileHandler(log) if log else logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.info("Init Daemon - Press Ctrl+C to quit")

    api = YTMusic(oauth)
    if not api:
        raise ValueError("Error with credentials")
    observer = None
    deduplicate = DeduplicateApi(deduplicate_api) if deduplicate_api else None
    if not oneshot:
        if os.path.isdir(directory):
            last_snapshot = DirectorySnapshot(directory)
        event_handler = MusicToUpload()
        event_handler.api = api
        event_handler.oauth = oauth
        event_handler.path = directory
        event_handler.remove = remove
        event_handler.logger = logger
        event_handler.deduplicate_api = deduplicate
        observer = Observer()
        observer.schedule(event_handler, directory, recursive=True)
        observer.start()
    if not listener_only:
        files = [file for file in glob.glob(glob.escape(directory) + '/**/*', recursive=True)]
        for file_path in files:
            upload_file(api, file_path, logger, remove=remove, deduplicate_api=deduplicate)
    if oneshot:
        sys.exit(0)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--directory",
        '-d',
        default='.',
        help="Music Folder to upload from (default: .)"
    )
    parser.add_argument(
        "--oauth",
        '-a',
        default=os.environ['HOME'] + '/oauth',
        help="Path to oauth file (default: ~/oauth)"
    )
    parser.add_argument(
        "-r",
        "--remove",
        action='store_true',
        help="Remove the file on your hard drive if it was already successfully uploaded (default: False)"
    )
    parser.add_argument(
        "--oneshot",
        '-o',
        action='store_true',
        help="Upload folder and exit (default: False)"
    )
    parser.add_argument(
        "--listener_only",
        '-l',
        action='store_true',
        help="Only listen for new files, does not parse all files at launch (default: False)"
    )
    parser.add_argument(
        "--deduplicate_api",
        '-w',
        default=None,
        help="Deduplicate API (should be HTTP and compatible with the manifest (see README)) (default: None)"
    )
    parser.add_argument(
        "--log",
        '-e',
        default=None,
        help="Log to a specified file path (Default stderr)"
    )
    parser.add_argument(
        "--version",
        '-v',
        action='store_true',
        help="show version number and exit"
    )
    args = parser.parse_args()
    if args.version:
        print(__version__)
        return
    upload(
        directory=args.directory,
        oauth=args.oauth,
        remove=args.remove,
        oneshot=args.oneshot,
        listener_only=args.listener_only,
        deduplicate_api=args.deduplicate_api,
        log=args.log,
    )


if __name__ == "__main__":
    main()
