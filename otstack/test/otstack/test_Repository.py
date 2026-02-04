import pytest

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
