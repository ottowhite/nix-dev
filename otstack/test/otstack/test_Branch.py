import pytest

from otstack.Branch import Branch
from otstack.LocalBranch import LocalBranch
from otstack.SimpleBranch import SimpleBranch

from .helpers.MockBranch import MockBranch


class TestBranchIsLocal:
    def test_branch_protocol_has_is_local_method(self) -> None:
        """Branch protocol defines is_local() method."""
        branch: Branch = MockBranch(name="test-branch", _is_local=True)

        result = branch.is_local()

        assert result is True

    def test_mock_branch_returns_configured_is_local_value(self) -> None:
        """MockBranch returns the configured _is_local value."""
        local_branch = MockBranch(name="local", _is_local=True)
        remote_branch = MockBranch(name="remote", _is_local=False)

        assert local_branch.is_local() is True
        assert remote_branch.is_local() is False


class TestSimpleBranchIsLocal:
    def test_simple_branch_is_local_returns_false(self) -> None:
        """SimpleBranch.is_local() always returns False."""
        branch = SimpleBranch(name="some-branch")

        result = branch.is_local()

        assert result is False


class TestLocalBranchIsLocal:
    def test_local_branch_is_local_returns_true(self, tmp_path) -> None:
        """LocalBranch.is_local() always returns True."""
        from git import Repo

        repo = Repo.init(tmp_path)
        branch = LocalBranch(name="main", _repo=repo)

        result = branch.is_local()

        assert result is True


class TestBranchPush:
    def test_branch_protocol_has_push_method(self) -> None:
        """Branch protocol defines push() method."""
        branch: Branch = MockBranch(name="test-branch", _push_will_succeed=True)

        result = branch.push()

        assert result is True

    def test_mock_branch_returns_configured_push_value(self) -> None:
        """MockBranch returns the configured _push_will_succeed value."""
        success_branch = MockBranch(name="success", _push_will_succeed=True)
        fail_branch = MockBranch(name="fail", _push_will_succeed=False)

        assert success_branch.push() is True
        assert fail_branch.push() is False


class TestSimpleBranchPush:
    def test_simple_branch_push_raises_not_implemented_error(self) -> None:
        """SimpleBranch.push() raises NotImplementedError."""
        branch = SimpleBranch(name="some-branch")

        with pytest.raises(NotImplementedError):
            branch.push()
