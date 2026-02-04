from typing import Protocol


class Repository(Protocol):
    """Protocol defining the interface for a repository."""

    name: str
    full_name: str
    description: str | None
    private: bool
    url: str
