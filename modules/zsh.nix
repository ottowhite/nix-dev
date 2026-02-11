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
      KEA04_TAILSCALE_IP = "100.67.99.38";
      VI_MODE_SET_CURSOR = "true";
      KEYTIMEOUT = "20";
    };

    shellAliases = {
      cff = "configure_file flake.nix";
      cfhome = "configure_file home.nix";
      getsid = "ssh -t root@kangaroo2 id -u ";
      sx = "startx";
      ka = "killall";
      svm = "sudo systemctl start libvirtd && sudo virsh net-start default";
      x = "exit";
      nixmac = "sudo launchctl load /Library/LaunchDaemons/org.nixos.nix-daemon.plist";
      nrb = "sudo nixos-rebuild ";
      nrbt = "sudo nixos-rebuild test";
      nrbs = "sudo nixos-rebuild switch";
      tailhome = "sudo tailscale set --exit-node=";
      tailbaby = "sudo tailscale set --exit-node=$BABY_SERVER_TAILSCALE_IP";
      tailberry = "sudo tailscale set --exit-node=$STRAWBERRY_SHORTCAKE_TAILSCALE_IP";
      tailkea = "sudo tailscale set --exit-node=$KEA04_TAILSCALE_IP";
      "??" = "noglob _ask_gpt";
    };

    initContent = ''
      # Source and export environment variables from ~/.env if it exists
      if [[ -f ~/.env ]]; then
        set -a  # automatically export all variables
        source ~/.env
        set +a
      fi

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

      configure_file() {
        if [ -d $NIX_HOME ]; then
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
	  nix flake update otstack
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
        home-manager switch --flake "$NIX_HOME#$config" --extra-experimental-features 'nix-command flakes' \
          && exec zsh
      }
    '';
  };
}
