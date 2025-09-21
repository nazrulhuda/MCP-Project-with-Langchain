from __future__ import annotations

import asyncio
import threading
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import psutil
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("SysInfo")


@dataclass
class Sample:
    timestamp: float
    cpu_percent: float
    memory_percent: float


class RollingMetrics:
    def __init__(self, max_seconds: int = 24 * 3600):
        self.max_seconds = max_seconds
        self._samples: List[Sample] = []
        self._lock = threading.Lock()

    def add_sample(self, sample: Sample) -> None:
        with self._lock:
            self._samples.append(sample)
            cutoff = time.time() - self.max_seconds
            # drop old samples
            idx = 0
            for i, s in enumerate(self._samples):
                if s.timestamp >= cutoff:
                    idx = i
                    break
            if idx > 0:
                self._samples = self._samples[idx:]

    def latest(self) -> Optional[Sample]:
        with self._lock:
            return self._samples[-1] if self._samples else None

    def at_or_before(self, when_epoch: float) -> Optional[Sample]:
        with self._lock:
            # binary search could be used; list expected small enough
            candidate: Optional[Sample] = None
            for s in self._samples:
                if s.timestamp <= when_epoch:
                    candidate = s
                else:
                    break
            return candidate


metrics = RollingMetrics()


def _sampler(stop_event: threading.Event, interval: float = 2.0) -> None:
    # prime cpu_percent measurement
    psutil.cpu_percent(interval=None)
    while not stop_event.is_set():
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        metrics.add_sample(Sample(time.time(), cpu, mem))
        stop_event.wait(interval)


stop_event = threading.Event()
sampler_thread = threading.Thread(target=_sampler, args=(stop_event,), daemon=True)
sampler_thread.start()


@mcp.tool()
async def get_cpu_now() -> str:
    """Return current system CPU utilization percentage as a human string."""
    s = metrics.latest()
    if not s:
        # fallback direct read
        val = psutil.cpu_percent(interval=0.1)
        return f"CPU utilization is approximately {val:.1f}% right now."
    return f"CPU utilization is approximately {s.cpu_percent:.1f}% right now."


@mcp.tool()
async def get_memory_now() -> str:
    """Return current system memory utilization percentage as a human string."""
    s = metrics.latest()
    if not s:
        val = psutil.virtual_memory().percent
        return f"Memory utilization is approximately {val:.1f}% right now."
    return f"Memory utilization is approximately {s.memory_percent:.1f}% right now."


@mcp.tool()
async def get_cpu_at(timestamp_iso: str) -> str:
    """Return CPU utilization near a specific time.

    Provide an ISO 8601 like '2025-09-17 22:00:00' or '2025-09-17T22:00:00' in local time.
    Returns the closest sample at or before that time within the rolling window.
    """
    when_epoch = _parse_local_timestamp_to_epoch(timestamp_iso)
    s = metrics.at_or_before(when_epoch)
    if not s:
        return "No CPU sample available at or before the requested time."
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(s.timestamp))
    return f"CPU utilization at {ts} was approximately {s.cpu_percent:.1f}%."


@mcp.tool()
async def get_memory_at(timestamp_iso: str) -> str:
    """Return Memory utilization near a specific time.

    Provide an ISO 8601 like '2025-09-17 22:00:00' or '2025-09-17T22:00:00' in local time.
    Returns the closest sample at or before that time within the rolling window.
    """
    when_epoch = _parse_local_timestamp_to_epoch(timestamp_iso)
    s = metrics.at_or_before(when_epoch)
    if not s:
        return "No Memory sample available at or before the requested time."
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(s.timestamp))
    return f"Memory utilization at {ts} was approximately {s.memory_percent:.1f}%."


def _parse_local_timestamp_to_epoch(s: str) -> float:
    s = s.strip().replace("T", " ")
    # best-effort parse: 'YYYY-mm-dd HH:MM:SS'
    try:
        tm = time.strptime(s, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        # try minute precision
        tm = time.strptime(s, "%Y-%m-%d %H:%M")
    return time.mktime(tm)


if __name__ == "__main__":
    try:
        # Run over stdio so we can co-exist with the weather HTTP server
        mcp.run(transport="stdio")
    finally:
        stop_event.set()

