# -*- coding: utf-8 -*-
""" Unit test for injector module """
import sys
import unittest
from pathlib import Path
from shutil import copy
from shutil import rmtree
from unittest.mock import patch

import toml

from injector import main

TMP_DIR: Path = Path(__file__).absolute().parents[2].joinpath('test_tmp')
ASSETS_DIR: Path = Path(__file__).absolute().parents[1].joinpath('assets')


class TestInjector(unittest.TestCase):
    def setUp(self):
        TMP_DIR.mkdir(exist_ok=False, parents=False)

    def tearDown(self):
        rmtree(TMP_DIR)

    def test_injector_as_a_script_when_given_a_lock(self):
        # Copy some assets
        pipfile_path = TMP_DIR.joinpath('Pipfile.lock')
        pyproject_path = TMP_DIR.joinpath('pyproject.toml')
        pyproject_reference = ASSETS_DIR.joinpath('pyproject_from_lock.toml')

        copy(ASSETS_DIR.joinpath('Pipfile.lock'), pipfile_path)
        copy(ASSETS_DIR.joinpath('pyproject.toml'), pyproject_path)

        test_args = ['injector.py',
                     '-l',
                     pipfile_path.__str__(),
                     '-c',
                     pyproject_path.__str__()]

        with patch.object(sys, 'argv', test_args):
            main()

        with pyproject_reference.open('r') as expected_file, \
                pyproject_path.open('r') as infile:
            expected = toml.load(expected_file)
            result = toml.load(infile)

        self.assertDictEqual(expected, result)

    def test_injector_as_a_script_when_given_a_pipfile(self):
        # Copy some assets
        pipfile_path = TMP_DIR.joinpath('Pipfile')
        pyproject_path = TMP_DIR.joinpath('pyproject.toml')
        pyproject_reference = ASSETS_DIR.joinpath(
            'pyproject_from_pipfile.toml')

        copy(ASSETS_DIR.joinpath('Pipfile'), pipfile_path)
        copy(ASSETS_DIR.joinpath('pyproject.toml'), pyproject_path)

        test_args = ['injector.py',
                     '-p',
                     pipfile_path.__str__(),
                     '-c',
                     pyproject_path.__str__()]

        with patch.object(sys, 'argv', test_args):
            main()

        with pyproject_reference.open('r') as expected_file, \
                pyproject_path.open('r') as infile:
            expected = toml.load(expected_file)
            result = toml.load(infile)

        self.assertDictEqual(expected, result)
