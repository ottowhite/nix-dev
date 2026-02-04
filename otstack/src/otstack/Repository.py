from typing import Protocol

from .Branch import Branch
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
        self, source_branch: Branch, destination_branch: Branch, title: str
    ) -> PullRequest:
        """Create a pull request from source_branch to destination_branch."""
        ...

    def get_branches(self) -> list[Branch]:
        """Get all branches in this repository."""
        ...

    def get_local_branches(self) -> list[Branch]:
        """
        Get all branches with local filesystem checkouts (main repo and worktrees).

        Raises ValueError if no local git repository is associated.
        Invariant: No two branches in the returned list have the same name.
        """
        ...
