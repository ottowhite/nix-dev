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
        if not prs:
            return

        # Find root branches (destinations that are not source branches of any PR)
        source_branches = {pr.source_branch.name for pr in prs}
        dest_branches = {pr.destination_branch.name for pr in prs}
        roots = [dest for dest in dest_branches if dest not in source_branches]

        for root in roots:
            pr_tree = self.get_pr_tree(repo, root)
            self._output.write(f"{pr_tree.branch_name}\n")
            self._print_pr_tree(pr_tree, "")

    def get_repo(self, name: str) -> Repository:
        """Get a repository by name (e.g., 'owner/repo')."""
        return self._github_client.get_repo(name)

    def get_pr_tree(self, repo: Repository, branch: str) -> PRTree:
        """Get the PR dependency tree rooted at the given branch."""
        prs = repo.get_open_pull_requests()
        return self._build_pr_tree(branch, None, prs)

    def _build_pr_tree(
        self,
        branch: str,
        pull_request: PullRequest | None,
        all_prs: list[PullRequest],
    ) -> PRTree:
        """Recursively build a PRTree for the given branch."""
        children = [
            self._build_pr_tree(pr.source_branch.name, pr, all_prs)
            for pr in all_prs
            if pr.destination_branch.name == branch
        ]
        return PRTree(branch_name=branch, pull_request=pull_request, children=children)

    def _print_pr_tree(self, pr_tree: PRTree, prefix: str) -> None:
        """Recursively print a PRTree."""
        for i, child in enumerate(pr_tree.children):
            is_last = i == len(pr_tree.children) - 1
            connector = "└── " if is_last else "├── "
            pr_title = child.pull_request.title if child.pull_request else ""
            self._output.write(f'{prefix}{connector}{child.branch_name} (PR: "{pr_title}")\n')
            extension = "    " if is_last else "│   "
            self._print_pr_tree(child, prefix + extension)

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
