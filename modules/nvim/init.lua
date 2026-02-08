vim.g.mapleader = " "
vim.g.copilot_no_tab_map = true
vim.keymap.set('i', '<C-y>', 'copilot#Accept("<CR>")', { expr = true, replace_keycodes = false })
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.clipboard:append("unnamedplus")

-- Colorscheme with treesitter support
vim.cmd.colorscheme("tokyonight")

-- Enable treesitter highlighting for all buffers
vim.api.nvim_create_autocmd("FileType", {
  pattern = "python",
  callback = function()
    vim.treesitter.start()
  end,
})

-- LSP: ty (Python type checker)
vim.lsp.config('ty', {
  cmd = { 'ty', 'server' },
  filetypes = { 'python' },
  root_markers = { 'pyproject.toml', 'ty.toml', '.git' },
})
vim.lsp.enable('ty')

-- LSP: nil (Nix)
vim.lsp.config('nil_ls', {
  cmd = { 'nil' },
  filetypes = { 'nix' },
  root_markers = { 'flake.nix', '.git' },
})
vim.lsp.enable('nil_ls')

vim.diagnostic.config({
  virtual_text = true,
  signs = true,
  underline = true,
  update_in_insert = true,
})

-- Completion setup
local cmp = require('cmp')
cmp.setup({
  sources = {
    { name = 'nvim_lsp' },
  },
  mapping = cmp.mapping.preset.insert({
    ['<Tab>'] = cmp.mapping.select_next_item(),
    ['<S-Tab>'] = cmp.mapping.select_prev_item(),
    ['<CR>'] = cmp.mapping.confirm({ select = true }),
  }),
})

-- File explorer
require('nvim-tree').setup()
vim.keymap.set('n', '<C-b>', '<cmd>NvimTreeToggle<CR>')

-- Telescope setup with custom keybindings
local actions = require('telescope.actions')
require('telescope').setup({
  defaults = {
    mappings = {
      i = {
        ["<C-j>"] = actions.move_selection_next,
        ["<C-k>"] = actions.move_selection_previous,
        ["<CR>"] = actions.select_tab,
      },
    },
  },
})

-- Keybindings
vim.keymap.set("n", "<leader>h", "gT")
vim.keymap.set("n", "<leader>l", "gt")
vim.keymap.set("n", "<C-p>", "<cmd>Telescope lsp_definitions<CR>")
vim.keymap.set("n", "<C-S-p>", "<cmd>Telescope lsp_references<CR>")
vim.keymap.set("n", "<C-f>", "<cmd>Telescope find_files<CR>")
vim.keymap.set("n", "<C-d>", "<cmd>Telescope live_grep<CR>")
