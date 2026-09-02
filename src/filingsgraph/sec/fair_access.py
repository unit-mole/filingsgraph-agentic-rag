from __future__ import annotations
import threading, time

class RateLimiter:
    def __init__(self, requests_per_second: float = 5.0):
        if requests_per_second <= 0 or requests_per_second > 10:
            raise ValueError("requests_per_second must be in (0, 10]")
        self.min_interval = 1.0 / requests_per_second
        self._last = 0.0
        self._lock = threading.Lock()

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            sleep_for = self.min_interval - (now - self._last)
            if sleep_for > 0:
                time.sleep(sleep_for)
            self._last = time.monotonic()
