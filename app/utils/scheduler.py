from threading import Lock, Timer
from typing import Callable, Dict


_timers: Dict[str, Timer] = {}
_timer_lock = Lock()


def schedule(key: str, delay_seconds: int, callback: Callable[[], None]) -> None:
    with _timer_lock:
        existing = _timers.get(key)
        if existing is not None:
            existing.cancel()

        timer = Timer(delay_seconds, callback)
        timer.daemon = True
        _timers[key] = timer
        timer.start()


def cancel(key: str) -> None:
    with _timer_lock:
        existing = _timers.pop(key, None)
        if existing is not None:
            existing.cancel()
