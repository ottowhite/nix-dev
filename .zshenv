export XDG_CONFIG_HOME=$HOME/.config
export XDG_DATA_HOME=$XDG_CONFIG_HOME/local/share
export XDG_CACHE_HOME=$XDG_CONFIG_HOME/cache
export SCM="$XDG_CONFIG_HOME/scm"
export PCF="$SCM/personal-config-files"

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

# Maven home
export M2_HOME=/usr/share/maven

# Useful directories
export TRASH=$HOME"/.local/share/Trash/files"
export WINDOWS_HOME="/mnt/c/Users/OttoWhite"

