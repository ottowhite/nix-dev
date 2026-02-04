- Always keep this CLAUDE.md up to date as you make changes
- Perform atomic git commits with standard git tags and descriptions as you work, and always push directly after committing

## Coding Practices

### File Organization
- Each class should be in its own file named exactly the same as the class (e.g., `OtStackClient` class in `OtStackClient.py`)
- Use Protocol classes for interfaces that need to be mocked in tests
- Concrete implementations should be prefixed with the library/implementation name (e.g., `PyGitHubClient` for PyGithub implementation)
- Never maintain `__init__.py` exports or `__all__` lists - this is an internal project and we are the only consumers, so we don't care about breaking compatibility. Less to keep in sync is better.

### Protocols and Interfaces
- We use Protocols extensively to completely mock out external interactions (like GitHub) for testing, and to define exact interfaces without coupling to implementation details
- Define Protocol classes for abstractions that will have multiple implementations or need to be mocked
- Protocol methods should have `...` as the body
- For data-holding protocols intended for dataclass implementations, use attribute annotations (e.g., `name: str`) rather than `@property` decorators
- Concrete implementations can use dataclasses for simple data-holding classes that implement protocols
- All protocol implementations should explicitly inherit from the protocol definition for clarity (e.g., `class PyGitHubClient(GitHubClient):`)

### Type Checking
- Never use `if TYPE_CHECKING:` guards - we always type check, so these are unnecessary indirection
