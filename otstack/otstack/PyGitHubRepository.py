from dataclasses import dataclass


@dataclass
class PyGitHubRepository:
    """Concrete implementation of Repository."""

    name: str
    full_name: str
    description: str | None
    private: bool
    url: str
