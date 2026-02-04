from io import StringIO

from otstack.OtStackClient import OtStackClient
from otstack.PullRequest import PullRequest
from otstack.Repository import Repository

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


def test_get_repo_returns_repository_by_name() -> None:
    repo = MockRepository(
        name="test-repo",
        full_name="test-user/test-repo",
        description="A test repository",
        private=False,
        url="https://github.com/test-user/test-repo",
    )
    mock_client = MockGitHubClient(repos=[repo])
    client = OtStackClient(github_client=mock_client)

    result = client.get_repo("test-user/test-repo")

    assert result.name == "test-repo"


class TestTree:
    def test_no_prs_returns_empty_output(self) -> None:
        repo = _make_repo(pull_requests=[])
        client, output = _make_client_with_output(repos=[repo])

        client.tree(repo)

        assert output.getvalue() == ""

    def test_single_pr_shows_simple_tree(self) -> None:
        pr = _make_pr(
            title="Add feature A",
            source_branch="feature-a",
            destination_branch="main",
        )
        repo = _make_repo(pull_requests=[pr])
        client, output = _make_client_with_output(repos=[repo])

        client.tree(repo)

        expected = """\
main
└── feature-a (PR: "Add feature A")
"""
        assert output.getvalue() == expected

    def test_multiple_independent_prs_to_same_base(self) -> None:
        pr1 = _make_pr(
            title="Add feature A",
            source_branch="feature-a",
            destination_branch="main",
        )
        pr2 = _make_pr(
            title="Add feature C",
            source_branch="feature-c",
            destination_branch="main",
        )
        repo = _make_repo(pull_requests=[pr1, pr2])
        client, output = _make_client_with_output(repos=[repo])

        client.tree(repo)

        expected = """\
main
├── feature-a (PR: "Add feature A")
└── feature-c (PR: "Add feature C")
"""
        assert output.getvalue() == expected

    def test_chained_prs_show_nested_tree(self) -> None:
        """PR feature-b depends on feature-a which depends on main."""
        pr1 = _make_pr(
            title="Add feature A",
            source_branch="feature-a",
            destination_branch="main",
        )
        pr2 = _make_pr(
            title="Add feature B",
            source_branch="feature-b",
            destination_branch="feature-a",
        )
        repo = _make_repo(pull_requests=[pr1, pr2])
        client, output = _make_client_with_output(repos=[repo])

        client.tree(repo)

        expected = """\
main
└── feature-a (PR: "Add feature A")
    └── feature-b (PR: "Add feature B")
"""
        assert output.getvalue() == expected

    def test_complex_dag_with_multiple_chains(self) -> None:
        """
        Complex DAG structure:
        main
        ├── feature-a
        │   └── feature-b
        └── feature-c
        """
        pr_a = _make_pr(
            title="Add feature A",
            source_branch="feature-a",
            destination_branch="main",
        )
        pr_b = _make_pr(
            title="Add feature B",
            source_branch="feature-b",
            destination_branch="feature-a",
        )
        pr_c = _make_pr(
            title="Add feature C",
            source_branch="feature-c",
            destination_branch="main",
        )
        repo = _make_repo(pull_requests=[pr_a, pr_b, pr_c])
        client, output = _make_client_with_output(repos=[repo])

        client.tree(repo)

        expected = """\
main
├── feature-a (PR: "Add feature A")
│   └── feature-b (PR: "Add feature B")
└── feature-c (PR: "Add feature C")
"""
        assert output.getvalue() == expected


# Test helpers


def _make_client_with_output(
    repos: list[Repository],
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
