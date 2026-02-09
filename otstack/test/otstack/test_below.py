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

    def test_raises_error_when_multiple_open_prs_for_current_branch(self) -> None:
        """below() raises ValueError when multiple open PRs exist for current branch."""
        current_branch = MockBranch(name="feature-branch")
        pr1 = _make_pr(source_branch="feature-branch", destination_branch="main")
        pr2 = _make_pr(source_branch="feature-branch", destination_branch="develop")
        repo = _make_repo(current_branch=current_branch, pull_requests=[pr1, pr2])
        client = _make_client(repos=[repo])

        with pytest.raises(
            ValueError, match="Multiple open PRs found for branch 'feature-branch'"
        ):
            client.below(
                repo=repo,
                new_branch_name="prep-work",
                pr_title="Preparatory refactor",
                worktree_path="/tmp/project-prep-work",
            )

    def test_raises_error_when_new_branch_already_exists(self) -> None:
        """below() raises ValueError when new branch name already exists."""
        current_branch = MockBranch(name="feature-branch")
        pr = _make_pr(source_branch="feature-branch", destination_branch="main")
        existing_branch = MockBranch(name="prep-work")
        repo = _make_repo(
            current_branch=current_branch,
            pull_requests=[pr],
            branches=[existing_branch],
        )
        client = _make_client(repos=[repo])

        with pytest.raises(ValueError, match="Branch 'prep-work' already exists"):
            client.below(
                repo=repo,
                new_branch_name="prep-work",
                pr_title="Preparatory refactor",
                worktree_path="/tmp/project-prep-work",
            )

    def test_raises_error_when_worktree_path_already_exists(self, tmp_path) -> None:
        """below() raises ValueError when worktree path already exists."""
        current_branch = MockBranch(name="feature-branch")
        pr = _make_pr(source_branch="feature-branch", destination_branch="main")
        repo = _make_repo(current_branch=current_branch, pull_requests=[pr])
        client = _make_client(repos=[repo])
        existing_path = tmp_path / "existing-dir"
        existing_path.mkdir()

        with pytest.raises(ValueError, match="Path .* already exists"):
            client.below(
                repo=repo,
                new_branch_name="prep-work",
                pr_title="Preparatory refactor",
                worktree_path=str(existing_path),
            )

    def test_creates_new_branch_from_original_destination(self, tmp_path) -> None:
        """below() creates new branch at the same commit as original PR destination."""
        current_branch = MockBranch(name="feature-branch")
        main_branch = MockBranch(name="main")
        pr = _make_pr(
            source_branch="feature-branch",
            destination_branch="main",
            destination_branch_obj=main_branch,
        )
        repo = _make_repo(current_branch=current_branch, pull_requests=[pr])
        client = _make_client(repos=[repo])
        worktree_path = str(tmp_path / "new-worktree")

        client.below(
            repo=repo,
            new_branch_name="prep-work",
            pr_title="Preparatory refactor",
            worktree_path=worktree_path,
        )

        # Verify the new branch was created from main
        assert len(repo.created_branches) == 1
        branch_name, from_branch = repo.created_branches[0]
        assert branch_name == "prep-work"
        assert from_branch.name == "main"

    def test_creates_worktree_for_new_branch(self, tmp_path) -> None:
        """below() creates a git worktree for the new branch."""
        current_branch = MockBranch(name="feature-branch")
        pr = _make_pr(source_branch="feature-branch", destination_branch="main")
        repo = _make_repo(current_branch=current_branch, pull_requests=[pr])
        client = _make_client(repos=[repo])
        worktree_path = str(tmp_path / "new-worktree")

        client.below(
            repo=repo,
            new_branch_name="prep-work",
            pr_title="Preparatory refactor",
            worktree_path=worktree_path,
        )

        # Verify worktree was created
        assert len(repo.created_worktrees) == 1
        branch, path = repo.created_worktrees[0]
        assert branch.name == "prep-work"
        assert path == worktree_path

    def test_pushes_new_branch_to_origin(self, tmp_path) -> None:
        """below() pushes the new branch to origin."""
        current_branch = MockBranch(name="feature-branch")
        pr = _make_pr(source_branch="feature-branch", destination_branch="main")
        repo = _make_repo(current_branch=current_branch, pull_requests=[pr])
        client = _make_client(repos=[repo])
        worktree_path = str(tmp_path / "new-worktree")

        client.below(
            repo=repo,
            new_branch_name="prep-work",
            pr_title="Preparatory refactor",
            worktree_path=worktree_path,
        )

        # Verify push was called on the new branch
        assert len(repo.created_branches) == 1
        new_branch = repo.created_worktrees[0][0]  # Get the branch from worktree
        assert new_branch.push_called is True

    def test_creates_pr_from_new_branch_to_original_destination(self, tmp_path) -> None:
        """below() creates a PR from new branch to original destination."""
        current_branch = MockBranch(name="feature-branch")
        main_branch = MockBranch(name="main")
        pr = _make_pr(
            source_branch="feature-branch",
            destination_branch="main",
            destination_branch_obj=main_branch,
        )
        repo = _make_repo(current_branch=current_branch, pull_requests=[pr])
        client = _make_client(repos=[repo])
        worktree_path = str(tmp_path / "new-worktree")

        client.below(
            repo=repo,
            new_branch_name="prep-work",
            pr_title="Preparatory refactor",
            worktree_path=worktree_path,
        )

        # Verify new PR was created
        assert len(repo.created_prs) == 1
        source, destination, title = repo.created_prs[0]
        assert source.name == "prep-work"
        assert destination.name == "main"
        assert title == "Preparatory refactor"


# Test helpers


def _make_client(repos: list[MockRepository]) -> OtStackClient:
    """Create an OtStackClient with the given repos."""
    mock_client = MockGitHubClient(repos=repos)
    return OtStackClient(github_client=mock_client)


def _make_repo(
    current_branch: MockBranch | None = None,
    pull_requests: list[MockPullRequest] | None = None,
    has_uncommitted_changes: bool = False,
    branches: list[MockBranch] | None = None,
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
        _branches=branches or [],
    )


def _make_pr(
    source_branch: str,
    destination_branch: str,
    title: str = "Test PR",
    destination_branch_obj: MockBranch | None = None,
) -> MockPullRequest:
    """Create a MockPullRequest with the given branches."""
    return MockPullRequest(
        title=title,
        description=None,
        source_branch=MockBranch(name=source_branch),
        destination_branch=destination_branch_obj or MockBranch(name=destination_branch),
        url="https://github.com/test-user/test-repo/pull/1",
    )
