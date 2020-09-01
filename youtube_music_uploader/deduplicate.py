#!/usr/bin/env python
# coding: utf-8

import glob
import argparse
from .uploader_daemon import DeduplicateApi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--deduplicate_api",
        '-w',
        required=True,
        help="Deduplicate API (should be HTTP and compatible with the manifest (see README)) (default: None)"
    )
    parser.add_argument(
        "--directory",
        '-d',
        default=None,
        help="Music Folder to deduplicate"
    )
    parser.add_argument(
        "--file",
        '-f',
        default=None,
        help="Music file path to deduplicate"
    )
    parser.add_argument(
        "--remove",
        '-r',
        action='store_true',
        help="Unmark specified file/folder (default: False)"
    )
    args = parser.parse_args()
    directory = args.directory
    file = args.file
    deduplicate_api = DeduplicateApi(args.deduplicate_api)
    if directory:
        files = [file for file in glob.glob(glob.escape(directory) + '/**/*', recursive=True)]
    elif file:
        files = [file]
    else:
        raise FileNotFoundError('Unable to load directory or file')
    for file_path in files:
        if args.remove:
            deduplicate_api.remove(file_path)
        else:
            deduplicate_api.save(file_path)


if __name__ == "__main__":
    main()
