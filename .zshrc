ZSH_THEME="bira"

# Configuration aliases
alias cff="configure_file flake.nix"
alias cfz="configure_file .zshrc && source $NIX_HOME/.zshrc"
alias cfn="configure_file init.vim"
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
alias x="exit"

function cds {
	cd "$(dirname "$(fzf)")"
}

configure_file() {
        if [ -d $NIX_HOME ]
        then
		git -C $NIX_HOME pull
        else
		git clone git@github.com:ottowhite/nix-dev.git $NIX_HOME 
        fi

	$EDITOR $NIX_HOME/$1
}

nixup() {
	(
		cd $NIX_HOME
		clear
		git --no-pager diff
		git status
		drawline
		echo You\'re in a subshell \for updating your nix repo. After updating, \type x to \return to your original location.
		drawline
		zsh
	)
}

# Quokka commands
drawline() {
        printf %"$(tput cols)"s | tr " " "-"
}

gfza() {
        git add $(git diff --name-only | fzf)
}

rpt() {
        for i in $(seq 100000); (echo Run $i\\n && eval "$@" && sleep 1 && clear)
}

cds() {
        cd "$(dirname "$(fzf)")"
}

remote_exec() {
        machine=$1
        args=${@:2}

        drawline
        echo $machine\> "${@:2}"
        drawline
        ssh $machine -t "${@:2}"
}

# Cluster for each
cfe() {
        cluster=$1

        quokkas=$(
		echo quokka01
		echo quokka02
		echo quokka03
		echo quokka04
	)
        keas=$(
		echo kea01
		echo kea02
		echo kea03
		echo kea04
		echo kea05
		echo kea06
		echo kea07
		echo kea08
	)

        if [ $cluster = "q" ]
        then
                machines=$quokkas
        else
                if [ $cluster = "k" ]
                then

                        machines=$keas
                else
                        # Combined
                        machines="$quokkas\\n$keas"
                fi
        fi

        for machine in $(echo $machines)
        do
                remote_exec $machine ${@:2}
        done
}

cpsu() {
        cluster=$1
        user=$2
        cfe $cluster ps -fjH -u $user
}

cexec() {
        cluster=$1
        machine_number=$2
        if [ $cluster = "q" ]
        then
                machine_prefix=quokka0
        else
                machine_prefix=kea0
        fi

        remote_exec $machine_prefix$machine_number ${@:3}
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

