- Perform atomic git commits with standard git tags and descriptions as you work, and always push directly after committing.
- Always keep the project-level CLAUDE.md up to date as you make changes

## Project Structure

- `home.nix` - Main entry point that imports all modules
- `flake.nix` - Nix flake configuration
- `modules/` - Modular configuration files:
  - `packages.nix` - System packages
  - `zsh.nix` - Zsh shell configuration
  - `tmux.nix` - Tmux terminal multiplexer
  - `neovim.nix` - Neovim editor
  - `direnv.nix` - Direnv integration
  - `fzf.nix` - FZF fuzzy finder