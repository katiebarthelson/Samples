# -*- coding: utf-8 -*-

import click
import os
import dotenv
import requests
import json
import logging
from helpers import create_output_dir

logger = logging.getLogger(__name__)

_dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(_dotenv_path)

_twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')


def stream_tweets():
    params = {
        'expansions': 'attachments.media_keys',
        'media.fields': 'url,type',
        'tweet.fields': 'lang,created_at,geo',
        'user.fields': 'location'
    }
    headers = {'Authorization': f'Bearer {_twitter_bearer_token}'}
    r = requests.get('https://api.twitter.com/2/tweets/sample/stream',
                     params=params,
                     headers=headers,
                     stream=True)

    return r


def tweet_is_retweet(tweet):
    text = tweet['data']['text']
    return text.startswith('RT @')


def tweet_is_english(tweet):
    return tweet['data']['lang'] == 'en'


def tweet_has_photo(tweet):
    includes = 'includes' in tweet and tweet['includes']
    media = includes and tweet['includes']['media']
    return media and media[0]['type'] == 'photo'


def tweet_text_long_enough(tweet):
    return len(tweet['data']['text'].split()) >= 5


def tweet_qualifies_for_use(tweet):
    is_english = tweet_is_english(tweet)
    has_photo = tweet_has_photo(tweet)
    is_not_retweet = not tweet_is_retweet(tweet)
    text_long_enough = tweet_text_long_enough(tweet)
    return is_english and has_photo and is_not_retweet and text_long_enough


def save_tweet(tweet, output_path):
    tweet_id = tweet['data']['id']

    logger.debug(f"Saving tweet {tweet_id}")

    path = os.path.join(output_path, tweet_id + '.json')

    with open(path, 'w') as f:
        json.dump(tweet, f)


@click.command()
@click.argument('output_path', type=click.Path())
def _main(output_path):
    create_output_dir(output_path)

    with stream_tweets() as stream:
        for tweet_json in stream.iter_lines(decode_unicode=True):
            try:
                tweet = json.loads(tweet_json)
            except Exception as e:
                logger.error(f"Error parsing tweet {tweet_json}")

            if tweet_qualifies_for_use(tweet):
                save_tweet(tweet, output_path)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    _main()
