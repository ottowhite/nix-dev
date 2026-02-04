from dataclasses import dataclass, field

from github.PullRequest import PullRequest as GHPullRequest

from .PullRequest import PullRequest


@dataclass
class PyGitHubPullRequest(PullRequest):
    """Concrete implementation of PullRequest."""

    title: str
    description: str | None
    source_branch: str
    destination_branch: str
    url: str
    _gh_pr: GHPullRequest | None = field(default=None, repr=False)

    def change_destination(self, new_destination: str) -> None:
        """Change the destination branch of this pull request."""
        if self._gh_pr is None:
            raise ValueError("Cannot change destination without GitHub PR reference")
        self._gh_pr.edit(base=new_destination)
        self.destination_branch = new_destination
