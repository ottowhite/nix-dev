from dataclasses import dataclass

from otstack.GitHubClient import GitHubClient
from otstack.OtStackClient import OtStackClient
from otstack.Repository import Repository


@dataclass
class MockRepository(Repository):
    name: str
    full_name: str
    description: str | None
    private: bool
    url: str


class MockGitHubClient(GitHubClient):
    def __init__(self, repos: list[Repository] | None = None) -> None:
        self._repos = repos or []
        self._closed = False

    def get_user_repos(self) -> list[Repository]:
        return self._repos

    def get_authenticated_user_login(self) -> str:
        return "test-user"

    def close(self) -> None:
        self._closed = True


def test_otstack_client_uses_injected_github_client() -> None:
    mock_repos = [
        MockRepository(
            name="test-repo",
            full_name="test-user/test-repo",
            description="A test repository",
            private=False,
            url="https://github.com/test-user/test-repo",
        )
    ]
    mock_client = MockGitHubClient(repos=mock_repos)

    client = OtStackClient(github_client=mock_client)

    repos = client.github.get_user_repos()
    assert len(repos) == 1
    assert repos[0].name == "test-repo"


def test_otstack_client_context_manager_closes_github_client() -> None:
    mock_client = MockGitHubClient()

    with OtStackClient(github_client=mock_client) as client:
        _ = client.github.get_authenticated_user_login()

    assert mock_client._closed is True
