from dataclasses import dataclass, field

from git import Repo
from git.exc import GitCommandError

from .Branch import Branch


@dataclass
class GitPythonBranch(Branch):
    """Concrete implementation of Branch using GitPython."""

    name: str
    _repo: Repo = field(repr=False)

    def merge(self, other_branch: Branch) -> bool:
        """
        Merge other_branch into this branch.

        Returns True if merge succeeded without conflicts.
        Returns False if there were conflicts (branch left in partially merged state).
        """
        # Checkout this branch first
        self._repo.git.checkout(self.name)

        try:
            self._repo.git.merge(other_branch.name)
            return True
        except GitCommandError:
            # Merge conflict occurred, branch is left in partially merged state
            return False
