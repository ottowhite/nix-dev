from io import StringIO

from otstack.OtStackClient import OtStackClient
from otstack.PullRequest import PullRequest

from .helpers.MockBranch import MockBranch
from .helpers.MockGitHubClient import MockGitHubClient
from .helpers.MockPullRequest import MockPullRequest
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

    def test_single_pr_shows_simple_tree(self) -> None:
        pr = _make_pr(
            title="Add feature A",
            source_branch="feature-a",
            destination_branch="main",
        )
        repo = _make_repo(pull_requests=[pr])
        client, output = _make_client_with_output(repos=[repo])

        client.tree()

        expected = """\
main
└── feature-a (PR: "Add feature A")
"""
        assert output.getvalue() == expected


# Test helpers


def _make_client_with_output(
    repos: list[MockRepository],
) -> tuple[OtStackClient, StringIO]:
    """Create an OtStackClient with captured stdout."""
    mock_client = MockGitHubClient(repos=repos)
    output = StringIO()
    client = OtStackClient(github_client=mock_client, output=output)
    return client, output


def _make_repo(
    pull_requests: list[PullRequest],
    name: str = "test-repo",
) -> MockRepository:
    """Create a MockRepository with the given PRs."""
    return MockRepository(
        name=name,
        full_name=f"test-user/{name}",
        description="Test repository",
        private=False,
        url=f"https://github.com/test-user/{name}",
        _pull_requests=pull_requests,
    )


def _make_pr(
    title: str,
    source_branch: str,
    destination_branch: str,
) -> MockPullRequest:
    """Create a MockPullRequest with the given properties."""
    return MockPullRequest(
        title=title,
        description=None,
        source_branch=MockBranch(name=source_branch),
        destination_branch=MockBranch(name=destination_branch),
        url="https://github.com/test-user/test-repo/pull/1",
    )
