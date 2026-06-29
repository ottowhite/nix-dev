{ ... }:

{
  programs.claude-code = {
    enable = true;

    settings = {
      # Always connect Remote Control when an interactive session starts,
      # rather than waiting for the /remote-control command.
      remoteControlAtStartup = true;

      tui = "fullscreen";
      editorMode = "vim";
      skipDangerousModePermissionPrompt = true;
      agentPushNotifEnabled = true;
    };
  };
}
