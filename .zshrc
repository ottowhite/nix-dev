ZSH_THEME="alanpeabody"

# Configuration aliases
alias cfz="$EDITOR $ZDOTDIR/.zshrc && source $ZDOTDIR/.zshrc"
alias cfv="$EDITOR ~/.config/nvim/init.vim"
alias cfi="$EDITOR ~/.config/i3/config"
alias cfa="$EDITOR ~/.config/alacritty/alacritty.yml"
alias cfx="$EDITOR ~/.config/X/.xinitrc"

# Useful aliases
alias gh="alias | grep"
alias idea="~/Applications/idea-IC-231.9011.34/bin/idea.sh"
alias ctl="ssh ow20@shell4.doc.ic.ac.uk"
alias clipboard="xclip -selection c"
alias sx="startx"
alias ka="killall"
alias svm='sudo systemctl start libvirtd && sudo virsh net-start default'
alias bins='f() { pacman -Ql $1 | grep bin };f'# See the binaries provided by a package
alias wp='f() { sudo pacman -Fy && pacman -F $1 };f' # See "which package" provides the binary you are looking for
alias backup='f() { sudo rsync -aAXvv --info=progress2 --delete --exclude /dev/ --exclude /proc/ --exclude /sys/ --exclude /tmp/ --exclude /mnt/ --exclude /usr/tmp/ --exclude /run/ --exclude /media/ --exclude /var/cache/ --exclude /lost+found/ --exclude /home/otto/Downloads/ --exclude /home/otto/.cache/ / $1 };f'
alias startsc='echo "Starting avahi-daemon" && sudo systemctl start avahi-daemon && uxplay && echo "Stopping avahi-daemon" && sudo systemctl stop avahi-daemon.service avahi-daemon.socket'

alias kps="kubectl get pods"
alias kpsf="kubectl get pods | grep "
alias kcs="kubectl config get-contexts "
alias kuc="kubectl config use-context "
alias kcs="kubectl config get-contexts "
alias krmp="kubectl delete pod "
alias kdp="kubectl describe pod "
alias ktail="kubetail "
alias uc="cd $PCF && git diff"

function cds {
	cd "$(dirname "$(fzf)")"
}

function kt {
	osascript -e 'tell application "Terminal" to quit'
}


# Plugins
plugins=(git vi-mode zsh-syntax-highlighting zsh-autosuggestions fzf kubectl)

# Vim mode
export VI_MODE_SET_CURSOR=true
bindkey -v
bindkey -M viins 'ii' vi-cmd-mode
export KEYTIMEOUT=20

# Do ls when change directory
chpwd() ls 

# Start Oh My Zsh, leave at end of file
source $ZSH/oh-my-zsh.sh

