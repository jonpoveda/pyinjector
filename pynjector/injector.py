# -*- coding: utf-8 -*-
""" Flint dependency injector from Pipenv for Python """
import argparse
import json
from pathlib import Path
from typing import Iterable
from typing import Tuple

import toml


def format(deps: dict) -> Iterable:
    """ Formats a dictionary into a TOML list of packages """
    return [f'{package} ({value.get("version")})'
            for package, value in deps.items()]


def inject(deps: Iterable, deps_dev: Iterable, config_file: Path) -> None:
    """ Replaces dependencies from a Flit's configuration file

    Args:
         deps: dependencies for prod
         deps_dev: dependencies for dev
         file: Flit's configuration file (`pyproject.toml`)
    """
    with config_file.open('r') as original_config:
        config = toml.load(original_config)
        config['tool']['flit']['metadata']['requires'] = deps
        config['tool']['flit']['metadata']['dev-requires'] = deps_dev

    with config_file.open('w') as outfile:
        toml.dump(config, outfile)


def parse_lock(file: Path) -> Tuple[Iterable, Iterable]:
    """ Formats Pipenv dependencies for Flit

    Formats `Pipfile.lock` dependencies as expected for Flit's `pyproject.toml`

    Args:
        file: path to a `Pipfile.lock`

    Returns:
        two dependency lists

    See also:
        `PEP 518`_, `Pipenv`_ , `Flit`_

    .. _PEP 518:
        https://www.python.org/dev/peps/pep-0518/
    .. _Pipenv:
        http://pipenv.readthedocs.io/en/latest/
    .. _Flit:
        https://pypi.org/project/flit/
    """
    with file.open('r') as infile:
        data = json.load(infile)
        deps = format(data['default'])
        deps_dev = format(data['develop'])

    return deps, deps_dev


def main():
    # Get parameters from arguments
    parser = argparse.ArgumentParser(description='Python dependency injector')
    parser.add_argument('-l', '--lock',
                        type=Path, default=Path('Pipfile.lock'),
                        help='path to Pipfile.lock file')
    parser.add_argument('-c', '--config',
                        type=Path, default=Path('pyproject.toml'),
                        help="path to Flit's config file path")
    parser.add_argument('--safe',
                        action='store_true',
                        help="set to not overwrite Flit's config file")
    arguments = parser.parse_args()

    prod_deps, dev_deps = parse_lock(Path(arguments.lock))

    if arguments.safe:
        print(f'The extracted project dependencies are: \n'
              f'{prod_deps}\n'
              f'and for develop are: \n'
              f'{dev_deps}')

    else:
        inject(prod_deps, dev_deps, config_file=Path(arguments.config))


if __name__ == '__main__':
    try:
        main()
    except AssertionError as expected:
        print(expected.args[0])
        exit(1)
