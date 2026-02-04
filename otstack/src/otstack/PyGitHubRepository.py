from dataclasses import dataclass, field

from github.Repository import Repository as GHRepository

from .PullRequest import PullRequest
from .PyGitHubPullRequest import PyGitHubPullRequest
from .Repository import Repository


@dataclass
class PyGitHubRepository(Repository):
    """Concrete implementation of Repository."""

    name: str
    full_name: str
    description: str | None
    private: bool
    url: str
    _gh_repo: GHRepository | None = field(default=None, repr=False)

    def get_open_pull_requests(self) -> list[PullRequest]:
        """Get all open pull requests for this repository."""
        if self._gh_repo is None:
            return []
        prs: list[PullRequest] = []
        for pr in self._gh_repo.get_pulls(state="open"):
            prs.append(
                PyGitHubPullRequest(
                    title=pr.title,
                    description=pr.body,
                    source_branch=pr.head.ref,
                    destination_branch=pr.base.ref,
                    url=pr.html_url,
                    _gh_pr=pr,
                )
            )
        return prs

    def create_pr(
        self, source_branch: str, destination_branch: str, title: str
    ) -> PullRequest:
        """Create a pull request from source_branch to destination_branch."""
        if self._gh_repo is None:
            raise ValueError("Cannot create PR without GitHub repository reference")
        pr = self._gh_repo.create_pull(
            title=title,
            body="",
            head=source_branch,
            base=destination_branch,
        )
        return PyGitHubPullRequest(
            title=pr.title,
            description=pr.body,
            source_branch=pr.head.ref,
            destination_branch=pr.base.ref,
            url=pr.html_url,
            _gh_pr=pr,
        )
