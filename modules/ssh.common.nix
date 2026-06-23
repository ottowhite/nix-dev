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

    # Applied to every host.
    settings."*" = {
      ForwardAgent = true;
      AddKeysToAgent = "yes";
    };
  };
}
