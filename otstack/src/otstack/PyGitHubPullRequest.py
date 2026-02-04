from dataclasses import dataclass, field

from github.PullRequest import PullRequest as GHPullRequest

from .Branch import Branch
from .PullRequest import PullRequest


@dataclass
class PyGitHubPullRequest(PullRequest):
    """Concrete implementation of PullRequest."""

    title: str
    description: str | None
    source_branch: Branch
    destination_branch: Branch
    url: str
    _gh_pr: GHPullRequest | None = field(default=None, repr=False)

    def change_destination(self, new_destination: Branch) -> None:
        """Change the destination branch of this pull request."""
        if self._gh_pr is None:
            raise ValueError("Cannot change destination without GitHub PR reference")
        self._gh_pr.edit(base=new_destination.name)
        self.destination_branch = new_destination

    def get_branch(self) -> Branch:
        """Get the source branch of this pull request."""
        return self.source_branch

    def is_local(self) -> bool:
        """Return True if both source and destination branches are local."""
        return self.source_branch.is_local() and self.destination_branch.is_local()
