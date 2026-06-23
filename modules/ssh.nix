{ ... }:

{
  programs.ssh = {
    enable = true;

    # Manage the host blocks below explicitly; don't inject home-manager's
    # default `Host *` block (which forces AddKeysToAgent/ForwardAgent to "no"
    # ahead of our own settings). Everything it set is an OpenSSH default
    # anyway, except the two we override globally below.
    enableDefaultConfig = false;

    settings = {
      # Global defaults applied to every host.
      "*" = {
        ForwardAgent = true;
        AddKeysToAgent = "yes";
      };

      # Imperial DoC jump hosts / gateways.
      opk1 = {
        HostName = "emu3.doc.res.ic.ac.uk";
        User = "ow20";
      };
      opk2 = {
        HostName = "lsds.doc.ic.ac.uk";
        User = "ow20";
      };
      opk3 = {
        HostName = "dingo1.doc.res.ic.ac.uk";
        User = "ow20";
        ProxyJump = "opk1";
      };

      # Any other *.doc.res.ic.ac.uk host reached by its full hostname:
      # default user ow20 and jump via opk1 (emu3). emu3 itself is excluded
      # to avoid a self-referential ProxyJump; it still gets user ow20 below.
      "*.doc.res.ic.ac.uk !emu3.doc.res.ic.ac.uk" = {
        User = "ow20";
        ProxyJump = "opk1";
      };
      "emu3.doc.res.ic.ac.uk" = {
        User = "ow20";
      };
    };
  };
}
