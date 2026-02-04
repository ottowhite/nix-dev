from dataclasses import dataclass

from otstack.PullRequest import PullRequest


@dataclass
class MockPullRequest(PullRequest):
    title: str
    description: str | None
    source_branch: str
    destination_branch: str
    url: str
