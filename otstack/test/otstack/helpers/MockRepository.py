from dataclasses import dataclass, field

from otstack.Branch import Branch
from otstack.PullRequest import PullRequest
from otstack.Repository import Repository

from .MockPullRequest import MockPullRequest


@dataclass
class MockRepository(Repository):
    name: str
    full_name: str
    description: str | None
    private: bool
    url: str
    _branches: list[Branch] = field(default_factory=list)

    def get_open_pull_requests(self) -> list[PullRequest]:
        return []

    def create_pr(
        self, source_branch: Branch, destination_branch: Branch, title: str
    ) -> PullRequest:
        return MockPullRequest(
            title=title,
            description=None,
            source_branch=source_branch,
            destination_branch=destination_branch,
            url=f"{self.url}/pull/1",
        )

    def get_branches(self) -> list[Branch]:
        return self._branches
