"""HTTP helpers for external APIs (urllib, no extra deps)."""
from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request

log = logging.getLogger("insurance.external")

DEFAULT_UA = "InsuranceLab/1.0 (educational; contact: lab@example.invalid)"


def http_get_json(url: str, *, timeout: float = 12.0) -> list | dict:
    req = urllib.request.Request(url, headers={"User-Agent": DEFAULT_UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        log.warning("HTTP error %s for %s", e.code, url)
        raise
    except urllib.error.URLError as e:
        log.warning("URL error for %s: %s", url, e)
        raise
    except TimeoutError:
        log.warning("Timeout for %s", url)
        raise
    return json.loads(body)
