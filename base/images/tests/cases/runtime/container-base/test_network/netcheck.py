# SPDX-License-Identifier: MIT
"""Outbound HTTPS fetch + parse helpers, run inside the container to validate networking."""

from __future__ import annotations

import re
import time
import urllib.request
from urllib.error import HTTPError, URLError

WEATHER_URLS = (
    "https://iotadbselfhostreportstor.blob.core.windows.net/marinerextendedtests/mockweathergov.html",
    "https://forecast.weather.gov/MapClick.php?lat=47.6786&lon=-122.1316",
)
REPO_CONFIG_URLS = (
    "https://packages.microsoft.com/azurelinux/3.0/prod/base/x86_64/config.repo",
    "https://packages.microsoft.com/cbl-mariner/2.0/prod/base/x86_64/config.repo",
)


def fetch(url: str, retries: int = 4) -> str:
    """Fetch a URL, retrying transient HTTP errors with backoff."""
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url)) as resp:
                return resp.read().decode()
        except HTTPError:
            time.sleep(attempt * 2)
        except URLError:
            break
    return ""


def fetch_first(urls: tuple[str, ...]) -> str:
    """Return the first non-empty page across the given URLs."""
    for url in urls:
        page = fetch(url)
        if page:
            return page
    return ""


def substring_between(source: str, before: str, after: str) -> str:
    """Return the markup-stripped text between two markers, or empty string."""
    beg = source.find(before)
    if beg < 0:
        return ""
    sub = source[beg + len(before):]
    end = sub.find(after)
    if end >= 0:
        sub = sub[:end]
    return re.sub(r"<.*?>", "", sub).strip()


def verify_weather(strict: bool = True) -> bool:
    """Fetch Redmond weather; strict requires all forecast fields present."""
    page = fetch_first(WEATHER_URLS)
    visibility = substring_between(page, "<b>Visibility</b></td>", "</td>")
    dewpoint = substring_between(page, "<b>Dewpoint</b></td>", "</td>")
    humidity = substring_between(page, "<b>Humidity</b></td>", "</td>")
    wind = substring_between(page, "<b>Wind Speed</b></td>", "</td>")
    forecast = substring_between(page, 'alt="Today:', '"')
    print(f"weather: bytes={len(page)} humidity={humidity!r} wind={wind!r} visibility={visibility!r} dewpoint={dewpoint!r} forecast={forecast!r}")
    if not (wind and humidity and visibility and dewpoint) and strict:
        return False
    return len(page) > 0


def verify_sustained_https(iterations: int = 50, strict: bool = True) -> bool:
    """Repeat repo-config fetch; strict requires name+enabled fields each time."""
    for i in range(iterations):
        page = fetch_first(REPO_CONFIG_URLS)
        name = substring_between(page, "name", "\n")
        enabled = substring_between(page, "enabled", "\n")
        print(f"fetch {i + 1}/{iterations}: bytes={len(page)} name={name!r} enabled={enabled!r}")
        if not (name and enabled) and strict:
            return False
        if len(page) == 0:
            return False
        time.sleep(1)
    return True


if __name__ == "__main__":
    import sys

    checks = {"weather": verify_weather, "sustained": verify_sustained_https}
    strict = "--strict" in sys.argv
    sys.exit(0 if checks[sys.argv[1]](strict=strict) else 1)
