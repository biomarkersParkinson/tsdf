
# tsdf

| Badges | |
|:----:|----|
| **Packages and Releases** | [![Latest release](https://img.shields.io/github/release/biomarkersparkinson/tsdf.svg)](https://github.com/biomarkersparkinson/tsdf/releases/latest) [![PyPI](https://img.shields.io/pypi/v/tsdf.svg)](https://pypi.python.org/pypi/tsdf/)  [![Static Badge](https://img.shields.io/badge/RSD-tsdf-lib)](https://research-software-directory.org/software/tsdf) |
| **Build Status** | [![](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) ![Python package](https://github.com/biomarkersparkinson/tsdf/workflows/Python%20package/badge.svg) [![pytype Type Check](https://github.com/biomarkersParkinson/tsdf/actions/workflows/pytype-checking.yml/badge.svg)](https://github.com/biomarkersParkinson/tsdf/actions/workflows/pytype-checking.yml) |
| **DOI** | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7867899.svg)](https://doi.org/10.5281/zenodo.7867899) |
| **License** |  [![GitHub license](https://img.shields.io/github/license/biomarkersParkinson/tsdf)](https://github.com/biomarkersparkinson/tsdf/blob/main/LICENSE) |
| **Fairness** |  [![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F-green)](https://fair-software.eu) [![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/8083/badge)](https://www.bestpractices.dev/projects/8083) |



A package ([documentation](https://biomarkersparkinson.github.io/tsdf/)) to load TSDF data ([specification](https://arxiv.org/abs/2211.11294)) into Python.

## Installation

### Using `pip`

The package is available in PyPi and requires [Python 3.9](https://www.python.org/downloads/) or higher. It can be installed using:

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

We use [Sphinx](https://www.sphinx-doc.org/) to build the documentation. Use this command to build the documentation locally:

```bash
poetry run make html --directory docs
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details on coding standards, how to get started, and the submission process.

## Code of Conduct

To ensure a welcoming and respectful community, all contributors and participants are expected to adhere to our [Code of Conduct](CONDUCT.md). By participating in this project, you agree to abide by its terms.

## License

This package was created by Pablo Rodríguez, Peter Kok and Vedran Kasalica. It is licensed under the terms of the Apache License 2.0 license.

## Credits

- The [TSDF data format](https://arxiv.org/abs/2211.11294) was created by Kasper Claes, Valentina Ticcinelli, Reham Badawy, Yordan P. Raykov, Luc J.W. Evers, Max A. Little.
- This package was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
