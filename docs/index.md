# Welcome to tsdf

A package to load [TSDF data](https://arxiv.org/abs/2211.11294) into Python.

## What is `TSDF data`?

`tsdf` stands for _time series data format_.
It is a unified, standardized format for storing all types of physiological sensor data. It was originally introduced in this [preprint](https://arxiv.org/abs/2211.11294).

### `TSDF data` in a nutshell

The key element of `TSDF data` is a metadata dictionary with the following:

#### Mandatory fields

| Field              | Description                                                                                                     | Type       |
|:-------------------|:----------------------------------------------------------------------------------------------------------------|:-----------|
| `subject_id`       | Unique identifier of the subject                                                                                | `string`   |
| `study_id`         | Unique identifier of the project or experiment                                                                  | `string`   |
| `device_id`        | Unique identifier of the measurement device                                                                     | `string`   |
| `endianness`       | [Byte order](https://en.wikipedia.org/wiki/Endianness) for numerical values in binary data ("big" or "little")  | `string`   |
| `metadata_version` | Format version (used for backwards compatibility)                                                               | `string`   |
| `start_iso8601`    | [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) time stamp for the start of the recording, with ms precision | `string`   |
| `end_iso8601`      | Same as `start_iso8601`, but for the end of the recording                                                       | `string`   |
| `rows`             | Total amount of samples per channel                                                                             | `uint`     |
| `filename`         | Name of the file containing the measured data                                                                   | `string`   |
| `channels`         | Labels for each data channel (_e.g.:_ `["time", "X", "Y", "Z"]` for 3D accelerometry)                           | `string[]` |
| `units`            | Unit for each channel (_e.g.:_ `["ms"]` for time)                                                               | `string[]` |
| `data_type`        | Number format of the measured data (_e.g.:_ `"float"`)                                                          | `string`   |
| `bits`             | Bit-length of the number format                                                                                 | `string`   |

#### Optional fields

| Field                    | Description                                    | Type      |
|:-------------------------|:-----------------------------------------------|:----------|
| `source_file_name`       | File containing the raw data                   | `string`  |
| `start_datetime_unix_ms` | Same as `start_iso8601`, but using UNIX format | `string`  |
| `end_datetime_unix_ms`   | Same as `end_iso8601`, but using UNIX format   | `string`  |
| `scale_factors`          | Scale factors applied to each channel          | `float[]` |
| `columns`                | Total amount of data channels per sample       | `uint`    |

#### Legacy fields

Work in progress.