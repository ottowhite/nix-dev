from dataclasses import dataclass

from .Repository import Repository


@dataclass
class PyGitHubRepository(Repository):
    """Concrete implementation of Repository."""

    name: str
    full_name: str
    description: str | None
    private: bool
    url: str
