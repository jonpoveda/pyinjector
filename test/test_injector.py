# -*- coding: utf-8 -*-
""" Unit test for injector module """
import unittest
from pathlib import Path
from shutil import copy
from shutil import rmtree

import toml

from injector import inject

TMP_DIR: Path = Path(__file__).absolute().parents[1].joinpath('test_tmp')
ASSETS_DIR: Path = Path(__file__).absolute().parent.joinpath('assets')


class TestInjector(unittest.TestCase):
    def setUp(self):
        TMP_DIR.mkdir(exist_ok=False, parents=False)

    def tearDown(self):
        rmtree(TMP_DIR)

    def test_injector_writes_expected_content_when_valid_files(self):
        # Copy some assets
        pipfile_path = TMP_DIR.joinpath('Pipfile.lock')
        pyproject_path = TMP_DIR.joinpath('pyproject.toml')
        pyproject_reference = ASSETS_DIR.joinpath('pyproject_mod.toml')

        copy(ASSETS_DIR.joinpath('Pipfile.lock'), pipfile_path)
        copy(ASSETS_DIR.joinpath('pyproject.toml'), pyproject_path)

        inject(pipfile_path, pyproject_path, safe=False)

        with pyproject_reference.open('r') as expected_file, \
                pyproject_path.open('r') as infile:
            expected = toml.load(expected_file)
            result = toml.load(infile)

        self.assertDictEqual(expected, result)
