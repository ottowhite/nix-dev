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


class TestGetPrTree:
    def test_returns_tree_with_no_children_when_no_prs_target_branch(self) -> None:
        """When no PRs target the given branch, return a tree with empty children."""
        repo = _make_repo(pull_requests=[])
        client = _make_client(repos=[repo])

        tree = client.get_pr_tree(repo, "main")

        assert tree.branch_name == "main"
        assert tree.pull_request is None
        assert tree.children == []

    def test_returns_tree_with_child_for_pr_targeting_branch(self) -> None:
        """When a PR targets the given branch, return a tree with that PR as a child."""
        pr = _make_pr(
            title="Add feature A",
            source_branch="feature-a",
            destination_branch="main",
        )
        repo = _make_repo(pull_requests=[pr])
        client = _make_client(repos=[repo])

        tree = client.get_pr_tree(repo, "main")

        assert tree.branch_name == "main"
        assert tree.pull_request is None
        assert len(tree.children) == 1
        child = tree.children[0]
        assert child.branch_name == "feature-a"
        assert child.pull_request == pr
        assert child.children == []

    def test_returns_nested_tree_for_chained_prs(self) -> None:
        """When PRs are chained, return a nested tree structure."""
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
        repo = _make_repo(pull_requests=[pr_a, pr_b])
        client = _make_client(repos=[repo])

        tree = client.get_pr_tree(repo, "main")

        # main -> feature-a -> feature-b
        assert tree.branch_name == "main"
        assert len(tree.children) == 1
        child_a = tree.children[0]
        assert child_a.branch_name == "feature-a"
        assert child_a.pull_request == pr_a
        assert len(child_a.children) == 1
        child_b = child_a.children[0]
        assert child_b.branch_name == "feature-b"
        assert child_b.pull_request == pr_b
        assert child_b.children == []

    def test_returns_multiple_children_for_multiple_prs_targeting_same_branch(
        self,
    ) -> None:
        """When multiple PRs target the same branch, all are included as children."""
        pr_a = _make_pr(
            title="Add feature A",
            source_branch="feature-a",
            destination_branch="main",
        )
        pr_b = _make_pr(
            title="Add feature B",
            source_branch="feature-b",
            destination_branch="main",
        )
        repo = _make_repo(pull_requests=[pr_a, pr_b])
        client = _make_client(repos=[repo])

        tree = client.get_pr_tree(repo, "main")

        assert tree.branch_name == "main"
        assert len(tree.children) == 2
        branch_names = {child.branch_name for child in tree.children}
        assert branch_names == {"feature-a", "feature-b"}


class TestTree:
    def test_no_prs_returns_empty_output(self) -> None:
        repo = _make_repo(pull_requests=[])
        client, output = _make_client_with_output(repos=[repo])

        client.tree(repo)

        assert output.getvalue() == ""

    def test_single_pr_shows_horizontal_tree(self) -> None:
        pr = _make_pr(
            title="Add feature A",
            source_branch="feature-a",
            destination_branch="main",
        )
        repo = _make_repo(pull_requests=[pr])
        client, output = _make_client_with_output(repos=[repo], terminal_width=60)

        client.tree(repo)

        # Content centered in 60-char width
        # feature-a: 9 chars, padding = (60-9)//2 = 25
        # "Add feature A": 15 chars, padding = (60-15)//2 = 22
        # |: 1 char, padding = (60-1)//2 = 29
        # main: 4 chars, padding = (60-4)//2 = 28
        expected = """\
                         feature-a
                      "Add feature A"
                             |
                            main
"""
        assert output.getvalue() == expected


# Test helpers


def _make_client(repos: list[Repository]) -> OtStackClient:
    """Create an OtStackClient with the given repos."""
    mock_client = MockGitHubClient(repos=repos)
    return OtStackClient(github_client=mock_client)


def _make_client_with_output(
    repos: list[Repository],
    terminal_width: int = 60,
) -> tuple[OtStackClient, StringIO]:
    """Create an OtStackClient with captured stdout."""
    mock_client = MockGitHubClient(repos=repos)
    output = StringIO()
    client = OtStackClient(
        github_client=mock_client, output=output, terminal_width=terminal_width
    )
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
