import os
import sys
from typing import TextIO

from dotenv import load_dotenv

from .GitHubClient import GitHubClient
from .PRTree import PRTree
from .PullRequest import PullRequest
from .PyGitHubClient import PyGitHubClient
from .Repository import Repository


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

    def tree(self, repo: Repository) -> None:
        """Display the PR dependency tree for a repository."""
        prs = repo.get_open_pull_requests()
        if prs:
            self._print_tree(prs)

    def get_repo(self, name: str) -> Repository:
        """Get a repository by name (e.g., 'owner/repo')."""
        return self._github_client.get_repo(name)

    def get_pr_tree(self, repo: Repository, branch: str) -> PRTree:
        """Get the PR dependency tree rooted at the given branch."""
        return PRTree(branch_name=branch, pull_request=None, children=[])

    def _print_tree(self, prs: list[PullRequest]) -> None:
        """Print the PR dependency tree."""
        # Build a mapping of destination -> list of PRs that target it
        children: dict[str, list[PullRequest]] = {}
        for pr in prs:
            dest = pr.destination_branch.name
            if dest not in children:
                children[dest] = []
            children[dest].append(pr)

        # Find root destinations (destinations that are not source branches of any PR)
        source_branches = {pr.source_branch.name for pr in prs}
        roots = [dest for dest in children if dest not in source_branches]

        for root in roots:
            self._output.write(f"{root}\n")
            self._print_subtree(root, children, "", True)

    def _print_subtree(
        self,
        branch: str,
        children: dict[str, list[PullRequest]],
        prefix: str,
        is_last: bool,
    ) -> None:
        """Recursively print a subtree."""
        if branch not in children:
            return

        branch_prs = children[branch]
        for i, pr in enumerate(branch_prs):
            is_last_child = i == len(branch_prs) - 1
            connector = "└── " if is_last_child else "├── "
            self._output.write(
                f'{prefix}{connector}{pr.source_branch.name} (PR: "{pr.title}")\n'
            )
            extension = "    " if is_last_child else "│   "
            self._print_subtree(
                pr.source_branch.name, children, prefix + extension, is_last_child
            )

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
