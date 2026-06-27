"""Browser-behaviour classifier.

An ordinary effect component should not need cookies, persistent storage,
clipboard, geolocation, camera, microphone, service workers, persistent
WebSockets, analytics or remote executable scripts. Any such capability is
flagged for explicit justification (security/network-policy.yml).
"""
from __future__ import annotations
import re
import pathlib
from . import Finding

CAPABILITIES: list[tuple[str, str, str, str]] = [
    ("cookies", "warn", r"document\.cookie", "Reads/writes cookies"),
    ("localstorage", "warn", r"\b(?:local|session)Storage\b", "Uses local/session storage"),
    ("clipboard", "warn", r"navigator\.clipboard|execCommand\(\s*['\"]copy", "Clipboard access"),
    ("geolocation", "high", r"navigator\.geolocation", "Geolocation access"),
    ("camera-mic", "high", r"getUserMedia|navigator\.mediaDevices", "Camera/microphone access"),
    ("service-worker", "high", r"serviceWorker\.register", "Registers a service worker"),
    ("websocket", "warn", r"new\s+WebSocket\b", "Opens a WebSocket"),
    ("analytics", "warn", r"google-analytics|gtag\(|mixpanel|segment\.com|posthog", "Analytics/telemetry endpoint"),
    ("notifications", "warn", r"Notification\.requestPermission", "Requests notification permission"),
    ("beacon", "warn", r"navigator\.sendBeacon", "sendBeacon telemetry"),
]

_COMPILED = [(c, s, re.compile(p), m) for c, s, p, m in CAPABILITIES]
_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".html"}


def scan_text(text: str, path: str = "") -> list[Finding]:
    out: list[Finding] = []
    for i, line in enumerate(text.splitlines(), 1):
        for code, sev, rx, msg in _COMPILED:
            if rx.search(line):
                out.append(Finding("behaviour_scanner", sev, code, msg, path, i))
    return out


def scan_path(target: str | pathlib.Path) -> list[Finding]:
    p = pathlib.Path(target)
    out: list[Finding] = []
    files = [p] if p.is_file() else [f for f in p.rglob("*") if f.is_file()]
    for f in files:
        if f.suffix.lower() not in _EXT:
            continue
        try:
            out.extend(scan_text(f.read_text(errors="replace"), str(f)))
        except OSError:
            continue
    return out
