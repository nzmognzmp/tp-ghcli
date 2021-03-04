import os
from typing import Any, Dict

import pytest
import requests

from ghcli.api import API


@pytest.fixture
def api() -> API:
    return API(os.environ["GITHUB_TOKEN"])


@pytest.fixture
def bad_token_api() -> API:
    return API("bad_token")


def test_list_issues_result_type(api: API) -> None:
    result = api.list_issues("m09", "tp-github-cli")
    assert isinstance(result, list)


def test_list_issues_html_url(api: API) -> None:
    issues = api.list_issues("m09", "tp-github-cli")
    assert all("tp-github-cli" in issue.html_url for issue in issues)


def test_list_issues_404(api: API) -> None:
    with pytest.raises(requests.HTTPError):
        api.list_issues("m09", "i-do-not-exist")


def test_create_issue(monkeypatch: Any, api: API) -> None:
    class FakePost:
        def __init__(
            self,
            url: str,
            headers: Dict[str, str],
            json: Any,
            *args: Any,
            **kwargs: Any
        ):
            if args:
                raise ValueError("Too many positional args")
            if kwargs:
                raise ValueError("Too many kw args")

        def raise_for_status(self) -> None:
            pass

        def json(self) -> Dict[str, str]:
            return dict(
                title="Issue title",
                body="Issue body",
                html_url="https://github.com/m09/tp-github-cli/issues/42",
            )

    monkeypatch.setattr(requests, "post", FakePost)
    issue = api.create_issue("m09", "tp-github-cli", "Issue title", "Issue body")
    assert issue.html_url == "https://github.com/m09/tp-github-cli/issues/42"


def test_create_issues_404(api: API) -> None:
    with pytest.raises(requests.HTTPError):
        api.create_issue("m09", "i-do-not-exist", "Issue title", "Issue body")


def test_create_issue_bad_token(bad_token_api: API) -> None:
    with pytest.raises(requests.HTTPError):
        bad_token_api.create_issue("m09", "tp-github-cli", "Issue title", "Issue body")
