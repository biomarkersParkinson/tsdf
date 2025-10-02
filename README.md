
# tsdf

| Badges | |
|:----:|----|
| **Packages and Releases** | [![Latest release](https://img.shields.io/github/release/biomarkersparkinson/tsdf.svg)](https://github.com/biomarkersparkinson/tsdf/releases/latest) [![PyPI](https://img.shields.io/pypi/v/tsdf.svg)](https://pypi.python.org/pypi/tsdf/)  [![Static Badge](https://img.shields.io/badge/RSD-tsdf-lib)](https://research-software-directory.org/software/tsdf) |
| **Build Status** | [![](https://img.shields.io/badge/python-3.11%2C3.12-blue.svg)](https://www.python.org/downloads/) ![Build and test](https://github.com/biomarkersparkinson/tsdf/workflows/build-and-test.yml/badge.svg) |
| **DOI** | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7867899.svg)](https://doi.org/10.5281/zenodo.7867899) |
| **License** |  [![GitHub license](https://img.shields.io/github/license/biomarkersParkinson/tsdf)](https://github.com/biomarkersparkinson/tsdf/blob/main/LICENSE) |
| **Fairness** |  [![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F-green)](https://fair-software.eu) [![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/8083/badge)](https://www.bestpractices.dev/projects/8083) |



A package ([documentation](https://biomarkersparkinson.github.io/tsdf/)) to load TSDF data ([specification](https://arxiv.org/abs/2211.11294)) into Python.

## Overview
The [tsdf package](10.5281/zenodo.7867899) is a comprehensively documented reference implementation of the Time Series Data Format (TSDF) standard [[1]](https://arxiv.org/abs/2211.11294). TSDF simplifies data storage and exchange of multi-channel digital sensor data, thereby promoting interpretability and reproducibility of scientific results. Sensor measurements and timestamps are stored as raw tabular binary array files. To ensure unambiguous reconstruction, binary array files are accompanied by human-readable JavaScript Object Notation (JSON) metadata files, which contain a set of mandatory fields limited to essential sensor measurement information.

The tsdf Python package implements functions for reading and writing TSDF files. It guarantees formatting and metadata consistency. It enforces usage of the essential metadata such as study identification, time frame, data channel descriptions and data attributes corresponding to the binary data.

## Installation

### Using `pip`

The package is available in PyPi and requires [Python 3.11](https://www.python.org/downloads/) or higher. It can be installed using:

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
