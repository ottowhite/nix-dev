from io import StringIO

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


class TestTree:
    def test_no_repos_returns_empty_output(self) -> None:
        client, output = _make_client_with_output(repos=[])

        client.tree()

        assert output.getvalue() == ""


# Test helpers


def _make_client_with_output(
    repos: list[MockRepository],
) -> tuple[OtStackClient, StringIO]:
    """Create an OtStackClient with captured stdout."""
    mock_client = MockGitHubClient(repos=repos)
    output = StringIO()
    client = OtStackClient(github_client=mock_client, output=output)
    return client, output
