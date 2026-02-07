{ config, pkgs, lib, username, homeDirectory, ... }:

{
  home.username = username;
  home.homeDirectory = homeDirectory;
  home.stateVersion = "24.05";

  # Let Home Manager manage itself
  programs.home-manager.enable = true;

  # Packages to install
  home.packages = with pkgs; [
    fzf
    tree
    tmux
    watch
    mosh
    stgit
    direnv
    nix-direnv
    claude-code
    github-copilot-cli
    graphite-cli
    shell-gpt
    opkssh
    nodejs_24
    jq
    uv
  ];

  # Zsh configuration
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
      XDG_CONFIG_HOME = "${homeDirectory}/.config";
      XDG_DATA_HOME = "${homeDirectory}/.config/local/share";
      XDG_CACHE_HOME = "${homeDirectory}/.config/cache";
      SCM = "${homeDirectory}/.config/scm";
      PCF = "${homeDirectory}/.config/scm/personal-config-files";
      NIX_HOME = "${homeDirectory}/nix-dev";
      EDITOR = "nvim";
      VISUAL = "nvim";
      TRASH = "${homeDirectory}/.local/share/Trash/files";
      BABY_SERVER_TAILSCALE_IP = "100.67.151.15";
      STRAWBERRY_SHORTCAKE_TAILSCALE_IP = "100.115.111.12";
      KEA04_TAILSCALE_IP = "100.67.99.38";
      VI_MODE_SET_CURSOR = "true";
      KEYTIMEOUT = "20";
    };

    shellAliases = {
      # Configuration aliases
      cff = "configure_file flake.nix";
      cfz = "configure_file .zshrc && source $NIX_HOME/.zshrc";
      cfzenv = "configure_file .zshenv && source $NIX_HOME/.zshenv";
      cfn = "configure_file init.vim";
      cfi = "$EDITOR ~/.config/i3/config";
      cfa = "$EDITOR ~/.config/alacritty/alacritty.yml";
      cfx = "$EDITOR ~/.config/X/.xinitrc";
      cfnix = "sudo $EDITOR /etc/nixos/configuration.nix";

      # Useful aliases
      idea = "~/Applications/idea-IC-231.9011.34/bin/idea.sh";
      ctl = "ssh ow20@shell4.doc.ic.ac.uk";
      clipboard = "xclip -selection c";
      sx = "startx";
      ka = "killall";
      svm = "sudo systemctl start libvirtd && sudo virsh net-start default";
      x = "exit";
      nixmac = "sudo launchctl load /Library/LaunchDaemons/org.nixos.nix-daemon.plist";
      nrb = "sudo nixos-rebuild ";
      nrbt = "sudo nixos-rebuild test";
      nrbs = "sudo nixos-rebuild switch";
      getsid = "ssh -t root@kangaroo2 id -u ";
      stgcommit = "python3 $NIX_HOME/stg-logged-commit.py commit";
      stguncommit = "python3 $NIX_HOME/stg-logged-commit.py uncommit";
      loadenv = "export $(grep -v ^# .env | xargs)";
      tailhome = "sudo tailscale set --exit-node=";
      tailbaby = "sudo tailscale set --exit-node=$BABY_SERVER_TAILSCALE_IP";
      tailberry = "sudo tailscale set --exit-node=$STRAWBERRY_SHORTCAKE_TAILSCALE_IP";
      tailkea = "sudo tailscale set --exit-node=$KEA04_TAILSCALE_IP";
      "??" = "noglob _ask_gpt";
    };

    initContent = ''
      # Vim mode
      bindkey -v
      bindkey -M viins 'ii' vi-cmd-mode

      # Do ls when change directory
      chpwd() ls

      # Enable direnv
      eval "$(direnv hook zsh)"

      # Custom functions
      function otstack() {
        local repo_name=$(git remote get-url origin 2>/dev/null | sed -E 's|.*github\.com[:/]||; s|\.git$||')
        local repo_path=$(pwd)
        if [[ -n "$repo_name" ]]; then
          uv --directory $NIX_HOME/otstack run main.py "$1" --repo "$repo_name" --path "$repo_path" "''${@:2}"
        else
          uv --directory $NIX_HOME/otstack run main.py "$@"
        fi
      }

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

      gsfe() {
        git submodule foreach $@
      }

      bins() {
        pacman -Ql $1 | grep bin
      }

      wp() {
        sudo pacman -Fy && pacman -F $1
      }

      backup() {
        sudo rsync -aAXvv --info=progress2 --delete --exclude /dev/ --exclude /proc/ --exclude /sys/ --exclude /tmp/ --exclude /mnt/ --exclude /usr/tmp/ --exclude /run/ --exclude /media/ --exclude /var/cache/ --exclude /lost+found/ --exclude /home/otto/Downloads/ --exclude /home/otto/.cache/ / $1
      }

      startsc() {
        echo "Starting avahi-daemon"
        sudo systemctl start avahi-daemon
        uxplay
        echo "Stopping avahi-daemon"
        sudo systemctl stop avahi-daemon.service avahi-daemon.socket
      }
    '';
  };

  # Tmux configuration
  programs.tmux = {
    enable = true;
    prefix = "C-a";
    extraConfig = ''
      # Vim keybindings for window navigation
      bind h select-pane -L
      bind j select-pane -D
      bind k select-pane -U
      bind l select-pane -R

      # Rename window with r
      bind-key r command-prompt -I "#W" "rename-window '%%'"

      # Stop windows renaming themselves
      set-option -g allow-rename off

      bind B source-file ~/.tmux/debug

      bind X setw synchronize-panes on
    '';
  };

  # Neovim configuration
  programs.neovim = {
    enable = true;
    defaultEditor = true;

    plugins = with pkgs.vimPlugins; [
      nvim-lspconfig
    ];

    initLua = ''
      vim.g.mapleader = " "
      vim.opt.number = true
      vim.opt.relativenumber = true
      vim.keymap.set("n", "<leader>h", "gT")
      vim.keymap.set("n", "<leader>l", "gt")
      vim.opt.clipboard:append("unnamedplus")

      -- Extensions
      vim.lsp.enable('ty')
    '';
  };

  # Direnv integration
  programs.direnv = {
    enable = true;
    nix-direnv.enable = true;
  };

  # FZF integration
  programs.fzf = {
    enable = true;
    enableZshIntegration = true;
  };

  # Ensure .claude directory exists
  home.file.".claude/.keep".text = "";
}
