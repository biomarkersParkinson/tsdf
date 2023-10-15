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
| `columns`        | `int`        | Number of columns in the data matrix.                                        |
| `rows`           | `int`        | Number of rows in the data matrix.                                          |




# TSDF schema `Digital biomarkers for PD` extension

## Mandatory fields

This is a preliminary list of mandatory fields for the `Digital biomarkers for PD` extension. The list will be updated based on the upcoming discussions.

| Field                      | Type         | Description                                                                       |
|----------------------------|--------------|-----------------------------------------------------------------------------------|
| `window_size_sec`          | `float`               | Size of the window (in seconds) used in the analysis.                             |
| `window_overlapped`        | `float`                | Indicates whether there is overlap between consecutive windows in the analysis.   |
| `step_size_sec`            | `float`               | Duration in seconds for each segment in the written data.                         |
| `freq_sampling`            | `int`                 | Sampling frequency (in Hz) of the input data.                                                   |
| `channels`         | [channel_type](tsdf_field_types.md)`[]`         | Description of the content of the data written. `channel_type` is specific to the `Digital biomarkers for PD` extension. |
| `units`         | [unit_type](tsdf_field_types.md)`[]`         | Description of the format of the data written. `unit_type` is specific to the `Digital biomarkers for PD` extension. |



## **Tremor** pipeline specific fields

Non-mandatory fields used in the tremor pipeline.

| Field                      | Type         | Description                                                                  |
|----------------------------|--------------|------------------------------------------------------------------------------|
| `mfcc_num_filters`         | `float`      | Number of filters used for estimating the mel-frequency cepstral coefficients. |
| `mfcc_num_mel_coeff`       | `float`      | Number of coefficients used for estimating the mel-frequency cepstral coefficients. |
| `mfcc_max_freq_filter`     | `float`      | Maximum frequency (in Hz) used for filtering in mel-frequency cepstral coefficients. |
| `mfcc_window_size`         | `float`      | Size of the sub-window in seconds used to estimate the spectrogram used in the evaluation of the mel-frequency cepstral coefficients. |
| `feature_names`             | `str[]`                  | List of names for the features.                                                      |
| `excluded_hours`            | `int[]`                  | `[TODO]` List of the excluded hours from the analysis (vector scaling?)                                                  |
| `sum_features_gyro_scale`   | `float[]`                  | `[TODO]` Scaling factors for the sum of tremor-related features (from gyro)                                          |
| `sum_squared_features_gyro_scale` | `float[]`            | `[TODO]` Scaling factors for the sum of squared tremor-related features (from gyro)                                 |
| `n_features_gyro_scale`     | `int`                    | `[TODO]` Scaling factor for the number of gyro features                                        |

## **PPG** pipeline specific fields

Non-mandatory fields used in the PPG pipeline.

| Field                      | Type                 | Description                                                                  |
|----------------------------|----------------------|------------------------------------------------------------------------------|
| `segment_number`           | `int`                | Order number of the analyzed data segment. |
| `freq_sampling_original`   | `int`                | Sampling frequency (in Hz) of the original data (before adjustments for the analysis).                                              |

## **Gait** pipeline specific fields

Non-mandatory fields used in the gait pipeline. We currently do not have information about the fields used in the gait pipeline, but we will update this section as soon as we have more information.

| Field                      | Type                 | Description                                                                  |
|----------------------------|----------------------|------------------------------------------------------------------------------|
| `field_name`           | `int`                | `[TODO]` Field description. |

## Additional TSDF field descriptions

These fields are non-mandatory, and provide standardised vocabulary for describing the data.


| Field                        | Type         | Description                                          |
|------------------------------|--------------|------------------------------------------------------|
| `week_number`                | `int`        | Denotes the specific week for tracking or comparing weekly data. |
| `interpolated`               | `bool`       | Indicates whether interpolation was performed on the data. |
| `high_pass_filter_applied`   | `bool`       | Indicates whether a high-pass filter was applied to remove low-frequency noise. |
| `high_pass_filter_cutoff`    | `float`      | Cutoff frequency (in Hz) for the high-pass filter, in case it was applied. |
| `z_score_normalised`         | `bool`       | Indicates whether z-score normalization was applied to the data. |
| `start_datetime_unix_ms`     | `string`     | UNIX timestamp for the start of the recording (milliseconds). Equivalent to `start_iso8601` in UNIX format.   |
| `end_datetime_unix_ms`       | `string`     | UNIX timestamp for the end of the recording (milliseconds). Equivalent to `end_iso8601` in UNIX format.   | 




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