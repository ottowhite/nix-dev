from dataclasses import dataclass

from otstack.GitHubClient import GitHubClient
from otstack.OtStackClient import OtStackClient
from otstack.PullRequest import PullRequest
from otstack.Repository import Repository


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


# Helpers and type definitions


@dataclass
class MockPullRequest(PullRequest):
    title: str
    description: str | None
    source_branch: str
    destination_branch: str
    url: str


@dataclass
class MockRepository(Repository):
    name: str
    full_name: str
    description: str | None
    private: bool
    url: str

    def get_open_pull_requests(self) -> list[PullRequest]:
        return []

    def create_pr(
        self, source_branch: str, destination_branch: str, title: str
    ) -> PullRequest:
        return MockPullRequest(
            title=title,
            description=None,
            source_branch=source_branch,
            destination_branch=destination_branch,
            url=f"{self.url}/pull/1",
        )


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
