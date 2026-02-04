from typing import Protocol

from .PullRequest import PullRequest


class Repository(Protocol):
    """Protocol defining the interface for a repository."""

    name: str
    full_name: str
    description: str | None
    private: bool
    url: str

    def get_open_pull_requests(self) -> list[PullRequest]:
        """Get all open pull requests for this repository."""
        ...

    def create_pr(
        self, source_branch: str, destination_branch: str, title: str
    ) -> PullRequest:
        """Create a pull request from source_branch to destination_branch."""
        ...
