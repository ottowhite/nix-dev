from typing import Protocol
from dataclasses import dataclass
from github import Github, Auth


@dataclass
class Repository:
    name: str
    full_name: str
    description: str | None
    private: bool
    url: str


class GitHubClient(Protocol):
    """Protocol defining the high-level interface for GitHub operations."""

    def get_user_repos(self) -> list[Repository]:
        """Get all repositories for the authenticated user."""
        ...

    def get_authenticated_user_login(self) -> str:
        """Get the login name of the authenticated user."""
        ...

    def close(self) -> None:
        """Close the client and release resources."""
        ...


class PyGitHubClient:
    """Concrete implementation of GitHubClient using PyGithub."""

    def __init__(self, access_token: str) -> None:
        auth = Auth.Token(access_token)
        self._github = Github(auth=auth)

    def get_user_repos(self) -> list[Repository]:
        """Get all repositories for the authenticated user."""
        repos = []
        for repo in self._github.get_user().get_repos():
            repos.append(
                Repository(
                    name=repo.name,
                    full_name=repo.full_name,
                    description=repo.description,
                    private=repo.private,
                    url=repo.html_url,
                )
            )
        return repos

    def get_authenticated_user_login(self) -> str:
        """Get the login name of the authenticated user."""
        return self._github.get_user().login

    def close(self) -> None:
        """Close the client and release resources."""
        self._github.close()
