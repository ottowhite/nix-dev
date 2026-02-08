{ config, pkgs, lib, username, homeDirectory, ... }:

{
  imports = [
    ./modules/packages.nix
    ./modules/zsh.nix
    ./modules/tmux.nix
    ./modules/neovim.nix
    ./modules/direnv.nix
    ./modules/fzf.nix
  ];

  home.username = username;
  home.homeDirectory = homeDirectory;
  home.stateVersion = "24.05";

  # Let Home Manager manage itself
  programs.home-manager.enable = true;

  # Ensure .claude directory exists
  home.file.".claude/.keep".text = "";
}
