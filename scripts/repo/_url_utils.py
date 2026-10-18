# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Shared repository URL validation."""

from __future__ import annotations

import urllib.request
from typing import TYPE_CHECKING
from urllib.parse import urlsplit

if TYPE_CHECKING:
    import ssl
    from http.client import HTTPMessage
    from typing import IO

ALLOWED_REPOSITORY_URL_SCHEMES = frozenset({"file", "http", "https"})


class _RepositoryRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Reject redirects to repository transports outside the allowlist."""

    def redirect_request(  # noqa: PLR0913, PLR0917 - signature overrides urllib
        self,
        req: urllib.request.Request,
        fp: IO[bytes],
        code: int,
        msg: str,
        headers: HTTPMessage,
        newurl: str,
    ) -> urllib.request.Request | None:
        """Validate the resolved redirect target before following it."""
        validate_repository_url(newurl, context="repository redirect URL")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def validate_repository_url(url: str, *, context: str = "repository URL") -> None:
    """Reject URL schemes that repository tools do not intentionally support."""
    scheme = urlsplit(url).scheme.lower()
    if scheme not in ALLOWED_REPOSITORY_URL_SCHEMES:
        allowed = ", ".join(sorted(ALLOWED_REPOSITORY_URL_SCHEMES))
        raise ValueError(
            f"{context} has unsupported scheme {scheme or '<missing>'!r}; "
            f"expected one of: {allowed}"
        )


def build_repository_url_opener(
    *, ssl_context: ssl.SSLContext | None = None
) -> urllib.request.OpenerDirector:
    """Build an opener that validates every repository redirect target."""
    handlers: list[urllib.request.BaseHandler] = [_RepositoryRedirectHandler()]
    if ssl_context is not None:
        handlers.append(urllib.request.HTTPSHandler(context=ssl_context))
    return urllib.request.build_opener(*handlers)
