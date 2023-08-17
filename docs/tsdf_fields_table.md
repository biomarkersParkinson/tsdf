# TSDF optional fields

Below are the fields and descriptions for optional TSDF fields.


| Field                        | Type         | Description                                          |
|------------------------------|--------------|------------------------------------------------------|
| week_number                  | `int`        | The week number for which the data is relevant.       |
| freq_sampling_original       | `int`        | The original frequency at which the data was sampled. |
| freq_sampling_adjusted       | `int`        | Adjusted sampling frequency for data processing.      |
| interpolate                  | `bool`       | Indicates if interpolation should be performed.       |
| gravity_removal              | `bool`       | Determines if gravity should be removed.              |
| fill_high_pass               | `bool`       | Indicates if a high-pass filter should be applied.    |
| z_score_accel                | `bool`       | Should z-score normalization be applied on accel data?|
| percent_vect                 | `list[int]`  | Percentage vector thresholds for data classification. |
| burst_thr_accel              | `list[float]`| Burst threshold values for accelerometer data.        |
| burst_thr_gyro               | `list[float]`| Burst threshold values for gyroscope data.            |
| index_percentil_burst_thr    | `int`        | Index of the percentile for burst threshold.          |
| inter_week_mean_accel        | `float`      | Mean accelerometer value across weeks.                |
| inter_week_std_accel         | `float`      | Standard deviation of accelerometer value across weeks.|
| inter_week_mean_gyro         | `float`      | Mean gyroscope value across weeks.                    |
| inter_week_std_gyro          | `float`      | Standard deviation of gyroscope value across weeks.   |
| window_size_sec              | `int`        | Size of the window in seconds for data processing.    |
| num_ECDE_coeff               | `int`        | Number of ECDE coefficients to consider.              |
| num_filters                  | `int`        | Number of filters to apply.                           |
| num_me1_coeff                | `int`        | Number of ME1 coefficients to consider.               |
| max_freq_filter              | `int`        | Maximum frequency for filtering.                      |