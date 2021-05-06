# -*- coding: utf-8 -*-

import glob
import os


def create_output_dir(output_path):
    dirname = os.path.dirname(output_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def list_directory(input_path, extension=None):
    file_selector = '*' if extension is None else f'*.{extension}'

    selector_path = os.path.join(input_path, file_selector)

    for path in glob.glob(selector_path):
        yield path
