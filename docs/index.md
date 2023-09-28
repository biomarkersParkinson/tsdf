# Welcome to the TSDF (Time Series Data Format) Python package

A package to work with TSDF data in Python. This implementation is based on the the TSDF format specification, which can be found in this [preprint](https://arxiv.org/abs/2211.11294).

## What is TSDF data?

TSDF provides a unified, user-friendly format for both numerical sensor data and metadata, utilizing raw binary data and JSON-format text files for measurements/timestamps and metadata, respectively. It defines essential metadata fields to enhance data interpretability and exchangeability, aiming to bolster scientific reproducibility in studies reliant on digital biosensor data as a critical evidence base across various disease domains.


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
