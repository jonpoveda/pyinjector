# -*- coding: utf-8 -*-
""" Unit test for injector module """
import unittest
from pathlib import Path
from shutil import copy
from shutil import rmtree

import toml

from injector import Dependencies
from injector import inject

TMP_DIR: Path = Path(__file__).absolute().parents[2].joinpath('test_tmp')
ASSETS_DIR: Path = Path(__file__).absolute().parents[1].joinpath('assets')


class TestInjector(unittest.TestCase):
    def setUp(self):
        TMP_DIR.mkdir(exist_ok=False, parents=False)

    def tearDown(self):
        rmtree(TMP_DIR)

    def test_injector_writes_expected_content_when_parsing_lock(self):
        # Copy some assets
        pipfile_path = TMP_DIR.joinpath('Pipfile.lock')
        pyproject_path = TMP_DIR.joinpath('pyproject.toml')
        pyproject_reference = ASSETS_DIR.joinpath('pyproject_from_lock.toml')

        copy(ASSETS_DIR.joinpath('Pipfile.lock'), pipfile_path)
        copy(ASSETS_DIR.joinpath('pyproject.toml'), pyproject_path)

        deps = Dependencies(
            prod=['argparse (==1.4.0)', 'toml (==0.9.4)'],
            dev=['aspy.yaml (==1.1.1)', 'astroid (==1.6.3)',
                 'cached-property (==1.4.2)', 'cfgv (==1.0.0)',
                 'identify (==1.0.16)', 'isort (==4.3.4)',
                 'lazy-object-proxy (==1.3.1)', 'mccabe (==0.6.1)',
                 'nodeenv (==1.3.0)', 'pre-commit (==1.8.2)',
                 'pylint (==1.8.4)', 'pyyaml (==3.12)', 'six (==1.11.0)',
                 'virtualenv (==15.2.0)', 'wrapt (==1.10.11)'])
        inject(deps, pyproject_path)

        with pyproject_reference.open('r') as expected_file, \
                pyproject_path.open('r') as infile:
            expected = toml.load(expected_file)
            result = toml.load(infile)

        self.assertDictEqual(expected, result)

    def test_injector_writes_expected_content_when_parsing_Pipfile(self):
        # Copy some assets
        pipfile_path = TMP_DIR.joinpath('Pipfile')
        pyproject_path = TMP_DIR.joinpath('pyproject.toml')
        pyproject_reference = ASSETS_DIR.joinpath(
            'pyproject_from_pipfile.toml')

        copy(ASSETS_DIR.joinpath('Pipfile'), pipfile_path)
        copy(ASSETS_DIR.joinpath('pyproject.toml'), pyproject_path)

        deps = Dependencies(
            prod=['toml (~=0.9.4)', 'argparse (~=1.4.0)'],
            dev=['pylint (~=1.8.4)', 'pre-commit (~=1.8.2)'])
        inject(deps, pyproject_path)

        with pyproject_reference.open('r') as expected_file, \
                pyproject_path.open('r') as infile:
            expected = toml.load(expected_file)
            result = toml.load(infile)

        self.assertDictEqual(expected, result)
