# -*- coding: utf-8 -*-

import click
import os
import dotenv
import urllib.request
import json
import logging
import multiprocessing
from helpers import create_output_dir
from download.helpers import list_tweets

logger = logging.getLogger(__name__)

_dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(_dotenv_path)


def get_tweet_image_url(tweet):
    return tweet['includes']['media'][0]['url']


def get_tweet_image_path(tweet, output_path):
    tweet_id = tweet['data']['id']
    file_path = get_tweet_image_url(tweet)
    _, extension = os.path.splitext(file_path)
    return os.path.join(output_path, tweet_id + extension)


def download_tweet_image(args):
    url, output_path = args

    logger.debug(f"Downloading image {url}")
    try:
        urllib.request.urlretrieve(url, output_path)
    except Exception as e:
        logger.error(f"Error downloading image {url}: {e}")


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def _main(input_path, output_path):
    create_output_dir(output_path)

    tweet_image_paths_to_download = []

    for tweet in list_tweets(input_path):
        tweet_image_url = get_tweet_image_url(tweet)
        tweet_image_path = get_tweet_image_path(tweet, output_path)
        if not os.path.exists(tweet_image_path):
            tweet_image_paths_to_download.append(
                (tweet_image_url, tweet_image_path))

    cpu_count = multiprocessing.cpu_count()
    multiprocessing.Pool(cpu_count * 4).map(
        download_tweet_image, tweet_image_paths_to_download)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    _main()
