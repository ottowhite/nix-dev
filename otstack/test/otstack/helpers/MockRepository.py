from dataclasses import dataclass

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

    def get_open_pull_requests(self) -> list[PullRequest]:
        return []

    def create_pr(
        self, source_branch: str, destination_branch: str, title: str
    ) -> PullRequest:
        return MockPullRequest(
            title=title,
            description=None,
            source_branch=source_branch,
            destination_branch=destination_branch,
            url=f"{self.url}/pull/1",
        )
