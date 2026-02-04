import os
import sys
from typing import TextIO

from dotenv import load_dotenv

from .GitHubClient import GitHubClient
from .PyGitHubClient import PyGitHubClient


class OtStackClient:
    """Main client for OtStack operations."""

    def __init__(
        self,
        github_client: GitHubClient | None = None,
        access_token: str | None = None,
        output: TextIO | None = None,
    ) -> None:
        """
        Initialize OtStackClient.

        Args:
            github_client: Optional GitHubClient to use (for testing/mocking).
            access_token: Optional GitHub access token. If not provided,
                         will load from GITHUB_PERSONAL_ACCESS_TOKEN env var.
            output: Optional output stream for printing. Defaults to stdout.

        Raises:
            ValueError: If no access token is provided or found in environment.
        """
        load_dotenv()

        self._output = output or sys.stdout

        if github_client is not None:
            self._github_client = github_client
        else:
            token = access_token or os.environ.get(
                "GITHUB_PERSONAL_ACCESS_TOKEN", None
            )

            if token is None:
                raise ValueError(
                    "GitHub access token required. Set GITHUB_PERSONAL_ACCESS_TOKEN "
                    "in .env or pass access_token parameter."
                )

            self._github_client = PyGitHubClient(token)

    def tree(self) -> None:
        """Display the PR dependency tree for all repositories."""
        pass

    @property
    def github(self) -> GitHubClient:
        """Get the GitHub client."""
        return self._github_client

    def close(self) -> None:
        """Close the client and release resources."""
        self._github_client.close()

    def __enter__(self) -> "OtStackClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()
