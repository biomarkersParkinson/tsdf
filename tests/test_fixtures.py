import pytest
import json


@pytest.fixture
def example_flat():
    """Returns a string containing the flat json example.
    Source: https://arxiv.org/abs/2211.11294"""
    data = """
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
        compression": "none",
        data_type": "int",
        bits": 16,
        file_name": "audio_voice_089.raw"
    }
    """
    return json.dumps(data)


@pytest.fixture
def example_hierarchical():
    """Returns a string containing the hierarchical json example.
    Source: https://arxiv.org/abs/2211.11294"""
    data = """
    {
    "subject_id": "PD0234",
    "study_id": "homestudy22",
    "device_id": "XBT7456",
    "endianness": "little",
    "metadata_version": "0.1",
    "data_type": "float",
    "bits": 32,
    "multi-day_session": [
        {
            "start_iso8601": "2022-26-10T09:26:45.123+00:00",
            "end_iso8601": "2022-26-10T09:36:52.266+00:00",
            "bits": 32,
            "sensors": [
                {
                    "rows": 60714,
                    "file_name": "accelerometer_t1.bin",
                    "channels": [
                        "time,",
                        "magnitude"
                    ],
                    "units": [
                        "ms",
                        "m/s/s"
                    ]
                },
                {
                    "rows": 607,
                    "file_name": "temperature_t1.bin",
                    "channels": [
                        "time",
                        "temperature"
                    ],
                    "units": [
                        "s",
                        "deg_C"
                    ]
                }
            ]
        },
        {
            "start_iso8601": "2022-28-10T10:42:12.465+00:00",
            "end_iso8601": "2019-28-10T13:54:36.578+00:00",
            "sensors": [
                {
                    "rows": 1154411,
                    "file_name": "accelerometer_t2.bin",
                    "channels": [
                        "time",
                        "magnitude"
                    ],
                    "units": [
                        "ms",
                        "m/s/s"
                    ]
                },
                {
                    "rows": 11544,
                    "file_name": "temperature_t2.bin",
                    "channels": [
                        "time",
                        "temperature"
                    ],
                    "units": [
                        "s",
                        "deg_C"
                    ]
                }
            ]
        }
    ]
}
    """
    return json.dumps(data)
