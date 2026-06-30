{ pkgs, ... }:

{
  programs.tmux = {
    enable = true;
    prefix = "C-a";
    keyMode = "vi";
    plugins = with pkgs.tmuxPlugins; [
      {
        # Powerline theme; tmux-power accepts a custom hex for an exact shade.
        plugin = power-theme;
        # tmux-power styles the center bar via the deprecated `status-bg`, which
        # tmux 3.6 ignores (leaving it default green), so set status-style to the
        # theme's own background/foreground (G04/G10) ourselves.
        extraConfig = ''
          set -g @tmux_power_theme '#0099ff'
          set -g status-style 'bg=#262626,fg=#626262'
        ''; # electric blue
      }
    ];
    extraConfig = ''
      # Send prefix to nested tmux
      bind-key C-a send-prefix

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

      # Allow OSC 52 clipboard to pass through to outer terminal
      set -g set-clipboard on
      set -g allow-passthrough on
    '';
  };
}
