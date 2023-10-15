# Custom field values (TSDF schema `Digital biomarkers for PD` extension)

Within the `Digital biomarkers for PD` extension, some of the field types are further specialised to provide a better description of the data. These are described in the following sections.

## Field: `channels`
**Type:** `channel_type[]`         
**Description:** Describes the content of the data written. `channel_type` is specific to the `Digital biomarkers for PD` extension.

---

**General types**

|   `channel_type` name          | Recommended `unit`       | Description                                                                           |
|----------------------------|-----------------------|---------------------------------------------------------------------------------------|
| `iso8601_time`              | `time`                | Time in ISO8601 format, characterizing each data window by its starting time.          |

---

<details>
<summary><b>PPG-related types</b></summary>

|   `channel_type` name          | Recommended `unit`       | Description                                                                           |
|----------------------------|-----------------------|---------------------------------------------------------------------------------------|
| `ppg_quality_post_prob`     | `probability`         | `[TODO]` Posterior probability that the corresponding PPG signal is of high quality (0 to 1).   |
</details>

---

<details>
<summary><b>Tremor-related types</b></summary>

| `channel_type` name       | Recommended `unit` | Description                                                                         |
|--------------------------|--------------------|-------------------------------------------------------------------------------------|
| `gyro_tremor_prob`       | `probability`      | Probability values (0 to 1) indicating the likelihood of tremor activity for each sample. |
| `gyro_tremor_hat`        | `boolean_num`         | Estimated values representing the presence or absence of tremor activity for each sample. |
| `gyro_arm_actv_prob`     | `probability`      | Probability values (0 to 1) indicating the likelihood of arm activity for each sample.    |
| `gyro_arm_actv_hat`      | `boolean_num`         | Estimated values representing the presence or absence of arm activity for each sample.    |
| `GyMeanDx`               | `unitless`         | Mean gyro derivative in the x axis. |
| `GyMeanDy`               | `unitless`         | Mean gyro derivative in the y axis. |
| `GyMeanDz`               | `unitless`         | Mean gyro derivative in the z axis. |
| `GyLTreDomPowerX`        | `unitless`         | Gyro Low tremor (range [3.5-8 Hz]) dominant power in the x axis. |
| `GyLTreDomPowerY`        | `unitless`         | Gyro Low tremor (range [3.5-8 Hz]) dominant power in the y axis. |
| `GyLTreDomPowerZ`        | `unitless`         | Gyro Low tremor (range [3.5-8 Hz]) dominant power in the z axis. |
| `GyGaitBandPower`        | `unitless`         | Gyro gait bandpower (range [0.4 – 2] Hz) – PSD: sum of the axes. |
| `GyGaitBandpowerRatio`   | `unitless`         | Gyro gait bandpower sum / total bandpower sum up to 15 Hz – PSD: sum of the axes. |
| `GyGaitFreqPeak`         | `unitless`         | Frequency peak of the in the gyro gait range – PSD: sum of the axes. |
| `GyGaitFixedDomPower`    | `unitless`         | `[TODO]` Gyro dominant power in a fixed range (specific frequency range not provided). |
| `GyGaitFixedDomPowerRatio` | `unitless`       | `[TODO]` Ratio of dominant power in the gyro gait range to total power. |
| `GyGaitDomPower`         | `unitless`         | `[TODO]` Dominant power in the gyro gait range. |
| `GyGaitDomPowerRatio`    | `unitless`         | `[TODO]` Ratio of dominant power in the gyro gait range to total power. |
| `GyGaitPeakFreqWidth`    | `unitless`         | `[TODO]` Width of the frequency peak in the gyro gait range. |
| `GyLTreBandPower`        | `unitless`         | `[TODO]` Low tremor bandpower (specific frequency range not provided). |
| `GyLTreBandpower`        | `unitless`         | `[TODO]` Low tremor bandpower (specific frequency range not provided). |
| `GyLTreFreqPeak`         | `unitless`         | `[TODO]` Frequency peak in the low tremor range. |
| `GyLTreFixedDomP`        | `unitless`         | `[TODO]` Low tremor dominant power in a fixed range (specific frequency range not provided). |
| `GyLTreFixedDomP`        | `unitless`         | `[TODO]` Low tremor dominant power in a fixed range (specific frequency range not provided). |
| `GyLTreDomPower`         | `unitless`         | `[TODO]` Low tremor dominant power (specific frequency range not provided). |
| `GyLTreDomPowerR`        | `unitless`         | `[TODO]` Ratio of low tremor dominant power to total power. |
| `GyLTrePeakFreqW`        | `unitless`         | `[TODO]` Width of the frequency peak in the low tremor range. |
| `GyHTreBandPower`        | `unitless`         | `[TODO]` High tremor bandpower (specific frequency range not provided). |
| `GyHTreBandpower`        | `unitless`         | `[TODO]` High tremor bandpower (specific frequency range not provided). |
| `GyHTreFreqPeak`         | `unitless`         | `[TODO]` Frequency peak in the high tremor range. |
| `GyHTreFixedDomP`        | `unitless`         | `[TODO]` High tremor dominant power in a fixed range (specific frequency range not provided). |
| `GyHTreFixedDomP`        | `unitless`         | `[TODO]` High tremor dominant power in a fixed range (specific frequency range not provided). |
| `GyHTreDomPower`         | `unitless`         | `[TODO]` High tremor dominant power (specific frequency range not provided). |
| `GyHTreDomPowerR`        | `unitless`         | `[TODO]` Ratio of high tremor dominant power to total power. |
| `GyHTrePeakFreqW`        | `unitless`         | `[TODO]` Width of the frequency peak in the high tremor range. |
| `GyMFCC1`                | `unitless`         | `[TODO]` Mel-frequency cepstral coefficient 1. |
| `GyMFCC2`                | `unitless`         | `[TODO]` Mel-frequency cepstral coefficient 2. |
| `GyMFCC3`                | `unitless`         | `[TODO]` Mel-frequency cepstral coefficient 3. |
| `GyMFCC4`                | `unitless`         | `[TODO]` Mel-frequency cepstral coefficient 4. |
| `GyMFCC5`                | `unitless`         | `[TODO]` Mel-frequency cepstral coefficient 5. |
| `GyMFCC6`                | `unitless`         | `[TODO]` Mel-frequency cepstral coefficient 6. |
| `GyMFCC7`                | `unitless`         | `[TODO]` Mel-frequency cepstral coefficient 7. |
| `GyMFCC8`                | `unitless`         | `[TODO]` Mel-frequency cepstral coefficient 8. |
| `GyMFCC9`                | `unitless`         | `[TODO]` Mel-frequency cepstral coefficient 9. |


</details>

---

<details>
<summary><b>Gait-related types</b></summary>

| `channel_type` name       | Recommended `unit` | Description                                                                         |
|--------------------------|--------------------|-------------------------------------------------------------------------------------|
| `accel_gait_feature_1`       | `unitless`            | `[TODO]` Gait-related feature 1 estimated from accelerometer data based on the windowed data `[TODO]`.     |
| `accel_gait_feature_2`       | `unitless`            | `[TODO]` Gait-related feature 2 estimated from accelerometer data based on the windowed data `[TODO]`.     |
| `accel_gait_prob`           | `probability`         | `[TODO]` Probability values (0 to 1) indicating the likelihood of gait activity for each sample.  |
| `accel_arm_swing_feature1`  | `unitless`            | `[TODO]` Arm swing-related feature 1 estimated from accelerometer data based on the windowed data`[TODO]`. |
| `accel_arm_swing_feature2`  | `unitless`            | `[TODO]` Arm swing-related feature 2 estimated from accelerometer data based on the windowed data`[TODO]`. |
| `accel_arm_swing_prob`      | `probability`         | `[TODO]` Probability values (0 to 1) indicating the likelihood of arm swing activity for each sample. |
</details>

---
---

## Field: `units`
**Type:** `unit_type[]`         
**Description:** Describes the format of the data written. `unit_type` is specific to the `Digital biomarkers for PD` extension.


|   `unit_type` name          | Description                                                                           |
|----------------------------|---------------------------------------------------------------------------------------|
| `time`              | Time in ISO8601 format, characterizing each data window by its starting time.                |
| `probability`       | Probability values (0 to 1) indicating the likelihood of tremor activity for each sample.    |
| `boolean_num`       | `[TODO]` Integer values (0 or 1) representing the true (1) or false (0) presence of an activity.      |
| `unitless`          | Numerical values without units.                                                              |
