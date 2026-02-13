{ pkgs, otstack-pkg, ... }:

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
    ruff
    ripgrep
    nil
    lua-language-server
    otstack-pkg
  ];
}
