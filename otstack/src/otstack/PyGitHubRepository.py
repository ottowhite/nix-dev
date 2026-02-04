from dataclasses import dataclass, field

from git import Repo
from github.Repository import Repository as GHRepository

from .Branch import Branch
from .LocalBranch import LocalBranch
from .PullRequest import PullRequest
from .PyGitHubPullRequest import PyGitHubPullRequest
from .Repository import Repository
from .SimpleBranch import SimpleBranch


@dataclass
class PyGitHubRepository(Repository):
    """Concrete implementation of Repository."""

    name: str
    full_name: str
    description: str | None
    private: bool
    url: str
    _gh_repo: GHRepository | None = field(default=None, repr=False)
    _git_repo: Repo | None = field(default=None, repr=False)

    def get_open_pull_requests(self) -> list[PullRequest]:
        """Get all open pull requests for this repository."""
        if self._gh_repo is None:
            return []
        prs: list[PullRequest] = []
        for pr in self._gh_repo.get_pulls(state="open"):
            if self._git_repo is not None:
                source_branch: Branch = LocalBranch(
                    name=pr.head.ref, _repo=self._git_repo
                )
                dest_branch: Branch = LocalBranch(
                    name=pr.base.ref, _repo=self._git_repo
                )
            else:
                source_branch = SimpleBranch(name=pr.head.ref)
                dest_branch = SimpleBranch(name=pr.base.ref)
            prs.append(
                PyGitHubPullRequest(
                    title=pr.title,
                    description=pr.body,
                    source_branch=source_branch,
                    destination_branch=dest_branch,
                    url=pr.html_url,
                    _gh_pr=pr,
                )
            )
        return prs

    def create_pr(
        self, source_branch: Branch, destination_branch: Branch, title: str
    ) -> PullRequest:
        """Create a pull request from source_branch to destination_branch."""
        if self._gh_repo is None or self._git_repo is None:
            raise ValueError("Cannot create PR without GitHub repository reference")
        pr = self._gh_repo.create_pull(
            title=title,
            body="",
            head=source_branch.name,
            base=destination_branch.name,
        )
        return PyGitHubPullRequest(
            title=pr.title,
            description=pr.body,
            source_branch=LocalBranch(name=pr.head.ref, _repo=self._git_repo),
            destination_branch=LocalBranch(name=pr.base.ref, _repo=self._git_repo),
            url=pr.html_url,
            _gh_pr=pr,
        )

    def get_branches(self) -> list[Branch]:
        """Get all branches in this repository."""
        if self._git_repo is None:
            return []
        branches: list[Branch] = []
        for ref in self._git_repo.references:
            if hasattr(ref, "name") and not ref.name.startswith("origin/"):
                branches.append(LocalBranch(name=ref.name, _repo=self._git_repo))
        return branches

    def get_local_branches(self) -> list[Branch]:
        """
        Get all branches with local filesystem checkouts (main repo and worktrees).

        Raises ValueError if no local git repository is associated.
        """
        if self._git_repo is None:
            raise ValueError("No local git repository associated")

        branches: list[Branch] = []

        # Get the main repo's currently checked out branch
        if not self._git_repo.head.is_detached:
            branches.append(
                LocalBranch(name=self._git_repo.active_branch.name, _repo=self._git_repo)
            )

        # Get worktree branches
        try:
            worktree_output = self._git_repo.git.worktree("list", "--porcelain")
            current_worktree_path = None
            for line in worktree_output.splitlines():
                if line.startswith("worktree "):
                    current_worktree_path = line[9:]  # Remove "worktree " prefix
                elif line.startswith("branch "):
                    branch_ref = line[7:]  # Remove "branch " prefix
                    # Extract branch name from refs/heads/branch-name
                    if branch_ref.startswith("refs/heads/"):
                        branch_name = branch_ref[11:]  # Remove "refs/heads/" prefix
                        # Skip if this is the main repo (already added above)
                        if current_worktree_path != str(self._git_repo.working_dir):
                            branches.append(
                                LocalBranch(name=branch_name, _repo=self._git_repo)
                            )
        except Exception:
            # Worktree command failed or not supported, just return main branch
            pass

        return branches
