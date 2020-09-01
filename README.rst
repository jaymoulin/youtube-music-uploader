.. image:: https://raw.githubusercontent.com/jaymoulin/youtube-music-uploader/master/logo.png
    :alt: logo
    :target: http://github.com/jaymoulin/youtube-music-uploader


======================
Youtube Music Uploader
======================


.. image:: https://img.shields.io/github/release/jaymoulin/youtube-music-uploader.svg
    :alt: latest release
    :target: http://github.com/jaymoulin/youtube-music-uploader/releases
.. image:: https://img.shields.io/pypi/v/youtube-music-uploader.svg
    :alt: PyPI version
    :target: https://pypi.org/project/youtube-music-uploader/
.. image:: https://github.com/jaymoulin/jaymoulin.github.io/raw/master/ppl.png
    :alt: PayPal donation
    :target: https://www.paypal.me/jaymoulin
.. image:: https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png
    :alt: Buy me a coffee
    :target: https://www.buymeacoffee.com/3Yu8ajd7W
.. image:: https://badgen.net/badge/become/a%20patron/F96854
    :alt: Become a Patron
    :target: https://patreon.com/jaymoulin

(This product is available under a free and permissive license, but needs financial support to sustain its continued improvements. In addition to maintenance and stability there are many desirable features yet to be added.)

This program will create a Daemonic folder to upload your music library to Youtube Music

This work is based upon `Sigma67's Youtube Music API <https://github.com/sigma67/ytmusicapi>`_.

Installation
------------

This program needs `watchdog`, `ytmusicapi` and `requests` Python libraries to work.

.. code::

    apt-get install python3-pip build-essential
    pip3 install youtube-music-uploader

Once installed, You have to authenticate to Youtube Music via the `youtube-music-auth` command

.. code::

    # Usage youtube-music-auth [path_to_oauth_cred_file=~/oauth]


If first parameter is not defined, the script will try to store/load your oauth credentials through the `~/oauth` file.

Then follow the setup instructions provided https://ytmusicapi.readthedocs.io/en/latest/setup.html#copy-authentication-headers.

Usage
-----

Uploader
~~~~~~~~

This program will scan a given directory for new elements to upload them to Youtube Music.
First, launch the daemon to watch a directory new inputs.

.. code::

    usage: youtube-music-upload [-h] [-v] [--directory DIRECTORY] [--oauth OAUTH] [-r]
                              [-o] [--deduplicate_api DEDUPLICATE_API]

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show version number and exit
      --directory DIRECTORY, -d DIRECTORY
                            Music Folder to upload from (default: .)
      --oauth OAUTH, -a OAUTH
                            Path to oauth file (default: ~/oauth)
      -r, --remove          Remove the file on your hard drive if it was already successfully uploaded (default: False)
      -o, --oneshot         Upload folder and exit (default: False)
      -w DEDUPLICATE_API, --deduplicate_api DEDUPLICATE_API
                            Deduplicate API (should be HTTP and compatible with
                            the manifest (see README)) (default: None)

Deduplicate
~~~~~~~~~~~

This program will send all files or the specified file to the deduplication API

.. code::

    usage: youtube-music-upload-deduplicate [-h] --deduplicate_api DEDUPLICATE_API
                                       [--directory DIRECTORY] [--file FILE]
                                       [--remove]

    optional arguments:
      -h, --help            show this help message and exit
      --directory DIRECTORY, -d DIRECTORY
                            Music Folder to deduplicate
      --file FILE, -f FILE
                            Music file path to deduplicate
      -r, --remove          Unmark specified file/folder (default: False)
      -w DEDUPLICATE_API, --deduplicate_api DEDUPLICATE_API
                            Deduplicate API (should be HTTP and compatible with
                            the manifest (see README)) (default: None)

=================
Deduplication API
=================

Preface
-------

This API is completely optional. You don't have to implement this. It will only help you to avoid useless Google calls

You can use your own API implementation to avoid multiple Youtube Music uploads.
This API should match with the following requirements.

You may want to use this existing one : `Google MusicManager Deduplicate API <https://github.com/jaymoulin/google-musicmanager-dedup-api>`_.

Exists
------

+------+--------+--------------------------+----------------------------------------------------+
| path | method | parameter                | status code                                        |
+======+========+======+===================+===================+================================+
| /    | GET    | name | description       | value             | description                    |
|      |        +------+-------------------+-------------------+--------------------------------+
|      |        | path | path of your file | 200 or 204        | Your file was already uploaded |
|      |        |      |                   +-------------------+--------------------------------+
|      |        |      |                   | 404 (or whatever) | Your file was NOT uploaded     |
+------+--------+------+-------------------+-------------------+--------------------------------+

Saving
------

+------+--------+--------------------------+-------------------------------------------------+
| path | method | parameter                | status code                                     |
+======+========+======+===================+==========+======================================+
| /    | POST   | name | description       | value    | description                          |
|      |        +------+-------------------+----------+--------------------------------------+
|      |        | path | path of your file | whatever | Status code does not change anything |
+------+--------+------+-------------------+----------+--------------------------------------+

Removing
--------

+------+--------+--------------------------+-------------------------------------------------+
| path | method | parameter                | status code                                     |
+======+========+======+===================+==========+======================================+
| /    | DELETE | name | description       | value    | description                          |
|      |        +------+-------------------+----------+--------------------------------------+
|      |        | path | path of your file | whatever | Status code does not change anything |
+------+--------+------+-------------------+----------+--------------------------------------+

=====
About
=====

Requirements
------------

Youtube Music Uploader works with Python 3 or above.

Submitting bugs and feature requests
------------------------------------

Bugs and feature request are tracked on GitHub

Author
------

Jay MOULIN jay@femtopixel.com See also the list of contributors which participated in this program.

License
-------

Youtube Music Uploader is licensed under the MIT License
