
# TSDF fields

Below are the fields and descriptions for TSDF fields, obligatory and optional (study specific) fields.

## TSDF obligatory fields

| Field            | Type         | Description                                                                 |
|------------------|--------------|-----------------------------------------------------------------------------|
| study_id         | `str`        | Identifier for the particular study.                                         |
| device_id        | `str`        | Specifies the device used for data collection, e.g., "Galaxy 3 watch".       |
| subject_id       | `str`        | Unique identifier for the subject or participant in the study.               |
| source_file_name | `str`        | Name of the original source file containing the data.                        |
| endianness       | `str`        | Byte order representation. Common values are "little" or "big".              |
| metadata_version | `str`        | Version information for the metadata.                                        |
| start_iso8601    | `str`        | Timestamp indicating the start time of data collection in ISO8601 format.    |
| end_iso8601      | `str`        | Timestamp indicating the end time of data collection in ISO8601 format.      |
| file_name        | `str`        | The name of the file in consideration, e.g., "eeee.bin".                     |
| channels         | `list[str]`  | List specifying the channels in the data, e.g., "time".                      |
| time_encode      | `str`        | Encoding type for time, e.g., "difference".                                  |
| units            | `list[str]`  | Units for each channel in the data, e.g., "ms" for milliseconds.             |
| data_type        | `str`        | Type of the data, e.g., "float".                                             |
| bits             | `int`        | Bit-depth of the data, e.g., 32-bit.                                         |
| columns          | `int`        | Number of columns in the data matrix.                                        |
| rows             | `int`        | Number of rows in the data matrix. 


## TSDF optional fields


| Field                        | Type         | Description                                          |
|------------------------------|--------------|------------------------------------------------------|
| week_number                  | `int`        | Denotes the specific week for tracking or comparing weekly data. |
| freq_sampling_original       | `int`        | Represents the frequency at which the original data was sampled. |
| freq_sampling_adjusted       | `int`        | The revised frequency set to optimize data processing or analysis. |
| interpolate                  | `bool`       | If true, missing or irregular data points will be estimated and filled. |
| gravity_removal              | `bool`       | Removes the gravity component to isolate user motion if set to true. |
| fill_high_pass               | `bool`       | Indicates if a high-pass filter should be applied to remove low-frequency noise. |
| z_score_accel                | `bool`       | Normalizes accelerometer data using z-score normalization if true. |
| percent_vect                 | `list[int]`  | List of percentage thresholds for motion intensity categorization. |
| burst_thr_accel              | `list[float]`| Threshold values for accelerometer to detect 'burst' or sudden motion. |
| burst_thr_gyro               | `list[float]`| Threshold values for gyroscope to detect 'burst' or sudden motion. |
| index_percentil_burst_thr    | `int`        | Chosen index from the percentile list for active burst threshold. |
| inter_week_mean_accel        | `float`      | Average accelerometer reading across multiple weeks. |
| inter_week_std_accel         | `float`      | Standard deviation of accelerometer readings across weeks. |
| inter_week_mean_gyro         | `float`      | Average gyroscope reading across weeks. |
| inter_week_std_gyro          | `float`      | Standard deviation of gyroscope readings across weeks. |
| window_size_sec              | `int`        | Duration in seconds for each data window for segmented analysis. |
| num_ECDE_coeff               | `int`        | Number of ECDE coefficients considered in analysis. |
| num_filters                  | `int`        | Number of filters applied for refining or isolating specific frequency bands. |
| num_me1_coeff                | `int`        | Number of ME1 coefficients considered during processing. |
| max_freq_filter              | `int`        | Highest frequency limit for any applied filter. |