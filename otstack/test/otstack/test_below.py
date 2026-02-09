import pytest

from otstack.OtStackClient import OtStackClient

from .helpers.MockBranch import MockBranch
from .helpers.MockGitHubClient import MockGitHubClient
from .helpers.MockPullRequest import MockPullRequest
from .helpers.MockRepository import MockRepository


class TestBelow:
    def test_raises_error_when_in_detached_head_state(self) -> None:
        """below() raises ValueError when in detached HEAD state."""
        repo = _make_repo(current_branch=None)
        client = _make_client(repos=[repo])

        with pytest.raises(ValueError, match="You are in detached HEAD state"):
            client.below(
                repo=repo,
                new_branch_name="prep-work",
                pr_title="Preparatory refactor",
                worktree_path="/tmp/project-prep-work",
            )

    def test_raises_error_when_uncommitted_changes_exist(self) -> None:
        """below() raises ValueError when there are uncommitted changes."""
        current_branch = MockBranch(name="feature-branch")
        repo = _make_repo(current_branch=current_branch, has_uncommitted_changes=True)
        client = _make_client(repos=[repo])

        with pytest.raises(ValueError, match="You have uncommitted changes"):
            client.below(
                repo=repo,
                new_branch_name="prep-work",
                pr_title="Preparatory refactor",
                worktree_path="/tmp/project-prep-work",
            )

    def test_raises_error_when_no_open_pr_for_current_branch(self) -> None:
        """below() raises ValueError when no open PR exists for current branch."""
        current_branch = MockBranch(name="feature-branch")
        repo = _make_repo(current_branch=current_branch, pull_requests=[])
        client = _make_client(repos=[repo])

        with pytest.raises(
            ValueError, match="No open PR found for branch 'feature-branch'"
        ):
            client.below(
                repo=repo,
                new_branch_name="prep-work",
                pr_title="Preparatory refactor",
                worktree_path="/tmp/project-prep-work",
            )


# Test helpers


def _make_client(repos: list[MockRepository]) -> OtStackClient:
    """Create an OtStackClient with the given repos."""
    mock_client = MockGitHubClient(repos=repos)
    return OtStackClient(github_client=mock_client)


def _make_repo(
    current_branch: MockBranch | None = None,
    pull_requests: list[MockPullRequest] | None = None,
    has_uncommitted_changes: bool = False,
    name: str = "test-repo",
) -> MockRepository:
    """Create a MockRepository with configurable current branch."""
    return MockRepository(
        name=name,
        full_name=f"test-user/{name}",
        description="Test repository",
        private=False,
        url=f"https://github.com/test-user/{name}",
        _pull_requests=pull_requests or [],
        _current_branch=current_branch,
        _has_uncommitted_changes=has_uncommitted_changes,
    )
