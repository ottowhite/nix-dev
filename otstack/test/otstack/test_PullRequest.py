from otstack.PullRequest import PullRequest
from otstack.PyGitHubPullRequest import PyGitHubPullRequest

from .helpers.MockBranch import MockBranch
from .helpers.MockPullRequest import MockPullRequest


class TestPullRequestIsLocal:
    def test_pull_request_protocol_has_is_local_method(self) -> None:
        """PullRequest protocol defines is_local() method."""
        pr: PullRequest = _make_pr(
            source_is_local=True,
            destination_is_local=True,
        )

        result = pr.is_local()

        assert result is True

    def test_mock_pull_request_returns_true_when_both_branches_local(self) -> None:
        """MockPullRequest.is_local() returns True when both branches are local."""
        pr = _make_pr(source_is_local=True, destination_is_local=True)

        assert pr.is_local() is True

    def test_mock_pull_request_returns_false_when_source_not_local(self) -> None:
        """MockPullRequest.is_local() returns False when source branch is not local."""
        pr = _make_pr(source_is_local=False, destination_is_local=True)

        assert pr.is_local() is False

    def test_mock_pull_request_returns_false_when_destination_not_local(self) -> None:
        """MockPullRequest.is_local() returns False when destination branch is not local."""
        pr = _make_pr(source_is_local=True, destination_is_local=False)

        assert pr.is_local() is False

    def test_mock_pull_request_returns_false_when_neither_branch_local(self) -> None:
        """MockPullRequest.is_local() returns False when neither branch is local."""
        pr = _make_pr(source_is_local=False, destination_is_local=False)

        assert pr.is_local() is False


class TestPyGitHubPullRequestIsLocal:
    def test_pygithub_pr_returns_true_when_both_branches_local(self) -> None:
        """PyGitHubPullRequest.is_local() returns True when both branches are local."""
        pr = _make_pygithub_pr(source_is_local=True, destination_is_local=True)

        assert pr.is_local() is True

    def test_pygithub_pr_returns_false_when_source_not_local(self) -> None:
        """PyGitHubPullRequest.is_local() returns False when source is not local."""
        pr = _make_pygithub_pr(source_is_local=False, destination_is_local=True)

        assert pr.is_local() is False


# Test helpers


def _make_pr(
    source_is_local: bool,
    destination_is_local: bool,
) -> MockPullRequest:
    """Create a MockPullRequest with branches having specified locality."""
    return MockPullRequest(
        title="Test PR",
        description=None,
        source_branch=MockBranch(name="feature", _is_local=source_is_local),
        destination_branch=MockBranch(name="main", _is_local=destination_is_local),
        url="https://github.com/test/repo/pull/1",
    )


def _make_pygithub_pr(
    source_is_local: bool,
    destination_is_local: bool,
) -> PyGitHubPullRequest:
    """Create a PyGitHubPullRequest with branches having specified locality."""
    return PyGitHubPullRequest(
        title="Test PR",
        description=None,
        source_branch=MockBranch(name="feature", _is_local=source_is_local),
        destination_branch=MockBranch(name="main", _is_local=destination_is_local),
        url="https://github.com/test/repo/pull/1",
    )
