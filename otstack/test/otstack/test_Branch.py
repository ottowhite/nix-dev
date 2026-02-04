from otstack.Branch import Branch

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
