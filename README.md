
# Welcome to the TSDF (Time Series Data Format)

| Badges | |
|:----:|----|
| **Packages and Releases** | [![Latest release](https://img.shields.io/github/release/biomarkersparkinson/tsdf.svg)](https://github.com/biomarkersparkinson/tsdf/releases/latest) [![PyPI](https://img.shields.io/pypi/v/tsdf.svg)](https://pypi.python.org/pypi/tsdf/)  [![Static Badge](https://img.shields.io/badge/RSD-tsdf-lib)](https://research-software-directory.org/software/tsdf) |
| **Build Status** | [![](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/) ![Python package](https://github.com/biomarkersparkinson/tsdf/workflows/Python%20package/badge.svg) [![pytype Type Check](https://github.com/biomarkersParkinson/tsdf/actions/workflows/pytype-checking.yml/badge.svg)](https://github.com/biomarkersParkinson/tsdf/actions/workflows/pytype-checking.yml) |
| **DOI** | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7867899.svg)](https://doi.org/10.5281/zenodo.7867899) |
| **License** |  [![GitHub license](https://img.shields.io/github/license/biomarkersParkinson/tsdf)](https://github.com/biomarkersparkinson/tsdf/blob/main/LICENSE) |
| **Fairness** |  [![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F-green)](https://fair-software.eu) [![OpenSSF Best Practices](https://bestpractices.coreinfrastructure.org/projects/8083/badge)](https://www.bestpractices.dev/projects/8083) |

A package to work with TSDF data in Python. This implementation is based on the the TSDF format specification, which can be found in this [preprint](https://arxiv.org/abs/2211.11294).

## What is TSDF data?

TSDF provides a unified, user-friendly format for both numerical sensor data and metadata, utilizing raw binary data and JSON-format text files for measurements/timestamps and metadata, respectively. It defines essential metadata fields to enhance data interpretability and exchangeability, aiming to bolster scientific reproducibility in studies reliant on digital biosensor data as a critical evidence base across various disease domains.

## How does the TSDF library work?

Detailed documentation and examples can be found in the [documentation](https://biomarkersparkinson.github.io/tsdf/).

## Example: TSDF Metadata

This example demonstrates a TSDF metadata JSON file, showcasing the structured format used to easily interpret and read the corresponding binary data. For more intricate examples and detailed specifications, the paper serves as a comprehensive reference.

```json
{
    "study_id": "voicedata",
    "subject_id": "recruit089",
    "device_id": "audiotechnica02",
    "endianness": "little",
    "metadata_version": "0.1",
    "start_iso8601": "2016-08-09T10:31:00.000+00:00",
    "end_iso8601": "2016-08-10T10:31:30.000+00:00",
    "sampling_rate": 44100,
    "rows": 1323000,
    "channels": [
        "left",
        "right"
    ],
    "units": [
        "unitless",
        "unitless"
    ],
    "compression": "none",
    "data_type": "int",
    "bits": 16,
    "file_name": "audio_voice_089.raw"
}
```
**Explanation:**

- `study_id`: Identifies the study as "voicedata".

- `subject_id`: Specifies the subject as "recruit089".

- `device_id`: Indicates the device used as "audiotechnica02".

- `endianness`: Specifies the byte order as "little".

- `metadata_version`: Denotes the metadata version as "0.1".

- `start_iso8601` and `end_iso8601`: Define the start and end timestamps of data collection in ISO 8601 format.

- `sampling_rate`: Represents the data sampling rate as 44,100 samples per second.

- `rows`: Specifies the number of data rows as 1,323,000.

- `channels`: Lists the data channels as "left" and "right".

- `units`: Specifies the units for each channel as "unitless".

- `compression`: Indicates that no compression has been applied to the data.

- `data_type`: Defines the data type as "int".

- `bits`: Specifies the bit length as 16.

- `file_name`: Names the binary file "audio_voice_089.raw" that contains the described data.



## The python library - `tsdf`
This Python library facilitates the manipulation of Time Series Data Format (TSDF) metadata and binary files, providing users with a familiar and structured interface. Leveraging the power of numpy arrays, it simplifies the process of working with TSDF data, allowing users to efficiently read, write, and manipulate both metadata and binary data. This approach enhances data management and analysis, making it a valuable tool for researchers and data scientists dealing with extensive physiological sensor data.


The package is available in [PyPI](https://pypi.org/project/tsdf/).

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details on coding standards, how to get started, and the submission process.

## Code of Conduct

To ensure a welcoming and respectful community, all contributors and participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by its terms.

## Credits

- The [TSDF data format](https://arxiv.org/abs/2211.11294) was created by Kasper Claes, Valentina Ticcinelli, Reham Badawy, Yordan P. Raykov, Luc J.W. Evers, Max A. Little.
- This package was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
