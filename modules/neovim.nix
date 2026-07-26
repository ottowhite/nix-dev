{ pkgs, ... }:

{
  programs.neovim = {
    enable = true;
    defaultEditor = true;

    # Disable the Ruby/Python remote-plugin providers: nothing here uses :ruby
    # or :python3 rplugins, and they pull an extra ruby/python provider build and
    # closure into every (cache-missing, config-specific) neovim wrapper build.
    # Setting them explicitly also silences the stateVersion < 26.05 deprecation
    # warning about the default flipping to false.
    withRuby = false;
    withPython3 = false;

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
