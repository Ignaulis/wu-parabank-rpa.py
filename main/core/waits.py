import time
from typing import Callable, Optional, TypeVar

T = TypeVar("T")


# Laukia kol salyga taps tenkinama arba baigsis laikas
def wait_until(
    timeout_ms: int,
    poll_interval_s: float,
    condition_fn: Callable[[], Optional[T]],
    on_timeout: Optional[Callable[[], T]] = None,
) -> Optional[T]:
    deadline = time.monotonic() + (timeout_ms / 1000)
    while time.monotonic() < deadline:
        result = condition_fn()
        if result is not None:
            return result
        time.sleep(poll_interval_s)

    return on_timeout() if on_timeout is not None else None

