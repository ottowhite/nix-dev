import pytest
from git import Repo

from otstack.LocalBranch import LocalBranch
from otstack.PyGitHubRepository import PyGitHubRepository
from otstack.Repository import Repository

from .helpers.MockBranch import MockBranch
from .helpers.MockRepository import MockRepository


class TestRepositoryGetLocalBranches:
    def test_repository_protocol_has_get_local_branches_method(self) -> None:
        """Repository protocol defines get_local_branches() method."""
        repo: Repository = _make_repo(local_branches=[])

        result = repo.get_local_branches()

        assert result == []

    def test_mock_repository_returns_configured_local_branches(self) -> None:
        """MockRepository returns the configured _local_branches value."""
        branch1 = MockBranch(name="feature-1", _is_local=True)
        branch2 = MockBranch(name="feature-2", _is_local=True)
        repo = _make_repo(local_branches=[branch1, branch2])

        result = repo.get_local_branches()

        assert result == [branch1, branch2]

    def test_mock_repository_raises_value_error_when_no_git_repo(self) -> None:
        """MockRepository.get_local_branches() raises ValueError when no git repo."""
        repo = _make_repo(local_branches=None)

        with pytest.raises(ValueError, match="No local git repository"):
            repo.get_local_branches()


class TestPyGitHubRepositoryGetLocalBranches:
    def test_raises_value_error_when_no_git_repo(self) -> None:
        """PyGitHubRepository.get_local_branches() raises ValueError when _git_repo is None."""
        repo = _make_pygithub_repo(git_repo=None)

        with pytest.raises(ValueError, match="No local git repository"):
            repo.get_local_branches()

    def test_returns_main_repo_current_branch(self, tmp_path) -> None:
        """Returns the branch currently checked out in the main repo."""
        git_repo = Repo.init(tmp_path)
        (tmp_path / "file.txt").write_text("content")
        git_repo.index.add(["file.txt"])
        git_repo.index.commit("Initial commit")
        repo = _make_pygithub_repo(git_repo=git_repo)

        result = repo.get_local_branches()

        assert len(result) == 1
        assert result[0].name == "master"
        assert isinstance(result[0], LocalBranch)
        assert result[0].is_local() is True

    def test_returns_worktree_branches(self, tmp_path) -> None:
        """Returns branches checked out in worktrees."""
        main_path = tmp_path / "main"
        main_path.mkdir()
        git_repo = Repo.init(main_path)
        (main_path / "file.txt").write_text("content")
        git_repo.index.add(["file.txt"])
        git_repo.index.commit("Initial commit")

        # Create a feature branch
        git_repo.git.branch("feature-1")

        # Create a worktree for the feature branch
        worktree_path = tmp_path / "worktree-feature-1"
        git_repo.git.worktree("add", str(worktree_path), "feature-1")

        repo = _make_pygithub_repo(git_repo=git_repo)

        result = repo.get_local_branches()

        branch_names = {b.name for b in result}
        assert "master" in branch_names
        assert "feature-1" in branch_names
        assert len(result) == 2
        for branch in result:
            assert isinstance(branch, LocalBranch)


# Test helpers


def _make_repo(
    local_branches: list[MockBranch] | None,
) -> MockRepository:
    """Create a MockRepository with specified local branches."""
    return MockRepository(
        name="test-repo",
        full_name="test-user/test-repo",
        description="Test repository",
        private=False,
        url="https://github.com/test-user/test-repo",
        _local_branches=local_branches,
    )


def _make_pygithub_repo(
    git_repo: Repo | None,
) -> PyGitHubRepository:
    """Create a PyGitHubRepository with specified git repo."""
    return PyGitHubRepository(
        name="test-repo",
        full_name="test-user/test-repo",
        description="Test repository",
        private=False,
        url="https://github.com/test-user/test-repo",
        _git_repo=git_repo,
    )
