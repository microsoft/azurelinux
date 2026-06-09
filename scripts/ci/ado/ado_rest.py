"""Minimal Azure DevOps REST client for pipeline helper scripts.

Standard-library only (``urllib``) so it can run in any pipeline step without a
prior ``pip install`` — including before the dependency-install step. It
authenticates with the pipeline's build-identity OAuth token
(``System.AccessToken``), which the Azure DevOps control-plane REST API accepts
directly as a bearer token.

This talks to the ADO control plane (the pipeline's own build history), **not**
to Azure Resource Manager or Control Tower, so the Workload Identity Federation
service-connection rule that governs those calls does not apply here. The build
identity is the correct least-privilege caller for reading builds of the
definition it belongs to.

Reusable surface (intended to grow as more pipelines need ADO REST):
    * :class:`AdoConnection` — collection URI + project + token, with
      :meth:`AdoConnection.from_env`.
    * :func:`get_json` — authenticated GET with bounded retry on transient
      errors.
    * :func:`list_builds` — typed wrapper over ``GET /_apis/build/builds``.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

# ADO REST API version. Pinned (no floating version) per pipeline security
# rules; bump deliberately when a newer contract is required.
_API_VERSION = "7.1"

# HTTP status codes worth retrying: rate-limiting plus transient gateway/5xx.
_RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})

# Required ADO predefined variables for AdoConnection.from_env().
_ENV_COLLECTION_URI = "SYSTEM_COLLECTIONURI"
_ENV_PROJECT = "SYSTEM_TEAMPROJECT"
_ENV_TOKEN = "SYSTEM_ACCESSTOKEN"  # noqa: S105 — env var NAME, not a secret value


class AdoRestError(RuntimeError):
    """Raised when an ADO REST call fails or returns an unexpected payload."""


@dataclass(frozen=True)
class AdoConnection:
    """Connection parameters for the Azure DevOps REST API."""

    collection_uri: str
    """Organization/collection base URL, e.g. ``https://dev.azure.com/org/``."""

    project: str
    """Team project name or id."""

    token: str
    """Bearer token; the pipeline's ``System.AccessToken``."""

    @classmethod
    def from_env(cls) -> AdoConnection:
        """Build a connection from the standard ADO predefined variables.

        Reads ``SYSTEM_COLLECTIONURI``, ``SYSTEM_TEAMPROJECT`` and
        ``SYSTEM_ACCESSTOKEN`` from the environment.

        Returns:
            The populated :class:`AdoConnection`.

        Raises:
            AdoRestError: If any required variable is missing or empty.
        """
        missing = [name for name in (_ENV_COLLECTION_URI, _ENV_PROJECT, _ENV_TOKEN) if not os.environ.get(name)]
        if missing:
            msg = (
                "Missing required ADO environment variable(s): "
                f"{', '.join(missing)}. Ensure the job has 'Allow scripts to "
                "access the OAuth token' enabled and that these are exported in "
                "the step's env: block."
            )
            raise AdoRestError(msg)
        return cls(
            collection_uri=os.environ[_ENV_COLLECTION_URI],
            project=os.environ[_ENV_PROJECT],
            token=os.environ[_ENV_TOKEN],
        )


def get_json(
    conn: AdoConnection,
    path: str,
    query: dict[str, str] | None = None,
    *,
    max_attempts: int = 4,
    backoff_seconds: float = 1.0,
) -> dict[str, object]:
    """GET ``{collection}/{project}/{path}`` and return the parsed JSON object.

    The ``api-version`` query parameter is injected automatically. Transient
    failures (the statuses in :data:`_RETRY_STATUSES` and connection errors)
    are retried up to ``max_attempts`` times with linear backoff.

    Args:
        conn: The ADO connection to use.
        path: API path under the project, e.g. ``_apis/build/builds``.
        query: Extra query parameters.
        max_attempts: Maximum number of attempts before giving up.
        backoff_seconds: Base delay multiplied by the attempt number.

    Returns:
        The response body parsed as a JSON object.

    Raises:
        AdoRestError: On a non-retryable HTTP error, exhausted retries, a
            non-HTTPS URL, or a body that is not a JSON object.
    """
    params = dict(query or {})
    params["api-version"] = _API_VERSION

    base = conn.collection_uri.rstrip("/")
    project = urllib.parse.quote(conn.project, safe="")
    url = f"{base}/{project}/{path.lstrip('/')}?{urllib.parse.urlencode(params)}"

    if urllib.parse.urlsplit(url).scheme != "https":
        msg = f"Refusing to call a non-HTTPS ADO URL: {url}"
        raise AdoRestError(msg)

    headers = {"Authorization": f"Bearer {conn.token}", "Accept": "application/json"}

    last_error = ""
    for attempt in range(1, max_attempts + 1):
        request = urllib.request.Request(url, headers=headers, method="GET")  # noqa: S310 — scheme validated https above
        try:
            with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310 — scheme validated https above
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            if exc.code in _RETRY_STATUSES and attempt < max_attempts:
                last_error = f"HTTP {exc.code} {exc.reason}"
                time.sleep(backoff_seconds * attempt)
                continue
            msg = f"GET {url} failed: HTTP {exc.code} {exc.reason}"
            raise AdoRestError(msg) from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            if attempt < max_attempts:
                last_error = str(exc)
                time.sleep(backoff_seconds * attempt)
                continue
            msg = f"GET {url} failed after {max_attempts} attempts: {exc}"
            raise AdoRestError(msg) from exc

        try:
            data = json.loads(body)
        except json.JSONDecodeError as exc:
            msg = f"GET {url} returned a non-JSON body: {exc}"
            raise AdoRestError(msg) from exc
        if not isinstance(data, dict):
            msg = f"GET {url} returned a JSON {type(data).__name__}, expected an object."
            raise AdoRestError(msg)
        return data

    msg = f"GET {url} failed after {max_attempts} attempts: {last_error}"
    raise AdoRestError(msg)


def list_builds(
    conn: AdoConnection,
    *,
    definition_id: int,
    branch_name: str,
    top: int = 20,
    query_order: str = "queueTimeDescending",
) -> list[object]:
    """Return builds for one definition on ``branch_name``.

    Thin wrapper over ``GET /_apis/build/builds`` returning the raw ``value``
    array; callers filter and select. Entries are JSON objects but are typed as
    ``object`` so callers narrow them explicitly.

    Args:
        conn: The ADO connection to use.
        definition_id: Build definition (pipeline) id to filter by.
        branch_name: Full source branch ref, e.g. ``refs/heads/4.0``.
        top: Maximum number of builds to return.
        query_order: ADO ``queryOrder`` value (default most-recent first).

    Returns:
        The ``value`` array from the response.

    Raises:
        AdoRestError: If the response ``value`` field is not an array.
    """
    response = get_json(
        conn,
        "_apis/build/builds",
        {
            "definitions": str(definition_id),
            "branchName": branch_name,
            "$top": str(top),
            "queryOrder": query_order,
        },
    )
    value = response.get("value")
    if not isinstance(value, list):
        msg = "Unexpected ADO response: 'value' is not an array."
        raise AdoRestError(msg)
    return value
