{ pkgs, lib, username, homeDirectory, isLaptop ? false, ... }:

{
  imports = [
    ./modules/packages.nix
    ./modules/zsh.nix
    ./modules/tmux.nix
    ./modules/neovim.nix
    ./modules/direnv.nix
    ./modules/fzf.nix
    ./modules/ghostty-terminfo.nix
    ./modules/claude-code.nix
    ./modules/ssh.common.nix
  ] ++ lib.optional isLaptop ./modules/ssh.local.nix;

  home.username = username;
  home.homeDirectory = homeDirectory;
  home.stateVersion = "24.05";
  home.sessionPath = [ "${homeDirectory}/.local/bin" ];

  nix.package = pkgs.nix;
  nix.settings.experimental-features = [ "nix-command" "flakes" ];

  xdg.enable = true;

  # Let Home Manager manage itself
  programs.home-manager.enable = true;

  # Suppress the "Last login:" and "You have mail." messages printed by
  # login(1) at the start of each login shell.
  home.file.".hushlogin".text = "";
}
