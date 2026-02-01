ZSH_THEME="pygmalion"

# Configuration aliases
alias cff="configure_file flake.nix"
alias cfz="configure_file .zshrc && source $NIX_HOME/.zshrc"
alias cfzenv="configure_file .zshenv && source $NIX_HOME/.zshenv"
alias cfn="configure_file init.vim"
alias cfi="$EDITOR ~/.config/i3/config"
alias cfa="$EDITOR ~/.config/alacritty/alacritty.yml"
alias cfx="$EDITOR ~/.config/X/.xinitrc"
alias cfnix="sudo $EDITOR /etc/nixos/configuration.nix"

# Useful aliases
# alias gh="alias | grep"
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
alias nixmac="sudo launchctl load /Library/LaunchDaemons/org.nixos.nix-daemon.plist"
alias nrb="sudo nixos-rebuild "
alias nrbt="sudo nixos-rebuild test"
alias nrbs="sudo nixos-rebuild switch"
alias getsid="ssh -t root@kangaroo2 id -u "
alias stgcommit="python3 $NIX_HOME/stg-logged-commit.py commit"
alias stguncommit="python3 $NIX_HOME/stg-logged-commit.py uncommit"

alias loadenv='export $(grep -v ^# .env | xargs)'

# "Worktree add"
function wta {
	git worktree add "$1"
	cd "$1"
	direnv allow
	# Force reload
	eval "$(direnv export zsh)"
}

# "Worktree remove"
function wtrm {
	rm -rf "$1"
	git worktree prune
}

# "Claude worktree add"
function cwta {
	wta "$1"
	claude --dangerously-skip-permissions
}

# "Claude worktree add in new tmux pane"
function cwtat {
	worktree_name=$(basename $(realpath "$1"))
	echo $worktree_name
	tmux new-window -n "$worktree_name"
	tmux send-keys "cwta \"$1\"" C-m
}


getshortcode() {
	ssh -t ow20@lsds.doc.ic.ac.uk "cat /etc/passwd | grep -i $1"
}

function crun {
	docker run -v$(pwd):$(pwd) -w $(pwd) --user "$(id -u):$(id -g)" $1 ${@:2}
}

# Enables '?? whats the command to do X', followed by ai generation/explanation for that command
alias '??'='noglob _ask_gpt'
function _ask_gpt() {
    sgpt -s "$*"
}

# Tailscale
function tailwhere {
	tailscale status
	echo
	curl -s ipinfo.io | jq
}
alias tailhome="sudo tailscale set --exit-node="
alias tailbaby="sudo tailscale set --exit-node=$BABY_SERVER_TAILSCALE_IP"
alias tailberry="sudo tailscale set --exit-node=$STRAWBERRY_SHORTCAKE_TAILSCALE_IP"
alias tailkea="sudo tailscale set --exit-node=$KEA04_TAILSCALE_IP"

function chill {
	tailbaby
	sleep 1
	firefox "https://www.netflix.com/browse" "https://www.disneyplus.com/en-gb/home" "https://www.amazon.co.uk/gp/video/storefront?ref_=nav_cs_prime_video" "https://www.bbc.co.uk/iplayer" "https://app.tvtime.com/shows/watchlist" "https://letterboxd.com/0tt/watchlist/"
}


function cds {
	cd "$(dirname "$(fzf)")"
}

function tunnel() {
	ssh -Nf -L $1\:localhost\:$2 $3
}

function untunnel() {
	pkill -f "ssh -Nf -L $1\:localhost\:$2 $3"
}
	
function proxy_up() {
	tunnel 8080 3128 $1
	networksetup -setsecurewebproxy Wi-Fi localhost 8080
}

function proxy_down() {
	untunnel 8080 3128 $1
	networksetup -setsecurewebproxystate Wi-Fi off
}

function oversight() {
	tunnel 3333 3000 komodo01
	ssh -t komodo01 "cd code/oversight && ./start_oversight.sh up"
	open "http://localhost:3333"
}

space() {
	sudo du -sh * -t 1G | sort -nr
	drawline
	sudo du -sh .* -t 1G | sort -nr
}

gdd() {
	git diff $1~ $1
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
		source pull-configs.sh
		clear
		git --no-pager diff
		git status
		drawline
		echo You\'re in a subshell \for updating your nix repo. After updating, \type x to \return to your original location.
		drawline
		zsh
	)
}

drawline() {
        printf %"$(tput cols)"s | tr " " "-"
}

gfza() {
        git add $(git diff --name-only | fzf)
}

gsfe() {
	git submodule foreach $@
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

eval "$(direnv hook zsh)"

# Start Oh My Zsh, leave at end of file
source $ZSH/oh-my-zsh.sh

