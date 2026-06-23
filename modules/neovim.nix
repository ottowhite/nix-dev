{ pkgs, ... }:

{
  programs.neovim = {
    enable = true;
    defaultEditor = true;

    # Keep legacy provider defaults (these flipped to false for stateVersion
    # >= 26.05); pin them so the build doesn't warn.
    withRuby = true;
    withPython3 = true;

    plugins = with pkgs.vimPlugins; [
      nvim-lspconfig
      telescope-nvim
      plenary-nvim
      onedark-nvim
      tokyonight-nvim
      catppuccin-nvim
      gruvbox-nvim
      rose-pine
      kanagawa-nvim
      nightfox-nvim
      dracula-nvim
      nord-nvim
      (nvim-treesitter.withPlugins (p: [ p.python p.nix p.lua p.go p.gomod p.gosum ]))
      nvim-cmp
      cmp-nvim-lsp
      nvim-tree-lua
      copilot-vim
    ];

    initLua = builtins.readFile ./nvim/init.lua;
  };
}
