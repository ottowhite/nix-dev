{ pkgs, ... }:

{
  home.packages = with pkgs; [
    git
    fzf
    tree
    tmux
    watch
    mosh
    direnv
    nix-direnv
    claude-code
    opkssh
    jq
    uv
    ty
    ruff
    ripgrep
    nil
    lua-language-server
    gopls
    go
    gh
  ];
}
