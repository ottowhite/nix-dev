from typing import Protocol


class Repository(Protocol):
    """Protocol defining the interface for a repository."""

    @property
    def name(self) -> str:
        """Repository name."""
        ...

    @property
    def full_name(self) -> str:
        """Full repository name (owner/repo)."""
        ...

    @property
    def description(self) -> str | None:
        """Repository description."""
        ...

    @property
    def private(self) -> bool:
        """Whether the repository is private."""
        ...

    @property
    def url(self) -> str:
        """Repository URL."""
        ...
