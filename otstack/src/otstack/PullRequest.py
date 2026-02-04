from typing import Protocol


class PullRequest(Protocol):
    """Protocol defining the interface for a pull request."""

    title: str
    description: str | None
    source_branch: str
    destination_branch: str
    url: str

    def change_destination(self, new_destination: str) -> None:
        """Change the destination branch of this pull request."""
        ...
