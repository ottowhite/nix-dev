from dataclasses import dataclass

from otstack.Branch import Branch
from otstack.PullRequest import PullRequest


@dataclass
class MockPullRequest(PullRequest):
    title: str
    description: str | None
    source_branch: Branch
    destination_branch: Branch
    url: str

    def change_destination(self, new_destination: Branch) -> None:
        self.destination_branch = new_destination
