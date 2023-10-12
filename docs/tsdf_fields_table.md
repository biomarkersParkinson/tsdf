# TSDF schema - metadata fields

TSDF metadata is represented as a dictionary. In this section, we will comprehensively list the mandatory and optional fields within the TSDF format.

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
| `channels`       | `str[]`      | Labels for each data channel (_e.g.:_ `[time]` for time channel or `[X, Y, Z]` for 3D accelerometry).                      |
| `time_encode`    | `str`        | Encoding type for time, e.g., "difference".                                  |
| `units`          | `str[]`      | Units for each channel in the data, e.g., "ms" for milliseconds.             |
| `data_type`      | `str`        | Number format of the measured data (_e.g.:_ `float`).                                             |
| `bits`           | `int`        | Bit-length of the number format (e.g., 32-bit).                                         |
| `columns`        | `int`        | Number of columns in the data matrix.                                        |
| `rows`           | `int`        | Number of rows in the data matrix.                                          |




# TSDF schema `Digital biomarkers for PD` extension

## Mandatory fields

| Field                      | Type         | Description                                                                       |
|----------------------------|--------------|-----------------------------------------------------------------------------------|
| `pd_bin_content`         | `bin_content_type`         | Description of the content of the data written in the binary file. The type is specific to the `Digital biomarkers for PD` extension. |
| `window_size_sec`          | `float`               | Size of the window (in seconds) used in the analysis.                             |
| `window_overlapped`        | `bool`                | Indicates whether there is overlap between consecutive windows in the analysis.   |
| `step_size_sec`            | `float`               | Duration in seconds for each segment in the written data.                         |
| `freq_sampling`            | `int`                 | Sampling frequency of the data.                                                   |

where `bin_content_type` can be one of the following:
- `iso8601_time`:           Time in iso8601 format, where each data window is characterised by the starting time (DateTime,TimeUnixClass).
- `gyro-tremor-features`:   Tremor-related features estimated (from gyro data) based on the windowed data (FeaturesGyro).
- `gyro-tremor-prob`:       Probability values indicating the likelihood (on the scale 0 to 1) of tremor activity for each sample (TremorProb)
- `gyro-tremor-hat`:        Estimated values representing the presence or absence of tremor activity for each sample (TremorHat).
- `gyro-arm-actv-prob`:     Probability values indicating the likelihood (on the scale 0 to 1) of arm activity for each sample (ArmActvProb).
- `gyro-arm-actv-hat`:      Estimated values representing the presence or absence of arm activity for each sample (ArmActvHat).
- `ppg-quality-post-prob`:  Posterior probability that the corresponding PPG signal is of high quality (PostProb).
- `accel_gait_features`:    Gait-related features estimated (from accelerometer data) based on the windowed data ().
- `accel_gait_prob`:        Probability values indicating the likelihood (on the scale 0 to 1) of gait activity for each sample ().
- `accel_arm_swing_features`: Arm swing-related features estimated (from accelerometer data) based on the windowed data ().
- `accel_arm_swing_prob`:   Probability values indicating the likelihood (on the scale 0 to 1) of arm swing activity for each sample ().


## **Tremor** pipeline specific fields

| Field                      | Type         | Description                                                                  |
|----------------------------|--------------|------------------------------------------------------------------------------|
| `mfcc_num_filters`         | `float`      | Number of filters used for estimating the mel-frequency cepstral coefficients. |
| `mfcc_num_mel_coeff`       | `float`      | Number of coefficients used for estimating the mel-frequency cepstral coefficients. |
| `mfcc_max_freq_filter`     | `float`      | Maximum frequency (in Hz) used for filtering in mel-frequency cepstral coefficients. |
| `mfcc_window_size`         | `float`      | Size of the sub-window in seconds used to estimate the spectrogram used in the evaluation of the mel-frequency cepstral coefficients. |
| `feature_names`             | `str[]`                  | List of names for the features.                                                      |
| `excluded_hours`            | `int[]`                  | Scaling factors for excluded hours.                                                   |
| `sum_features_gyro_scale`   | `str[]`                  | Scaling factors for the sum of gyro features.                                          |
| `sum_squared_features_gyro_scale` | `str[]`            | Scaling factors for the sum of squared gyro features.                                 |
| `n_features_gyro_scale`     | `int`                    | Scaling factor for the number of gyro features.                                        |

## **PPG** pipeline specific fields

| Field                      | Type                 | Description                                                                  |
|----------------------------|----------------------|------------------------------------------------------------------------------|
| `segment_number`           | `int`                | Order number of the analyzed data segment. |
| `freq_sampling_original`   | `int`                | Sampling frequency (in Hz) of the original data (before adjustments for the analysis).                                              |


## Additional TSDF field descriptions

These fields are optional, and provide standardised vocabulary for describing the data.


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