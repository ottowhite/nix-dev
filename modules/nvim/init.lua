vim.g.mapleader = " "
vim.g.copilot_no_tab_map = true
vim.keymap.set('i', '<C-y>', 'copilot#Accept("<CR>")', { expr = true, replace_keycodes = false })
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.clipboard:append("unnamedplus")

-- Colorscheme
vim.cmd.colorscheme("carbonfox")

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

-- LSP: ruff (Python linter)
vim.lsp.config('ruff', {
  cmd = { 'ruff', 'server' },
  filetypes = { 'python' },
  root_markers = { 'pyproject.toml', 'ruff.toml', '.ruff.toml', '.git' },
})
vim.lsp.enable('ruff')

-- Ruff autofix on save
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = "*.py",
  callback = function()
    vim.lsp.buf.code_action({
      context = { only = { "source.fixAll.ruff" } },
      apply = true,
    })
  end,
})

-- LSP: nil (Nix)
vim.lsp.config('nil_ls', {
  cmd = { 'nil' },
  filetypes = { 'nix' },
  root_markers = { 'flake.nix', '.git' },
})
vim.lsp.enable('nil_ls')

-- LSP: lua-language-server
vim.lsp.config('lua_ls', {
  cmd = { 'lua-language-server' },
  filetypes = { 'lua' },
  root_markers = { '.luarc.json', '.git' },
  settings = {
    Lua = {
      runtime = { version = 'LuaJIT' },
      workspace = { library = vim.api.nvim_get_runtime_file("", true) },
    },
  },
})
vim.lsp.enable('lua_ls')

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
vim.keymap.set('n', '<C-w>>', '20<C-w>>')
vim.keymap.set('n', '<C-w><', '20<C-w><')

-- Telescope setup with custom keybindings
local actions = require('telescope.actions')
local action_state = require('telescope.actions.state')

-- Custom action: open in new tab, or replace if current buffer is empty
local function select_tab_or_replace_empty(prompt_bufnr)
  local picker = action_state.get_current_picker(prompt_bufnr)
  local original_win = picker.original_win_id
  local original_buf = vim.api.nvim_win_get_buf(original_win)

  local buf_name = vim.api.nvim_buf_get_name(original_buf)
  local buf_modified = vim.bo[original_buf].modified
  local line_count = vim.api.nvim_buf_line_count(original_buf)
  local first_line = vim.api.nvim_buf_get_lines(original_buf, 0, 1, false)[1] or ""

  local is_empty = buf_name == "" and not buf_modified and line_count == 1 and first_line == ""

  if is_empty then
    actions.select_default(prompt_bufnr)
  else
    actions.select_tab(prompt_bufnr)
  end
end

local file_picker_mappings = {
  i = {
    ["<C-j>"] = actions.move_selection_next,
    ["<C-k>"] = actions.move_selection_previous,
    ["<CR>"] = select_tab_or_replace_empty,
  },
}

require('telescope').setup({
  defaults = {
    mappings = {
      i = {
        ["<C-j>"] = actions.move_selection_next,
        ["<C-k>"] = actions.move_selection_previous,
      },
    },
  },
  pickers = {
    find_files = { mappings = file_picker_mappings },
    live_grep = { mappings = file_picker_mappings },
    lsp_definitions = { mappings = file_picker_mappings },
    lsp_references = { mappings = file_picker_mappings },
  },
})

-- Keybindings
vim.keymap.set("n", "<leader>h", "gT")
vim.keymap.set("n", "<leader>l", "gt")
vim.keymap.set("n", "gd", "<cmd>Telescope lsp_definitions<CR>")
vim.keymap.set("n", "gr", "<cmd>Telescope lsp_references<CR>")
vim.keymap.set("n", "<C-f>", "<cmd>Telescope find_files<CR>")
vim.keymap.set("n", "<C-d>", "<cmd>Telescope live_grep<CR>")
vim.keymap.set("n", "<leader>:", "<cmd>Telescope commands<CR>")
vim.keymap.set("n", "<leader>;", "<cmd>Telescope command_history<CR>")
