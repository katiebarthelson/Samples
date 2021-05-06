# -*- coding: utf-8 -*-

import click
import dotenv
import pandas as pd
import numpy as np
from functools import reduce, partial, update_wrapper
import logging
from helpers import create_output_dir

logger = logging.getLogger(__name__)

_dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(_dotenv_path)

PERIODS = ['1s', '5s', '30s', '1min', '2min', '5min', '15min', '30min', '1H', '1BH', '1D']
PERIOD_DEFAULT = PERIODS[0]

IMAGE_SENTIMENT_NEG_COLUMN = 'image_sentiment.neg'
IMAGE_SENTIMENT_NEU_COLUMN = 'image_sentiment.neu'
IMAGE_SENTIMENT_POS_COLUMN = 'image_sentiment.pos'

IMAGE_SENTIMENT_OVERALL_COLUMN = 'image_sentiment.sentiment'
TEXT_SENTIMENT_OVERALL_COLUMN = 'text_sentiment.sentiment'

SELECTED_COLUMNS = [
    IMAGE_SENTIMENT_NEG_COLUMN,
    IMAGE_SENTIMENT_NEU_COLUMN,
    IMAGE_SENTIMENT_POS_COLUMN,
    TEXT_SENTIMENT_OVERALL_COLUMN
]

OVERALL_SENTIMENT_COLUMN = 'fused.sentiment'
OVERALL_CATEGORY_COLUMN = 'fused.cat'


def load_twitter_dataset(input_path):
    return pd.read_json(input_path) \
        .set_index('data.created_at') \
        .sort_index()


def select_columns(df, columns):
    return df[columns]


def normalize_columns(df):
    df = df.copy()
    for column in df.columns:
        series = df[column]
        df[column] = (series - series.min())/(series.max() - series.min())
    return df


def generate_overall_image_sentiment(df):
    df = df.copy()
    series = df[IMAGE_SENTIMENT_POS_COLUMN].copy()
    series[df[IMAGE_SENTIMENT_NEG_COLUMN] > series] = (
        -df[IMAGE_SENTIMENT_NEG_COLUMN])
    series *= (1.0 - df[IMAGE_SENTIMENT_NEU_COLUMN])
    df[IMAGE_SENTIMENT_OVERALL_COLUMN] = series
    return df


def generate_fused_sentiment(df):
    df = df.copy()
    df[OVERALL_SENTIMENT_COLUMN] = df[[
        IMAGE_SENTIMENT_OVERALL_COLUMN,
        TEXT_SENTIMENT_OVERALL_COLUMN
    ]].sum(axis=1)
    return df


def generate_overall_categories(df):
    df = df.copy()
    df[OVERALL_CATEGORY_COLUMN] = pd.qcut(
        df[OVERALL_SENTIMENT_COLUMN], q=3, labels=False)
    return df


def aggregate_overall_sentiment(df, period):
    return df.groupby([
        pd.Grouper(freq=period),
        OVERALL_CATEGORY_COLUMN
    ]).agg({
        OVERALL_CATEGORY_COLUMN: 'count',
        OVERALL_SENTIMENT_COLUMN: 'mean',
        IMAGE_SENTIMENT_OVERALL_COLUMN: 'mean',
        TEXT_SENTIMENT_OVERALL_COLUMN: 'mean',
        IMAGE_SENTIMENT_NEG_COLUMN: 'max',
        IMAGE_SENTIMENT_NEU_COLUMN: 'max',
        IMAGE_SENTIMENT_POS_COLUMN: 'max'
    }).rename(columns={
        OVERALL_CATEGORY_COLUMN: 'count'
    })


def drop_na(df):
    return df.dropna()


def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.option('-p', '--period', default=PERIOD_DEFAULT,
              type=click.Choice(PERIODS))
def _main(input_path, output_path, period):
    logger.info(f"Loading Twitter dataset {input_path} and writing to {output_path}")
    logger.info(f"Period: {period}")

    create_output_dir(output_path)

    df = load_twitter_dataset(input_path)

    pipeline = [
        wrapped_partial(select_columns, columns=SELECTED_COLUMNS),
        normalize_columns,
        generate_overall_image_sentiment,
        normalize_columns,
        generate_fused_sentiment,
        normalize_columns,
        generate_overall_categories,
        wrapped_partial(aggregate_overall_sentiment, period=period),
        drop_na
    ]

    for stage in pipeline:
        logger.debug(f"Running stage {stage.__name__}")
        df = stage(df)

    logger.debug(f"Dataframe sample:\n{df}")

    logger.info(f"Writing Twitter dataset to {output_path}")
    df.to_json(output_path)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    _main()
