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
        terminal_width: int | None = None,
    ) -> None:
        """
        Initialize OtStackClient.

        Args:
            github_client: Optional GitHubClient to use (for testing/mocking).
            access_token: Optional GitHub access token. If not provided,
                         will load from GITHUB_PERSONAL_ACCESS_TOKEN env var.
            output: Optional output stream for printing. Defaults to stdout.
            terminal_width: Optional terminal width. If not provided,
                           will use os.get_terminal_size().columns with fallback to 80.

        Raises:
            ValueError: If no access token is provided or found in environment.
        """
        load_dotenv()

        self._output = output or sys.stdout
        if terminal_width is None:
            try:
                terminal_width = os.get_terminal_size().columns
            except OSError:
                terminal_width = 80
        self._terminal_width = terminal_width

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
            self._print_horizontal_tree(pr_tree)

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

    def _print_horizontal_tree(self, pr_tree: PRTree) -> None:
        """Print the PR tree in horizontal format."""
        width = self._terminal_width

        # Get the top-level children (PRs targeting root)
        children = pr_tree.children
        if not children:
            return

        # For single child (possibly with its own children forming a chain)
        if len(children) == 1:
            self._print_chain(children[0], width)
            # Print root branch
            self._output.write(self._center_text(pr_tree.branch_name, width) + "\n")
        else:
            # For multiple PRs, divide into columns
            col_width = width // len(children)
            # Print branch names
            line = ""
            for child in children:
                line += child.branch_name.center(col_width)
            self._output.write(line.rstrip() + "\n")
            # Print PR titles
            line = ""
            for child in children:
                pr_title = f'"{child.pull_request.title}"' if child.pull_request else ""
                line += pr_title.center(col_width)
            self._output.write(line.rstrip() + "\n")
            # Print connectors
            line = ""
            for _ in children:
                line += "|".center(col_width)
            self._output.write(line.rstrip() + "\n")
            # Print horizontal connecting line
            self._output.write(
                self._build_horizontal_connector(col_width, len(children)) + "\n"
            )
            # Print vertical connector to root
            self._output.write(self._center_text("|", width) + "\n")
            # Print root branch
            self._output.write(self._center_text(pr_tree.branch_name, width) + "\n")

    def _print_chain(self, node: PRTree, width: int) -> None:
        """Print a chain of PRs vertically (top-down from deepest to this node)."""
        # First print any children (recursively)
        if node.children:
            # For now, only handle single child chains
            if len(node.children) == 1:
                self._print_chain(node.children[0], width)

        # Then print this node
        branch_name = node.branch_name
        pr_title = f'"{node.pull_request.title}"' if node.pull_request else ""

        self._output.write(self._center_text(branch_name, width) + "\n")
        self._output.write(self._center_text(pr_title, width) + "\n")
        self._output.write(self._center_text("|", width) + "\n")

    def _center_text(self, text: str, width: int) -> str:
        """Center text within width, without trailing whitespace."""
        padding = (width - len(text)) // 2
        return " " * padding + text

    def _build_horizontal_connector(self, col_width: int, num_cols: int) -> str:
        """Build a horizontal line connecting all columns with + at junctions."""
        # Each column's center point (matching str.center behavior)
        # str.center(30) for a 1-char string gives (30-1)//2 = 14 spaces before
        centers = [(col_width - 1) // 2 + i * col_width for i in range(num_cols)]

        # Build the line from first center to last center
        first_center = centers[0]
        last_center = centers[-1]

        result = " " * first_center + "+"
        result += "-" * (last_center - first_center - 1) + "+"

        return result

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
