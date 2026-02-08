{ pkgs, ... }:

{
  programs.neovim = {
    enable = true;
    defaultEditor = true;

    plugins = with pkgs.vimPlugins; [
      nvim-lspconfig
      telescope-nvim
      plenary-nvim
      tokyonight-nvim
      (nvim-treesitter.withPlugins (p: [ p.python p.nix ]))
      nvim-cmp
      cmp-nvim-lsp
      nvim-tree-lua
      copilot-vim
    ];

    extraLuaConfig = builtins.readFile ./nvim/init.lua;
  };
}
