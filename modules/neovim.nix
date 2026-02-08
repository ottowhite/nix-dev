{ pkgs, ... }:

{
  programs.neovim = {
    enable = true;
    defaultEditor = true;

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
      (nvim-treesitter.withPlugins (p: [ p.python p.nix p.lua ]))
      nvim-cmp
      cmp-nvim-lsp
      nvim-tree-lua
      copilot-vim
    ];

    initLua = builtins.readFile ./nvim/init.lua;
  };
}
