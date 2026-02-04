import sys
from io import StringIO
from unittest.mock import patch

from main import main

from .helpers.MockBranch import MockBranch
from .helpers.MockGitHubClient import MockGitHubClient
from .helpers.MockGitRepoDetector import MockGitRepoDetector
from .helpers.MockPullRequest import MockPullRequest
from .helpers.MockRepository import MockRepository


class TestSyncCommand:
    def test_sync_command_prints_success_message(self) -> None:
        """sync command prints success message when all PRs are synced."""
        repo = _make_repo_with_local_pr()
        mock_client = MockGitHubClient(repos=[repo])
        mock_detector = MockGitRepoDetector(repo_name="test-user/test-repo")

        with (
            patch.object(sys, "argv", ["otstack", "sync"]),
            patch(
                "main.OtStackClient",
                return_value=_make_mock_client_context(mock_client, mock_detector),
            ),
            patch.object(sys, "stdout", new_callable=StringIO) as mock_stdout,
        ):
            main()
            output = mock_stdout.getvalue()
            assert "All PRs synced successfully!" in output

    def test_sync_command_with_repo_argument(self) -> None:
        """sync command accepts --repo argument."""
        repo = _make_repo_with_local_pr()
        mock_client = MockGitHubClient(repos=[repo])
        mock_detector = MockGitRepoDetector(repo_name=None)

        with (
            patch.object(sys, "argv", ["otstack", "sync", "--repo", "test-user/test-repo"]),
            patch(
                "main.OtStackClient",
                return_value=_make_mock_client_context(mock_client, mock_detector),
            ),
            patch.object(sys, "stdout", new_callable=StringIO) as mock_stdout,
        ):
            main()
            output = mock_stdout.getvalue()
            assert "All PRs synced successfully!" in output


# Test helpers


def _make_repo_with_local_pr() -> MockRepository:
    """Create a repo with a local PR for testing."""
    pr = MockPullRequest(
        title="Add feature",
        description=None,
        source_branch=MockBranch(name="feature", _is_local=True),
        destination_branch=MockBranch(name="main", _is_local=True),
        url="https://github.com/test-user/test-repo/pull/1",
    )
    return MockRepository(
        name="test-repo",
        full_name="test-user/test-repo",
        description="Test repository",
        private=False,
        url="https://github.com/test-user/test-repo",
        _pull_requests=[pr],
    )


class _MockOtStackClientContext:
    """Context manager for mocking OtStackClient."""

    def __init__(self, github_client, repo_detector):
        from otstack.OtStackClient import OtStackClient

        self._client = OtStackClient(
            github_client=github_client, repo_detector=repo_detector
        )

    def __enter__(self):
        return self._client

    def __exit__(self, *args):
        pass


def _make_mock_client_context(mock_client, mock_detector) -> _MockOtStackClientContext:
    """Create a mock OtStackClient context manager."""
    return _MockOtStackClientContext(mock_client, mock_detector)
