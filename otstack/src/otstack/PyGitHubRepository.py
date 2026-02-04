from dataclasses import dataclass, field

from git import Repo
from github.Repository import Repository as GHRepository

from .Branch import Branch
from .GitPythonBranch import GitPythonBranch
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
                source_branch: Branch = GitPythonBranch(
                    name=pr.head.ref, _repo=self._git_repo
                )
                dest_branch: Branch = GitPythonBranch(
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
            source_branch=GitPythonBranch(name=pr.head.ref, _repo=self._git_repo),
            destination_branch=GitPythonBranch(name=pr.base.ref, _repo=self._git_repo),
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
                branches.append(GitPythonBranch(name=ref.name, _repo=self._git_repo))
        return branches
