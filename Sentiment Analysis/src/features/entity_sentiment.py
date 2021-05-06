# -*- coding: utf-8 -*-

import click
import os
import requests
import multiprocessing
import json
import logging
from helpers import create_output_dir, list_directory
from download.helpers import list_tweets
from google.cloud import language_v1
from os import listdir
from os.path import isfile, join, basename

logger = logging.getLogger(__name__)

def get_files_to_analyze(input_path, output_path):
    files_to_analyze = []

    output_path_files = {}
    filenames = [f for f in listdir(output_path) if isfile(join(output_path, f))]
    for file in filenames:
        output_path_files[file] = True

    filenames = [f for f in listdir(input_path) if isfile(join(input_path, f))]
    for file in filenames:
        if file not in output_path_files:
            full_path = join(input_path, file)
            files_to_analyze.append(full_path)

    return files_to_analyze

def request_entity_sentiment(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text,
        language='en',
        type_=language_v1.Document.Type.PLAIN_TEXT)
    try:
        response = client.analyze_entity_sentiment(document=document)
        all_entities = {'entity_sentiment':[]}
        temp = all_entities['entity_sentiment']
        for entity in response.entities:
            sentiment = entity.sentiment
            results = {
                'name':entity.name,
                'type': language_v1.Entity.Type(entity.type_).name,
                'salience': entity.salience,
                'wikipedia_url': entity.metadata.get('wikipedia_url', '-'),
                'mid': entity.metadata.get('mid', '-'),
                'sentiment':sentiment.score,
                'magnitude':sentiment.magnitude
            }
            temp.append(results)
        return all_entities
    except Exception as e:
        logger.exception(f"1 or more API Calls Failed: {str(e)}")

def analyze_tweet(args):
    try:
        input_file, output_path = args

        with open(input_file) as fp:
            tweet_data = json.load(fp)

        tweet_text = tweet_data['data']['text']
        tweet_id = tweet_data['data']['id']
        entity_sentiment = request_entity_sentiment(tweet_text)

        output_data = entity_sentiment
        output_file = join(output_path, basename(input_file))

        with open(output_file, 'w') as fp:
            json.dump(output_data, fp)

    except Exception as e:
        logger.error(f"Error analyzing tweet {tweet_id}: {str(e)}")

def analyze_tweets(tweet_files, output_path):
    logger.info(f"Processing {len(tweet_files)} Tweets in Parallel")
    input_file_output_path_pairs = []
    for input_file in tweet_files:
        input_file_output_path_pairs.append(
            (input_file, output_path)
        )

    cpu_count = multiprocessing.cpu_count()
    multiprocessing.Pool(cpu_count).map(
        analyze_tweet, input_file_output_path_pairs)


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def _main(input_path, output_path):
    create_output_dir(output_path)
    files_to_analyze = get_files_to_analyze(input_path, output_path)
    analyze_tweets(files_to_analyze, output_path)
    logger.info(f"Entity Sentiment Analysis complete")


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    _main()
