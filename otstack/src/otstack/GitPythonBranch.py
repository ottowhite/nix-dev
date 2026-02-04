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

        Returns True if merge would succeed without conflicts.
        Returns False if there would be conflicts (no changes made to branch).
        """
        self._repo.git.checkout(self.name)

        # Check if merge would have conflicts using --no-commit --no-ff
        try:
            self._repo.git.merge("--no-commit", "--no-ff", other_branch.name)
            # Merge succeeded, commit it
            self._repo.git.commit("-m", f"Merge branch '{other_branch.name}'")
            return True
        except GitCommandError:
            # Merge would conflict, abort to leave branch clean
            self._repo.git.merge("--abort")
            return False

    def pull(self) -> bool:
        """
        Pull latest changes from remote for this branch.

        Returns True if new commits were pulled.
        Returns False if already up to date.
        """
        self._repo.git.checkout(self.name)

        # Get current HEAD before pull
        head_before = self._repo.head.commit.hexsha

        try:
            self._repo.git.pull("origin", self.name)
        except GitCommandError:
            return False

        # Check if HEAD changed
        head_after = self._repo.head.commit.hexsha
        return head_before != head_after
