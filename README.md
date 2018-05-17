# pynjector

[Flit][flit] dependency injector from [Pipenv][pipenv] for [Python3][python3]

## Usage

First of all, generate a python environment with Pipenv if you haven't
got any and install `pynjector`:

```sh
pipenv install
pipenv install pynjector-0.1-py3-none-any.whl
```

and activate the environment:

```sh
pipenv shell
```

### As an script

Run the tool as an script:

```sh
python -m pynjector.injector -p Pipfile
```

You can add the argument `-h` to check for options.

### As a module

Just import it in your python module or run it in your python shell:

```python
from pathlib import Path
import pynjector

deps = pynjector.parse_pipenv(Path('Pipfile.lock'))
pynjector.inject(deps, Path('pyproject.toml'))
```

**Note: no wheel is currently available online but you can build one
following the steps indicated in [Building](#building) section**

## Developing

Clone this project and generate a python environment for developing with
Pipenv:

```sh
pipenv install --dev
```

### Packaging

Following [PEP 518][pep518] recommendations, this project can be easily
build by using [Flit][flit], following this steps:

- Update library version in `src\__init__.py`
- In case of dependency changes, use injector to update `pyproject.toml`
    ```
    python pynjector/injector
    ```
- Ask Flit to generate the wheel:
    ```sh
    flit build --format wheel
    ```
- Check `dist` directory for the compiled library


[flit]: https://flit.readthedocs.io/en/latest/index.html
[pipenv]: http://pipenv.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[python3]: https://docs.python.org/3/
[pep518]: https://www.python.org/dev/peps/pep-0518/
