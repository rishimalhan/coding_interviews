#! /usr/bin/python3

from dataclasses import dataclass
from abc import ABC, abstractmethod
from bisect import bisect_left, bisect_right
from typing import Optional
import threading
import time
from typing import Any
import numpy as np
from collections import deque


@dataclass
class SensorData:
    name: str
    timestamp: float
    values: float


class SensorAPI(ABC):
    def __init__(
        self,
        name: str,
        maxlen: int = 100,
        time_threshold: float = 1e-3,
    ):
        self._name = name
        self._timestamps = deque(maxlen=maxlen)
        self._messages = deque(maxlen=maxlen)
        self._timethrehsold = time_threshold

        self._lock = threading.Lock()

    def append_data(self, message: SensorData):
        with self._lock:
            timestamp = message.timestamp
            idx = bisect_left(self._timestamps)
            self._timestamps.insert(idx, timestamp)
            self._messages.insert(idx, message)

    def get_closest(self, reference_time: float):
        with self._lock:
            if len(self._timestamps) == 0:
                return None

            t_min = reference_time - self._timethrehsold
            t_max = reference_time + self._timethrehsold
            idx_left = bisect_left(self._timestamps, t_min)
            idx_right = bisect_right(self._timestamps, t_max)

            if idx_left == idx_right:
                return None

            candidate_ts = self._timestamps[idx_left:idx_right]
            errors = np.subtract(candidate_ts - reference_time)
            min_idx = int(np.argmin(errors))
            global_min = idx_left + min_idx

            return self._messages[global_min]

    @abstractmethod
    def callback(self):
        """
        Real sensor implementation should read hardware/API
        and call self.append_data(...)
        """
        pass


class FakeSensor(SensorAPI):
    def callback(self):
        msg = SensorData(
            name=self.name,
            timestamp=time.time(),
            data={"value": np.random.randn()},
        )
        self.append_data(msg)


class DataSynchronizer:
    def __init__(
        self,
        timestamp_tol: float = 0.02,
        missing_field: Any = None,
    ):
        self.timestamp_tol = timestamp_tol
        self.missing_field = missing_field
        self.sensors: dict[str, SensorAPI] = {}

    def add_sensor(self, sensor: SensorAPI):
        self.sensors[sensor.name] = sensor

    def sync(
        self,
        reference_time: Optional[float] = None,
        reference_sensor: Optional[str] = None,
    ):
        """
        If reference_sensor is given, use its latest timestamp.
        Otherwise use current wall time.

        Returns:
            packet: dict[str, SensorData | None]
            status: dict[str, str]
            all_ok: bool
        """

        if reference_sensor is not None:
            ref_api = self.sensors[reference_sensor]

            with ref_api.lock:
                if not ref_api.timestamps:
                    return {}, {}, False

                reference_time = ref_api.timestamps[-1]

        if reference_time is None:
            reference_time = time.time()

        packet = {}
        status = {}
        all_ok = True

        for name, sensor in self.sensors.items():
            msg = sensor.get_closest(
                reference_time=reference_time,
                tolerance=self.timestamp_tol,
            )

            if msg is None:
                packet[name] = self.missing_field
                status[name] = "missing_or_out_of_sync"
                all_ok = False
            else:
                packet[name] = msg
                status[name] = "ok"

        return packet, status, all_ok


if __name__ == "__main__":

    camera = FakeSensor("camera", maxsize=100)
    joint = FakeSensor("joint", maxsize=300)
    tactile = FakeSensor("tactile", maxsize=500)

    sync = DataSynchronizer(timestamp_tol=0.02)

    sync.add_sensor(camera)
    sync.add_sensor(joint)
    sync.add_sensor(tactile)

    # Simulate incoming data
    joint.append_data(SensorData("joint", 1.000, {"q": [1, 2, 3]}))
    joint.append_data(SensorData("joint", 1.010, {"q": [4, 5, 6]}))
    tactile.append_data(SensorData("tactile", 0.995, {"force": 3.1}))
    camera.append_data(SensorData("camera", 1.005, {"image": "frame"}))

    packet, status, ok = sync.sync(reference_sensor="camera")

    print(ok)
    print(status)
    print(packet)
