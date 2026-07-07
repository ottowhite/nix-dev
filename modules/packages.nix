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
    # claude-code itself is installed by programs.claude-code (modules/claude-code.nix);
    # listing it here too collides with that module's plugin-wrapped `claude`.
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
    playwright-mcp
    ncdu
  ];
}
