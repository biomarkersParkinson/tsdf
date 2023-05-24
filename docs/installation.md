# Installation

## Requirements

`tsdf` requires a recent version of [Python](https://www.python.org/) and a Python package manager (such as `pip`).
Chances are that you have them already installed.
You can check if that's the case from the command line:

```bash
python --version
```

```bash
pip --version
```

## Installing tsdf

The package is available in [PyPI](https://pypi.org/project/tsdf/). The latest stable release can be installed using:

```bash
$ pip install tsdf
```

### Installing the develop version

The source code is stored and maintained on [GitHub](https://github.com/biomarkersParkinson/tsdf).

If you have `git` installed, the latest version of tsdf can be installed by typing:

```bash
pip install 'tsdf @ git+https://github.com/biomarkersParkinson/tsdf.git'
```

Otherwise you can install it manually by following these steps:

1. Download or clone the content from [our repository](https://github.com/biomarkersParkinson/tsdf).
2. Browse to the folder you just downloaded (typically: `cd tsdf/`).
3. Install using your package manager (typically: `pip install .`).

## What now?

Now you can import functions from the `tsdf` Python package.
See some examples in the next section.