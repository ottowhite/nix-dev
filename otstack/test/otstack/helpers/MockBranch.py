from dataclasses import dataclass, field

from otstack.Branch import Branch


@dataclass
class MockBranch(Branch):
    name: str
    _merge_will_conflict: bool = field(default=False)
    _pull_has_new_commits: bool = field(default=False)

    def merge(self, other_branch: Branch) -> bool:
        if self._merge_will_conflict:
            return False
        return True

    def pull(self) -> bool:
        return self._pull_has_new_commits
