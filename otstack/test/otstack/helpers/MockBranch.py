from dataclasses import dataclass, field

from otstack.Branch import Branch


@dataclass
class MockBranch(Branch):
    name: str
    _merge_will_conflict: bool = field(default=False)

    def merge(self, other_branch: Branch) -> bool:
        if self._merge_will_conflict:
            return False
        return True
