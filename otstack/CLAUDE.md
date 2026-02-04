- Perform atomic git commits with standard git tags and descriptions as you work, and always push directly after committing.
- Always keep the project-level CLAUDE.md up to date as you make changes

## Coding Practices

### File Organization
- Each class should be in its own file named exactly the same as the class (e.g., `OtStackClient` class in `OtStackClient.py`)
- Use Protocol classes for interfaces that need to be mocked in tests
- Concrete implementations should be prefixed with the library/implementation name (e.g., `PyGitHubClient` for PyGithub implementation)

### Protocols and Interfaces
- Define Protocol classes for abstractions that will have multiple implementations or need to be mocked
- Protocol methods should have `...` as the body
- For data-holding protocols intended for dataclass implementations, use attribute annotations (e.g., `name: str`) rather than `@property` decorators
- Concrete implementations can use dataclasses for simple data-holding classes that implement protocols
- All protocol implementations should explicitly inherit from the protocol definition for clarity (e.g., `class PyGitHubClient(GitHubClient):`)
