import os
import sys
from typing import TextIO

from dotenv import load_dotenv

from .GitHubClient import GitHubClient
from .GitRepoDetector import GitPythonRepoDetector, GitRepoDetector
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
        repo_detector: GitRepoDetector | None = None,
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
            repo_detector: Optional GitRepoDetector for detecting the current repo
                          from git remotes. Defaults to GitPythonRepoDetector.

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

        self._repo_detector = repo_detector or GitPythonRepoDetector()

    def detect_repo_name(self) -> str | None:
        """
        Detect the GitHub repository name from the current git directory.

        Returns:
            Repository name in 'owner/repo' format, or None if not detectable.
        """
        return self._repo_detector.get_repo_name()

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
            max_text_width = col_width - 2  # Leave 1 char margin on each side

            # Get chains for each column (from deepest to shallowest)
            chains = [self._get_chain(child) for child in children]
            max_depth = max(len(chain) for chain in chains)

            # Print chains from top (deepest level) to bottom
            for level in range(max_depth - 1, -1, -1):
                # Print branch names at this level
                line = ""
                for chain in chains:
                    if level < len(chain):
                        branch_name = self._truncate_text(
                            chain[level].branch_name, max_text_width
                        )
                        line += branch_name.center(col_width)
                    else:
                        line += "".center(col_width)
                self._output.write(line.rstrip() + "\n")

                # Print PR titles at this level
                line = ""
                for chain in chains:
                    if level < len(chain):
                        node = chain[level]
                        pr_title = (
                            f'"{node.pull_request.title}"' if node.pull_request else ""
                        )
                        pr_title = self._truncate_text(pr_title, max_text_width)
                        line += pr_title.center(col_width)
                    else:
                        line += "".center(col_width)
                self._output.write(line.rstrip() + "\n")

                # Print connectors at this level
                line = ""
                for chain in chains:
                    if level < len(chain):
                        line += "|".center(col_width)
                    else:
                        line += "".center(col_width)
                self._output.write(line.rstrip() + "\n")

            # Print horizontal connecting line
            self._output.write(
                self._build_horizontal_connector(col_width, len(children)) + "\n"
            )
            # Print vertical connector to root
            self._output.write(self._center_text("|", width) + "\n")
            # Print root branch
            self._output.write(self._center_text(pr_tree.branch_name, width) + "\n")

    def _get_chain(self, node: PRTree) -> list[PRTree]:
        """Get a list of nodes from this node up to the deepest descendant (single-child chains only)."""
        chain = [node]
        current = node
        while current.children and len(current.children) == 1:
            current = current.children[0]
            chain.append(current)
        return chain

    def _print_chain(self, node: PRTree, width: int) -> None:
        """Print a chain of PRs vertically (top-down from deepest to this node)."""
        # Get the chain and print from deepest to shallowest
        chain = self._get_chain(node)
        max_text_width = width - 2  # Leave 1 char margin on each side
        for n in reversed(chain):
            branch_name = self._truncate_text(n.branch_name, max_text_width)
            pr_title = f'"{n.pull_request.title}"' if n.pull_request else ""
            pr_title = self._truncate_text(pr_title, max_text_width)

            self._output.write(self._center_text(branch_name, width) + "\n")
            self._output.write(self._center_text(pr_title, width) + "\n")
            self._output.write(self._center_text("|", width) + "\n")

    def _center_text(self, text: str, width: int) -> str:
        """Center text within width, without trailing whitespace."""
        padding = (width - len(text)) // 2
        return " " * padding + text

    def _truncate_text(self, text: str, max_width: int) -> str:
        """Truncate text with ... if it exceeds max_width."""
        if len(text) <= max_width:
            return text
        return text[: max_width - 3] + "..."

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
