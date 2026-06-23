{ ... }:

{
  # SSH config applied on every machine (laptops and servers alike).
  programs.ssh = {
    enable = true;

    # Manage host blocks explicitly; don't inject home-manager's default
    # `Host *` block (it would force AddKeysToAgent/ForwardAgent to "no"
    # ahead of our own values). Everything it set is an OpenSSH default
    # anyway, except the two we override globally below.
    enableDefaultConfig = false;

    settings = {
      # Applied to every host.
      "*" = {
        ForwardAgent = true;
        AddKeysToAgent = "yes";
      };

      # Tailscale hosts.
      baby-server.HostName = "100.67.151.15";
      strawberry-shortcake.HostName = "100.115.111.12";

      # Imperial DoC GitLab (lsds) checkout user.
      lsds-check = {
        HostName = "lsds.doc.ic.ac.uk";
        User = "lsds_git";
        IdentityFile = "~/.ssh/id_rsa";
      };

      # Imperial DoC shell gateway.
      shell1 = {
        HostName = "shell1.doc.ic.ac.uk";
        User = "ow20";
        IdentityFile = "~/.ssh/id_rsa";
      };
    };
  };
}
