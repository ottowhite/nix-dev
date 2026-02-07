vim.g.mapleader = " "
vim.opt.number = true
vim.opt.relativenumber = true
vim.keymap.set("n", "<leader>h", "gT")
vim.keymap.set("n", "<leader>l", "gt")
vim.opt.clipboard:append("unnamedplus")

-- Extensions
vim.lsp.enable('ty')
