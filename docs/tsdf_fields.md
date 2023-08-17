# TSDF optional fields

Below are the fields and descriptions for optional TSDF fields:

- **week_number**: `int`  
  Denotes the specific week for which the dataset is relevant. Useful for tracking or comparing weekly data.

- **freq_sampling_original**: `int`  
  Represents the frequency in Hertz at which the original data was sampled before any modifications.

- **freq_sampling_adjusted**: `int`  
  The revised or adjusted frequency, also in Hertz, which might be set to optimize data processing or analysis.

- **interpolate**: `bool`  
  If set to true, any missing or irregular data points will be estimated and filled, ensuring a consistent dataset.

- **gravity_removal**: `bool`  
  If true, the gravity component (constant force affecting all gyroscopic measurements) will be removed to isolate user motion.

- **fill_high_pass**: `bool`  
  A flag indicating if the dataset should be subjected to a high-pass filter, which removes low-frequency noise.

- **z_score_accel**: `bool`  
  If true, the accelerometer data will be normalized using z-score normalization, converting values to a standard scale.

- **percent_vect**: `list[int]`  
  List of percentage thresholds. These could be used to categorize or grade the motion intensity based on magnitude.

- **burst_thr_accel**: `list[float]`  
  Set of threshold values specific to the accelerometer. Any value surpassing these indicates a 'burst' or sudden intense motion.

- **burst_thr_gyro**: `list[float]`  
  Similar to `burst_thr_accel`, but specific to gyroscope measurements.

- **index_percentil_burst_thr**: `int`  
  The chosen index from the percentile list to set the active burst threshold for data classification.

- **inter_week_mean_accel**: `float`  
  Provides the average accelerometer reading when comparing data across multiple weeks.

- **inter_week_std_accel**: `float`  
  Denotes the standard deviation for the accelerometer readings across weeks, providing insights into data variability.

- **inter_week_mean_gyro**: `float`  
  The average gyroscope reading across weeks, giving a central tendency measure for the gyro data.

- **inter_week_std_gyro**: `float`  
  Represents how spread out the gyroscope measurements are from the mean over different weeks.

- **window_size_sec**: `int`  
  Specifies the duration in seconds for each data window. Analysis is often performed on these smaller chunks of continuous data.

- **num_ECDE_coeff**: `int`  
  Dictates the number of ECDE (Empirical Cumulative Distribution Function) coefficients to be considered in the analysis.

- **num_filters**: `int`  
  Denotes how many different filters will be applied to the data for refining or isolating specific frequency bands.

- **num_me1_coeff**: `int`  
  Indicates the number of ME1 (possibly a specific kind of coefficient) to consider during the processing.

- **max_freq_filter**: `int`  
  The highest frequency limit for any applied filter, ensuring data above this frequency is not considered.