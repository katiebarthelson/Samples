# -*- coding: utf-8 -*-

import requests
import sys
import os
import tarfile
import logging
import json
from helpers import create_output_dir, list_directory

logger = logging.getLogger(__name__)


def list_tweets(input_path):
    for tweet_path in list_directory(input_path, 'json'):
        with open(tweet_path, 'r') as f:
            tweet = json.load(f)
            yield tweet


def extract_tar(path):
    logger.info(f"Extracting tar file {path}")

    target_path = os.path.dirname(path)

    tar = tarfile.open(path)
    tar.extractall(target_path)
    tar.close()

    logger.info(f"Done extracting tar file {path}")


def download_with_progress(url, out, user=None, password=None):
    logger.info(f"Downloading {url} as {out}")

    create_output_dir(out)

    auth = None
    if user is not None or password is not None:
        auth = (user, password)

    with open(out, 'wb') as f:
        response = requests.get(url, auth=auth, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
                sys.stdout.flush()
    sys.stdout.write("\n")
    sys.stdout.flush()

    if out.endswith('.tar'):
        extract_tar(out)

    logger.info(f"Done downloading {url} as {out}")
