# nix-dev

Otto's personal Nix configuration using Home Manager standalone installation.

## Structure

- `flake.nix` - Flake definition with Home Manager configurations
- `home.nix` - Main Home Manager configuration (zsh, tmux, neovim, packages)
- `configuration.nix` - NixOS system configuration (separate from Home Manager)

## Usage

### Apply configuration on current machine

```bash
home-manager switch --flake .#ow20@nixos
```

### Apply on a different machine/user

```bash
home-manager switch --flake .#ow20@server
```

### Add a new machine configuration

Edit `flake.nix` and add a new entry to `homeConfigurations`:

```nix
"username@machine" = mkHomeConfiguration {
  system = "x86_64-linux";  # or aarch64-darwin for macOS
  username = "username";
  homeDirectory = "/home/username";  # or /Users/username on macOS
};
```

## Development Guidelines

- Perform atomic git commits with standard git tags and descriptions as you work, and always push directly after committing.
- Always keep the project-level CLAUDE.md up to date as you make changes
