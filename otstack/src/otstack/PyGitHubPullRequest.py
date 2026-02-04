from dataclasses import dataclass

from .PullRequest import PullRequest


@dataclass
class PyGitHubPullRequest(PullRequest):
    """Concrete implementation of PullRequest."""

    title: str
    description: str | None
    source_branch: str
    destination_branch: str
    url: str
