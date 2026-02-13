{ ... }:

{
  programs.tmux = {
    enable = true;
    prefix = "C-a";
    keyMode = "vi";
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
    '';
  };
}
