# -*- coding: utf-8 -*-
""" Flint dependency injector from Pipenv for Python """
import argparse
import json
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterable

import toml


def parse(deps: Dict[str, Any]) -> Iterable:
    """ Formats Pipenv dependencies for Flit

    Formats 'Pipfile.lock' dependencies as expected for Flit's 'pyproject.toml'

    See also:
        `PEP 518`_, `Pipenv`_ , `Flit`_

    .. _PEP 518:
        https://www.python.org/dev/peps/pep-0518/
    .. _Pipenv:
        http://pipenv.readthedocs.io/en/latest/
    .. _Flit:
        https://pypi.org/project/flit/
    """

    return [f'{package} ({value.get("version")})'
            for package, value in deps.items()]


def inject(pipfile: Path, project_config: Path, safe: bool):
    with pipfile.open('r') as infile:
        data = json.load(infile)
        deps = parse(data['default'])
        deps_dev = parse(data['develop'])

    with project_config.open('r') as original_config:
        config = toml.load(original_config)
        config['tool']['flit']['metadata']['requires'] = deps
        config['tool']['flit']['metadata']['dev-requires'] = deps_dev

    if not safe:
        with project_config.open('w') as outfile:
            toml.dump(config, outfile)

    return deps, deps_dev


def main():
    # Get parameters from arguments
    parser = argparse.ArgumentParser(description='Python dependency injector')
    parser.add_argument('-p',
                        type=Path, default=Path('Pipfile.lock'),
                        help='path to Pipfile.lock file')
    parser.add_argument('-f',
                        type=Path, default=Path('pyproject.toml'),
                        help="path to Flit's config file path")
    parser.add_argument('--safe',
                        action='store_true',
                        help="set to not overwrite Flit's config file")
    arguments = parser.parse_args()

    deps, deps_dev = inject(pipfile=Path(arguments.p),
                            project_config=Path(arguments.f),
                            safe=bool(arguments.safe))

    if arguments.safe:
        print(f'The extracted project dependencies are: \n'
              f'{deps}\n'
              f'and for develop are: \n'
              f'{deps_dev}')


if __name__ == '__main__':
    try:
        main()
    except AssertionError as expected:
        print(expected.args[0])
        exit(1)
