from typing import Protocol


class Branch(Protocol):
    """Protocol defining the interface for a git branch."""

    name: str

    def merge(self, other_branch: "Branch") -> bool:
        """
        Merge other_branch into this branch.

        Returns True if merge succeeded without conflicts.
        Returns False if there were conflicts (branch left in partially merged state).
        """
        ...
