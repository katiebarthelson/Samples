# -*- coding: utf-8 -*-

import click
import os
import dotenv
import json
import logging
import pandas as pd
import multiprocessing
import yfinance
from helpers import create_output_dir, list_directory

logger = logging.getLogger(__name__)

_dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(_dotenv_path)

_stocks_interval = os.getenv('STOCKS_INTERVAL', '1m')


def get_tweet_created_at(tweet_path):
    with open(tweet_path, 'r') as f:
        tweet = json.load(f)

    raw_created_at = tweet['data']['created_at']
    return pd.to_datetime(raw_created_at).tz_localize(None)


def get_tweets_timespan(input_path):
    tweet_paths = list_directory(input_path, 'json')

    cpu_count = multiprocessing.cpu_count()
    tweets_created_at = multiprocessing.Pool(cpu_count).map(
        get_tweet_created_at, tweet_paths)

    return (min(tweets_created_at), max(tweets_created_at))


def fetch_stock_history(ticker, start_at, end_at):
    return yfinance.download(
        ticker, start_at, end_at, interval=_stocks_interval)


def write_stock_history(output_folder, ticker, stocks_df):
    output_path = os.path.join(output_folder, f'stock_{ticker}.json')
    stocks_df.to_json(output_path)


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.argument('tickers', nargs=-1)
def _main(input_path, output_path, tickers):
    logger.info(f"Fetching stocks {tickers}")
    logger.info(f"Using time input range from {input_path}")

    create_output_dir(output_path)

    start_at, end_at = get_tweets_timespan(input_path)
    logger.debug(f"Stocks start time: {start_at}, end time: {end_at}")
    logger.debug(f"NOTE: This may be smaller than you expect due to weekends")

    stocks = [fetch_stock_history(ticker, start_at, end_at)
              for ticker in tickers]

    for ticker, stocks_df in zip(tickers, stocks):
        num_rows = len(stocks_df)
        logger.debug(f"Writing history for {ticker}: {num_rows} rows")
        write_stock_history(output_path, ticker, stocks_df)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    _main()
