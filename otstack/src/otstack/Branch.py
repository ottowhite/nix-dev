from typing import Protocol


class Branch(Protocol):
    """Protocol defining the interface for a git branch."""

    name: str

    def merge(self, other_branch: "Branch") -> bool:
        """
        Merge other_branch into this branch.

        Returns True if merge would succeed without conflicts.
        Returns False if there would be conflicts (no changes made to branch).
        """
        ...

    def pull(self) -> bool:
        """
        Pull latest changes from remote for this branch.

        Returns True if new commits were pulled.
        Returns False if already up to date.
        """
        ...
