{ pkgs, lib, isLaptop ? false, ... }:

{
  programs.claude-code = {
    enable = true;

    # Make Playwright browser automation available to every Claude session.
    # The nixpkgs `playwright-mcp` wrapper pins its own matching browser set via
    # PLAYWRIGHT_BROWSERS_PATH, so no npx/download/version-skew on NixOS. The
    # home-manager module bakes this into a plugin loaded via --plugin-dir for
    # all sessions, so no per-project .mcp.json or approval prompt is needed.
    mcpServers.playwright = {
      type = "stdio";
      command = "${pkgs.playwright-mcp}/bin/playwright-mcp";
      # Headless everywhere except laptops, which have a display.
      args = [ "--isolated" ] ++ lib.optional (!isLaptop) "--headless";
    };

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
