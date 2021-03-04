"""Request info from GitHub API."""
from typing import Any, Dict, List

import attr
import deal
import requests


@attr.s(auto_attribs=True)
class Issue:
    """Issue from GitHub."""

    title: str
    body: str
    html_url: str

    @classmethod
    def from_dict(cls, dct: Dict[str, Any]) -> "Issue":
        """Create an issue from a dict obtained from GitHub API."""
        return cls(title=dct["title"], body=dct["body"], html_url=dct["html_url"])


class API:
    """GitHub API client."""

    def __init__(self, token: str) -> None:
        """Initialize a GitHub API client."""
        self.headers = dict(
            Accept="application/vnd.github.v3+json",
            Authorization=f"token {token}",
        )
        self.endpoint = "https://api.github.com"

    @deal.pre(lambda self, owner, repo: bool(owner) and bool(repo))
    @deal.pre(lambda self, owner, repo: "/" not in owner)
    @deal.pre(lambda self, owner, repo: "/" not in repo)
    @deal.post(
        lambda issues: all(issue.html_url.startswith("http") for issue in issues)
    )
    @deal.raises(requests.HTTPError)
    def list_issues(self, owner: str, repo: str) -> List[Issue]:
        """List all issues from a specific repository."""
        response = requests.get(
            f"{self.endpoint}/repos/{owner}/{repo}/issues", headers=self.headers
        )
        response.raise_for_status()
        return [Issue.from_dict(issue) for issue in response.json()]

    @deal.raises(requests.HTTPError)
    def create_issue(self, owner: str, repo: str, title: str, body: str) -> Issue:
        """Create an issue in a specific repository."""
        data = dict(title=title)
        if body is not None:
            data["body"] = body
        response = requests.post(
            f"{self.endpoint}/repos/{owner}/{repo}/issues",
            json=data,
            headers=self.headers,
        )
        response.raise_for_status()
        return Issue.from_dict(response.json())
