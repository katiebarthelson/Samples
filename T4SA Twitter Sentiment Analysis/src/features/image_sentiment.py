# -*- coding: utf-8 -*-

import click
import os
import dotenv
import requests
import json
import logging
from PIL import Image
from helpers import create_output_dir, list_directory

logger = logging.getLogger(__name__)

_dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(_dotenv_path)

_image_sentiment_inference_service_url = os.getenv(
    'IMAGE_SENTIMENT_INFERENCE_SERVICE_URL',
    'http://127.0.0.1:5000')


def request_image_sentiment(image, extension):
    _content_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png'
    }
    return requests.post(_image_sentiment_inference_service_url,
                         data=image,
                         headers={
                             'Content-Type': _content_types[extension]
                         })


def get_tweet_id_from_image_path(image_path):
    return os.path.splitext(os.path.basename(image_path))[0]


def get_sentiment_output_path(output_path, tweet_id):
    return os.path.join(output_path, tweet_id + '.json')


def write_sentiment(output_path, sentiment):
    with open(output_path, 'w') as f:
        json.dump({ 'image_sentiment': sentiment }, f)


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def _main(input_path, output_path):
    create_output_dir(output_path)

    for image_path in list_directory(input_path):
        tweet_id = get_tweet_id_from_image_path(image_path)

        sentiment_output_path = get_sentiment_output_path(
            output_path, tweet_id)

        if os.path.exists(sentiment_output_path):
            continue

        logger.debug(f"Loading image {image_path}")
        with open(image_path, 'rb') as image_file:
            image = image_file.read()

        logger.debug(f"Requesting sentiment for {image_path}")
        extension = os.path.splitext(image_path)[1]
        response = request_image_sentiment(image, extension)
        if not response:
            logger.debug(f"Invalid sentiment for {image_path}")
            continue

        sentiment = json.loads(response.content)

        logger.debug(
            f"Writing sentiment {sentiment} to {sentiment_output_path}")
        write_sentiment(sentiment_output_path, sentiment)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    _main()
