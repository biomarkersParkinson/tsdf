# TSDF fields

TSDF metadata is represented as a dictionary. In this section, we will comprehensively list the mandatory and optional fields within the TSDF format.

## TSDF mandatory fields

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
| `channels`       | `str[]`      | Labels for each data channel (_e.g.:_ `["time", "X", "Y", "Z"]` for 3D accelerometry).                      |
| `time_encode`    | `str`        | Encoding type for time, e.g., "difference".                                  |
| `units`          | `str[]`      | Units for each channel in the data, e.g., "ms" for milliseconds.             |
| `data_type`      | `str`        | Number format of the measured data (_e.g.:_ `"float"`).                                             |
| `bits`           | `int`        | Bit-length of the number format (e.g., 32-bit).                                         |
| `columns`        | `int`        | Number of columns in the data matrix.                                        |
| `rows`           | `int`        | Number of rows in the data matrix.                                          |



## TSDF domain-specific fields


| Field                        | Type         | Description                                          |
|------------------------------|--------------|------------------------------------------------------|
| `start_datetime_unix_ms`     | `string`     | UNIX timestamp for the start of the recording (milliseconds). Equivalent to `start_iso8601` in UNIX format.   |
| `end_datetime_unix_ms`       | `string`     | UNIX timestamp for the end of the recording (milliseconds). Equivalent to `end_iso8601` in UNIX format.   | 
| `scale_factors`              | `float[]`    | Scale factors applied to each data channel to adjust their values.          | 
| `week_number`                | `int`        | Denotes the specific week for tracking or comparing weekly data. |
| `freq_sampling_original`     | `int`        | Represents the original sampling frequency at which the data was recorded. |
| `freq_sampling_adjusted`     | `int`        | The adjusted sampling frequency optimized for data processing or analysis. |
| `interpolate`                | `bool`       | If set to true, missing or irregular data points will be estimated and filled. |
| `gravity_removal`            | `bool`       | When true, the gravity component is removed to isolate user motion. |
| `apply_high_pass_filter`     | `bool`       | Indicates if a high-pass filter should be applied to remove low-frequency noise. |
| `normalize_acceleration`     | `bool`       | If true, accelerometer data is normalized using z-score normalization. |
| `motion_intensity_thresholds` | `int[]`     | List of percentage thresholds for categorizing motion intensity. |
| `accelerometer_burst_thresholds` | `float[]` | Threshold values for detecting 'burst' or sudden motion in the accelerometer. |
| `gyroscope_burst_thresholds` | `float[]`    | Threshold values for detecting 'burst' or sudden motion in the gyroscope. |
| `active_burst_threshold_percentile` | `int` | Chosen percentile index for active burst threshold from the list of percentile values. |
| `average_acceleration_across_weeks` | `float` | Average accelerometer reading across multiple weeks. |
| `acceleration_stddev_across_weeks` | `float` | Standard deviation of accelerometer readings across weeks. |
| `average_gyroscope_across_weeks` | `float` | Average gyroscope reading across weeks. |
| `gyroscope_stddev_across_weeks` | `float` | Standard deviation of gyroscope readings across weeks. |
| `window_size_sec`            | `int`        | Duration in seconds for each data window used in segmented analysis. |
| `num_ECDE_coeff`             | `int`        | Number of ECDE coefficients considered in the analysis. |
| `num_filters`                | `int`        | Number of filters applied to refine or isolate specific frequency bands. |
| `num_ME1_coeff`              | `int`        | Number of ME1 coefficients considered during data processing. |
| `max_frequency_filter`       | `int`        | Highest frequency limit for any applied filter. |




## Legacy fields

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