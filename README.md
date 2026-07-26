# nix-dev

Otto's Nix configuration. The commands below terraform a fresh machine from scratch.

## Bootstrap a new machine

```bash
# Install nix (multi-user daemon install)
sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install) --yes --daemon

# Activate nix in the current shell
. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh

# Enable flakes + nix-command, and build derivations in parallel, for this session
export NIX_CONFIG="experimental-features = nix-command flakes
max-jobs = auto"

# Bootstrap with home-manager (pick the config that matches the machine below)
nix run home-manager/master -- switch --flake github:ottowhite/nix-dev#ow20@server

# Make the newly installed zsh the default shell
sudo usermod -s $(which zsh) $(whoami)
```

> The `max-jobs = auto` line builds derivations in parallel. The configs set
> `nix.settings.max-jobs = "auto"`, but that only takes effect *after* the first
> activation, and Nix otherwise defaults to `max-jobs = 1` (fully serial). Since a
> cold bootstrap builds ~75 local derivations (a config-specific neovim wrapper
> plus plugins that miss the public cache), setting it in `NIX_CONFIG` for the
> bootstrap session roughly halves wall-clock on a multi-core machine. Every
> rebuild after the first picks it up from the activated config automatically.

## Available configurations

The flake exposes one `homeConfigurations` output per machine. Swap the
`#...` selector on the bootstrap command for any of these:

```bash
# macOS laptop (aarch64-darwin)
nix run home-manager/master -- switch --flake github:ottowhite/nix-dev#ottowhite@Ottos-MacBook-Pro.local

# NixOS laptop (x86_64-linux)
nix run home-manager/master -- switch --flake github:ottowhite/nix-dev#otto@nixos

# Server, ow20 user (x86_64-linux)
nix run home-manager/master -- switch --flake github:ottowhite/nix-dev#ow20@server

# Server, ansible user (x86_64-linux)
nix run home-manager/master -- switch --flake github:ottowhite/nix-dev#ansible@server

# CSG server, ow20 user (x86_64-linux)
nix run home-manager/master -- switch --flake github:ottowhite/nix-dev#ow20@csgserver
```

> All `nix run`/`nix flake` invocations assume the `NIX_CONFIG` export from the
> bootstrap step above is in effect (`experimental-features = nix-command flakes`,
> plus `max-jobs = auto`). This matches the style used in `modules/zsh.nix`, so
> after the first switch the `hms` / `hmsr` shell helpers are available.

## Measuring cold-build cost

`Makefile.dev` has two targets that measure a from-scratch build without
touching the real `/nix/store` (they build into a throwaway chroot store that is
torn down on exit). Override `CONFIG=<name>` for a config other than the default
`ow20@server`:

```bash
# Timed cold build — total wall-clock only
make -f Makefile.dev cold-build

# Timed breakdown — attributes wall-clock to eval / download / local-build
# phases and lists the slowest downloads and derivations
make -f Makefile.dev cold-build-breakdown
```
