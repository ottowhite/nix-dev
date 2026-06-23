{ ... }:

{
  programs.ssh = {
    enable = true;
    # Stops blocking ForwardAgent and AddKeysToAgent by default
    enableDefaultConfig = false;

    settings = {
      "*" = {
        ForwardAgent = true;
        AddKeysToAgent = "yes";
      };

      lsds-git = {
        HostName = "lsds.doc.ic.ac.uk";
        User = "lsds_git";
        IdentityFile = "~/.ssh/id_rsa";
      };

      shell1 = {
        HostName = "shell1.doc.ic.ac.uk";
        User = "ow20";
      };

      baby-server.HostName = "100.67.151.15";
      strawberry-shortcake.HostName = "100.115.111.12";
    };
  };
}
