# TSDF schema - metadata fields

TSDF metadata is represented as a dictionary (or a JSON object). In this section, we will comprehensively list the mandatory and optional fields within the TSDF format.

## TSDF v0.1 mandatory fields

| Field            | Type         | Description                                                                 |
|------------------|--------------|-----------------------------------------------------------------------------|
| `study_id`       | `str`        | Unique identifier for the particular study.                                         |
| `device_id`      | `str`        | Specifies the device used for data collection.       |
| `subject_id`     | `str`        | Unique identifier for the subject or participant in the study.               |
| `source_file_name` | `str`     | Name of the original source file containing the data.                        |
| `endianness`     | `str`        | [Byte order](https://en.wikipedia.org/wiki/Endianness) for numerical values in binary data ("big" or "little").             |
| `metadata_version` | `str`    | Version information for the metadata.                                        |
| `start_iso8601`  | `str`        | [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) time stamp for the start of the recording, with ms precision.     |
| `end_iso8601`    | `str`        | Same as `start_iso8601`, but for the end of the recording.                     |
| `file_name`      | `str`        | The name of the file in consideration, e.g., "eeee.bin".                     |
| `channels`       | `str[]`      | Labels for each data channel (_e.g.:_ `[time]` for time data or `[X, Y, Z]` for 3D accelerometry).                      |
| `time_encode`    | `str`        | Encoding type for time, e.g., "difference".                                  |
| `units`          | `str[]`      | Units for each channel in the data, e.g., "ms" for milliseconds.             |
| `data_type`      | `str`        | Number format of the measured data (_e.g.:_ `float`).                                             |
| `bits`           | `int`        | Bit-length of the number format (e.g., 32-bit).                                         |
| `rows`           | `int`        | Number of rows in the data matrix.                                          |



# Legacy fields

The following table lists the legacy fields from the time when the format was called TSDB, along with their updated counterparts:

| Legacy field             | Updated field               | Updated data type     |
|--------------------------|-----------------------------|---------------|
| `project_id`             | `study_id`                  | -        |
| `quantities`             | `channels`                  | `str[]`      |
| `units`                  | `units`                     | `str[]`      |
| `datatype`               | `data_type`                 | -        |
| `start_datetime_iso8601` | `start_iso8601`             | -        |
| `end_datetime_iso8601`   | `end_iso8601`               | -        |

**Note**

As presented in the table above, the `quantities` and `units` fields are required to be arrays within the TSDF standard.