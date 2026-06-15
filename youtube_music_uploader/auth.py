#!/usr/bin/env python
# coding: utf8

# Usage youtube-music-auth [path_to_auth_file=~/oauth]
#
# NOTE: Despite the historical "oauth" naming, YouTube Music *uploads* require
# browser (cookie) authentication. OAuth credentials cannot upload to your
# library (YouTube Music exposes no public/OAuth upload API), so this command
# generates a browser auth file via ytmusicapi's browser setup.

import sys
import os
from ytmusicapi.setup import setup

DEFAULT_AUTH_FILE = os.environ['HOME'] + '/oauth'

INSTRUCTIONS = """\
Uploads to YouTube Music require browser (cookie) authentication.

To create your auth file you need to paste the request headers from a logged-in
browser session:

  1. In Firefox, open https://music.youtube.com (logged into the account that
     owns your library).
  2. Open DevTools (F12) -> Network tab, and type "/browse" in the filter box.
  3. Interact with the page so a POST request to "/browse" appears, click it.
  4. Right-click -> Copy Value -> Copy Request Headers.
  5. Paste below, press Enter, then Ctrl-D (EOF) to finish.
"""


def auth(auth_file: str = DEFAULT_AUTH_FILE) -> None:
    print(INSTRUCTIONS)
    if setup(auth_file):
        print("Logged successfully. Browser auth saved to %s" % auth_file)


def main():
    auth(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_AUTH_FILE)


if __name__ == "__main__":
    main()
