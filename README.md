# nix-dev

Otto's Nix configuration. The commands below terraform a fresh machine from scratch.

## Bootstrap a new machine

```bash
# Install nix (multi-user daemon install)
sh <(curl --proto '=https' --tlsv1.2 -L https://nixos.org/nix/install) --yes --daemon

# Activate nix in the current shell
. /nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh

# Enable flakes + nix-command for this session
export NIX_CONFIG="experimental-features = nix-command flakes"

# Bootstrap with home-manager (pick the config that matches the machine below)
nix run home-manager/master -- switch --flake github:ottowhite/nix-dev#ow20@server

# Make the newly installed zsh the default shell
sudo usermod -s $(which zsh) $(whoami)
```

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

> All `nix run`/`nix flake` invocations assume
> `NIX_CONFIG="experimental-features = nix-command flakes"` is exported (see the
> bootstrap step above). This matches the style used in `modules/zsh.nix`, so
> after the first switch the `hms` / `hmsr` shell helpers are available.
