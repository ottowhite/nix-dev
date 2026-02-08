{ pkgs, ... }:

{
  home.packages = with pkgs; [
    fzf
    tree
    tmux
    watch
    mosh
    stgit
    direnv
    nix-direnv
    claude-code
    github-copilot-cli
    graphite-cli
    shell-gpt
    opkssh
    nodejs_24
    jq
    uv
    ty
    ripgrep
    nil
  ];
}
