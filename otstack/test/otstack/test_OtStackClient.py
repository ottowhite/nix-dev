from otstack.OtStackClient import OtStackClient

from .helpers.MockGitHubClient import MockGitHubClient
from .helpers.MockRepository import MockRepository


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
