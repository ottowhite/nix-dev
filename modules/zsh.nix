{ config, homeDirectory, ... }:

{
  programs.zsh = {
    enable = true;
    dotDir = "${config.xdg.configHome}/zsh";

    oh-my-zsh = {
      enable = true;
      theme = "pygmalion";
      plugins = [ "git" "vi-mode" "fzf" "kubectl" ];
    };

    syntaxHighlighting.enable = true;
    autosuggestion.enable = true;

    history = {
      path = "${config.xdg.configHome}/zsh/.zhistory";
      size = 10000;
      save = 10000;
    };

    sessionVariables = {
      NIX_HOME = "${homeDirectory}/nix-dev";
      BABY_SERVER_TAILSCALE_IP = "100.67.151.15";
      STRAWBERRY_SHORTCAKE_TAILSCALE_IP = "100.115.111.12";
      KEA04_TAILSCALE_IP = "100.81.155.10";
      VI_MODE_SET_CURSOR = "true";
      KEYTIMEOUT = "20";
    };

    shellAliases = {
      hm = "NIX_CONFIG='experimental-features = nix-command flakes' nix run home-manager/master --";
      cff = "configure_file flake.nix";
      cfhome = "configure_file home.nix";
      getsid = "ssh -t root@kangaroo2 id -u ";
      sx = "startx";
      ka = "killall";
      svm = "sudo systemctl start libvirtd && sudo virsh net-start default";
      x = "exit";
      nixmac = "sudo launchctl load /Library/LaunchDaemons/org.nixos.nix-daemon.plist";
      nrbt = "sudo nixos-rebuild test";
      nrbs = "sudo nixos-rebuild switch";
      tailhome = "sudo tailscale set --exit-node=";
      tailbaby = "sudo tailscale set --exit-node=$BABY_SERVER_TAILSCALE_IP";
      tailberry = "sudo tailscale set --exit-node=$STRAWBERRY_SHORTCAKE_TAILSCALE_IP";
      tailkea = "sudo tailscale set --exit-node=$KEA04_TAILSCALE_IP";
      gsur="git submodule update --init --recursive";
      gsda="git submodule deinit --all";
      "??" = "noglob _ask_gpt";
    };

    initContent = ''
      # On macOS, /etc/zprofile runs path_helper which reorders PATH and pushes
      # Nix paths behind /usr/bin. Re-prepend so Nix-installed tools (e.g. git)
      # win over Apple stubs that depend on DEVELOPER_DIR.
      if [[ "$OSTYPE" == darwin* ]]; then
        typeset -U path PATH
        path=("$HOME/.nix-profile/bin" "/nix/var/nix/profiles/default/bin" $path)
        export PATH
      fi

      # Source and export environment variables from ~/.env if it exists
      if [[ -f ~/.env ]]; then
        set -a  # automatically export all variables
        source ~/.env
        set +a
      fi

      prdiff() {
          git diff --numstat main...HEAD \
              | awk '{a=($1=="-")?0:$1; d=($2=="-")?0:$2; print a+d, a, d, $3}' \
              | sort -rn \
              | awk 'BEGIN{G="\033[32m";R="\033[31m";B="\033[1m";N="\033[0m"}
                     {at = $2 ? G "+" $2 N : ""; la = $2 ? length($2)+1 : 0
                      dt = $3 ? R "-" $3 N : ""; ld = $3 ? length($3)+1 : 0
                      printf "%s%6d%s  %s%*s%s%*s%s\n", B,$1,N, at,8-la,"", dt,8-ld,"", $4}'
      }

      # Vim mode
      bindkey -v
      bindkey -M viins 'ii' vi-cmd-mode

      # Do ls when change directory
      chpwd() ls

      # "Worktree add"
      function wta {
        git worktree add "$1"
        cd "$1"
        direnv allow
        eval "$(direnv export zsh)"
      }

      # "Worktree remove"
      function wtrm {
        rm -rf "$1"
        git worktree prune
	git branch -D $(basename "$1")
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
        tmux send-keys "cwta $1" C-m
      }

      getshortcode() {
        ssh -t ow20@lsds.doc.ic.ac.uk "cat /etc/passwd | grep -i $1"
      }

      function crun {
        docker run -v$(pwd):$(pwd) -w $(pwd) --user "$(id -u):$(id -g)" $1 ''${@:2}
      }

      function _ask_gpt() {
        sgpt -s "$*"
      }

      function tailwhere {
        tailscale status
        echo
        curl -s ipinfo.io | jq
      }

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

      space() {
        sudo du -sh * -t 1G | sort -nr
        drawline
        sudo du -sh .* -t 1G | sort -nr
      }

      gdd() {
        git diff $1~ $1
      }

      pull_nix_dev() {
        if [ -d $NIX_HOME ]; then
          git -C $NIX_HOME pull
        else
          git clone git@github.com:ottowhite/nix-dev.git $NIX_HOME
        fi
      }

      configure_file() {

        pull_nix_dev

	(
	  cd $NIX_HOME && $EDITOR $1
	)
        
      }

      nixup() {
        (
          cd $NIX_HOME
          source pull-configs.sh
          clear
          git --no-pager diff
          git status
          drawline
          echo You\'re in a subshell for updating your nix repo. After updating, type x to return to your original location.
          drawline
          zsh
        )
      }

      nixrefresh() {
        nix develop --refresh github:ottowhite/nix-dev --extra-experimental-features nix-command --extra-experimental-features flakes
      }

      drawline() {
        printf %"$(tput cols)"s | tr " " "-"
      }

      gfza() {
        git add $(git diff --name-only | fzf)
      }

      nixsetup() {
        echo ""
        echo "=========================================="
        echo "  Nix + Home Manager Setup Instructions"
        echo "=========================================="
        echo ""
        echo "Step 1: Install Nix (multi-user)"
        echo "--------------------------------"
        echo ""
        echo "  sh <(curl -L https://nixos.org/nix/install) --daemon"
        echo ""
        echo "  Then log out and back in, or run:"
        echo ""
        echo "  . /etc/profile"
        echo ""
        echo "Step 2: Apply Home Manager configuration"
        echo "-----------------------------------------"
        echo ""
        echo "  nix run home-manager/master -- switch \\"
        echo "    --flake github:ottowhite/nix-dev#USERNAME@MACHINE \\"
        echo "    -b backup \\"
        echo "    --extra-experimental-features 'nix-command flakes'"
        echo ""
        echo "  Replace USERNAME@MACHINE with your config, e.g.:"
        echo "    ow20@nixos   - NixOS desktop"
        echo "    ow20@server  - Generic Linux server"
        echo ""
        echo "That's it! Your shell, neovim, tmux, and tools are now configured."
        echo ""
        echo "=========================================="
        echo "  Updating an existing installation"
        echo "=========================================="
        echo ""
        echo "  home-manager switch \\"
        echo "    --flake github:ottowhite/nix-dev#USERNAME@MACHINE \\"
        echo "    --extra-experimental-features 'nix-command flakes'"
        echo ""
      }

      hms() {
	pull_nix_dev

        local config="$1"
        if [[ -z "$config" ]]; then
          local user=$(whoami)
          local host=$(hostname)
          if [[ "$user" == "ow20" && "$HOME" == "/home/ow20" ]]; then
            config="ow20@server"
          else
            config="$user@$host"
          fi
        fi
        NIX_CONFIG="experimental-features = nix-command flakes" \
          nix run home-manager/master -- switch --flake "$NIX_HOME#$config" \
          && exec zsh
      }

      hmsr() {
        local config="$1"
        if [[ -z "$config" ]]; then
          local user=$(whoami)
          local host=$(hostname)
          if [[ "$user" == "ow20" && "$HOME" == "/home/ow20" ]]; then
            config="ow20@server"
          else
            config="$user@$host"
          fi
        fi
        NIX_CONFIG="experimental-features = nix-command flakes" \
          nix run home-manager/master -- switch --refresh --flake github:ottowhite/nix-dev#$config
      }

      # "Nix flake update": update flake.lock, review the diff, then prompt to
      # commit+push with a fixed message or roll the change back.
      nfu() {
        pull_nix_dev

        (
          cd $NIX_HOME || return 1

          NIX_CONFIG="experimental-features = nix-command flakes" \
            nix flake update || return 1

          if git diff --quiet flake.lock; then
            echo "flake.lock is already up to date, nothing to commit."
            return 0
          fi

          git add flake.lock
          clear
          git --no-pager diff --staged flake.lock
          drawline
          git status
          drawline

          local commit_msg="nix: update flake.lock"
          echo -n "Commit and push with message \"$commit_msg\"? [y/N] "
          read -r reply
          if [[ "$reply" =~ ^[Yy]$ ]]; then
            git commit -m "$commit_msg" && git push
          else
            echo "Rolling back flake.lock..."
            git restore --staged flake.lock
            git checkout -- flake.lock
          fi
        )
      }

      # Stable ssh-agent socket for forwarded (remote) sessions. A forwarded agent
      # socket dies with the SSH connection that created it, and tmux panes keep the
      # old path — so a dropped connection leaves agent auth broken until you open a
      # fresh pane. Pin a fixed symlink that each genuine login repoints at the live
      # socket; shells always read the fixed path, so reconnecting repairs every
      # existing pane. tmux panes with a dead socket fail the -S test and skip the
      # relink, so they never clobber the symlink with a stale path.
      if [ -n "$SSH_CONNECTION" ]; then
        if [ -S "$SSH_AUTH_SOCK" ] && [ "$SSH_AUTH_SOCK" != "$HOME/.ssh/ssh_auth_sock" ]; then
          ln -sf "$SSH_AUTH_SOCK" "$HOME/.ssh/ssh_auth_sock"
        fi
        export SSH_AUTH_SOCK="$HOME/.ssh/ssh_auth_sock"
      fi
    '';
  };
}
