# -*- coding: utf-8 -*-

import click
import dotenv
import os
import json
import pandas as pd
from functools import reduce
import logging
import multiprocessing
from flatten_dict import flatten
from helpers import create_output_dir, list_directory

logger = logging.getLogger(__name__)

_dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(_dotenv_path)


def get_input_dirs_lists(input_dirs):
    return [
        [
            os.path.basename(filename)
            for filename in list_directory(input_dir, 'json')
        ]
        for input_dir in input_dirs
    ]


def merge_input_dir_lists(input_dirs_lists):
    return reduce(lambda l, r: set(l).intersection(set(r)),
                  input_dirs_lists)


def generate_file_paths(input_dirs, merged_list):
    for filename in merged_list:
        yield [os.path.join(input_dir, filename)
               for input_dir in input_dirs]


def load_jsons(file_paths):
    jsons = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            jsons.append(json.load(f))
    return jsons


def merge_dicts(dicts):
    merged = {}
    try:
        for dict_ in dicts:
            merged.update(dict_)
    except Exception as e:
        return {}
    return merged


def load_and_merge_dicts(file_paths):
    jsons = load_jsons(file_paths)
    return merge_dicts(jsons)


def generate_merged_dicts(input_dirs, merged_list):
    all_file_paths = generate_file_paths(input_dirs, merged_list)
    cpu_count = multiprocessing.cpu_count()
    return multiprocessing.Pool(cpu_count).map(
        load_and_merge_dicts, all_file_paths)


def write_merged_dicts(output_path, merged_list, merged_dicts):
    for merged_dict, file_name in zip(merged_dicts, merged_list):
        if not merged_dict:
            logger.debug(f"{file_name} has no content, skipping")
            continue

        output_file = os.path.join(output_path, file_name)
        with open(output_file, 'w') as f:
            json.dump(merged_dict, f)


@click.command()
@click.argument('output_path', type=click.Path())
@click.argument('input_dirs', nargs=-1, type=click.Path(exists=True))
def _main(output_path, input_dirs):
    logger.info(f"Loading directories {input_dirs} and writing merge to {output_path}")

    create_output_dir(output_path)

    input_dirs_lists = get_input_dirs_lists(input_dirs)
    merged_list = merge_input_dir_lists(input_dirs_lists)

    logger.debug(f"Merging and writing {list(merged_list)[:10]}")

    merged_dicts = generate_merged_dicts(input_dirs, merged_list)
    filtered_dicts = filter(lambda dict_: not not dict_, merged_dicts)
    flattened_dicts = [flatten(dict_, reducer='dot')
                               for dict_ in filtered_dicts]

    df = pd.DataFrame.from_records(flattened_dicts)
    df.to_json(output_path)

    logger.info(f"Wrote merged files to {output_path}")


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_fmt)
    _main()
