
![Python package](https://github.com/biomarkersparkinson/tsdf/workflows/Python%20package/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/tsdf.svg)](https://pypi.python.org/pypi/tsdf/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7867900.svg)](https://doi.org/10.5281/zenodo.7867900)

# tsdf

A package to load [TSDF data](https://arxiv.org/abs/2211.11294) into Python

## Installation

### Using `pip`

The package is available in PyPi. It can be installed using:

```bash
$ pip install tsdf
```

## Usage

See our [extended tutorials](https://biomarkersparkinson.github.io/tsdf/).

## Development

### Running tests

```bash
poetry install
poetry run pytest
```

### Building the documentation

We use [mkdocs](https://www.mkdocs.org/) to build the documentation. If you want to build the documentation locally, the following commands will prove useful:

```bash
mkdocs build       # build the documentation
mkdocs serve       # serve the documentation on a local server
mkdocs gh-deploy   # deploy the documentation to GitHub pages
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

This package was created by Pablo Rodríguez, Peter Kok and Vedran Kasalica. It is licensed under the terms of the Apache License 2.0 license.

## Credits

- The [TSDF data format](https://arxiv.org/abs/2211.11294) was created by Kasper Claes, Valentina Ticcinelli, Reham Badawy, Yordan P. Raykov, Luc J.W. Evers, Max A. Little.
- This package was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
