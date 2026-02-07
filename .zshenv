export XDG_CONFIG_HOME=$HOME/.config
export XDG_DATA_HOME=$HOME/.local/share
export XDG_CACHE_HOME=$XDG_CONFIG_HOME/cache
export SCM="$XDG_CONFIG_HOME/scm"
export PCF="$SCM/personal-config-files"
export PATH="$PATH:$HOME/.local/bin"

export NIX_HOME="$HOME/nix-dev"

# editor
export EDITOR="nvim"
export VISUAL="nvim"

# zsh
export ZDOTDIR="$XDG_CONFIG_HOME/zsh"
export ZSH="$ZDOTDIR/.oh-my-zsh"
export ZSH_CUSTOM="$ZSH/custom"
export HISTFILE="$ZDOTDIR/.zhistory"    # History filepath
export HISTSIZE=10000                   # Maximum events for internal history
export SAVEHIST=10000                   # Maximum events in history file

# tailscale
export BABY_SERVER_TAILSCALE_IP=100.67.151.15
export STRAWBERRY_SHORTCAKE_TAILSCALE_IP=100.115.111.12
export KEA04_TAILSCALE_IP=100.67.99.38

# Useful directories
export TRASH=$HOME"/.local/share/Trash/files"

