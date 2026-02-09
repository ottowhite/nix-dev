from dataclasses import dataclass

from .PullRequest import PullRequest


@dataclass
class BelowDryRunResult:
    """Result of a dry-run below operation showing what would happen."""

    current_branch_name: str
    current_pr: PullRequest
    new_branch_name: str
    pr_title: str
    worktree_path: str
    original_destination_name: str
    copy_files: list[str] | None
    run_direnv: bool
