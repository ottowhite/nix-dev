from dataclasses import dataclass

from .Branch import Branch


@dataclass
class SimpleBranch(Branch):
    """Simple branch implementation that only holds a name.

    Use this when you only need branch metadata (e.g., for displaying PR info)
    but don't need local git operations.
    """

    name: str

    def merge(self, other_branch: Branch) -> bool:
        raise NotImplementedError(
            "SimpleBranch does not support merge. Use GitPythonBranch for local git operations."
        )

    def pull(self) -> bool:
        raise NotImplementedError(
            "SimpleBranch does not support pull. Use GitPythonBranch for local git operations."
        )
