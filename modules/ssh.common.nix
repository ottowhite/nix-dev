{ lib, isLaptop ? false, ... }:

let
  # Imperial DoC cluster aliases: <prefix><n> -> <host><nn>.doc.res.ic.ac.uk
  # (hosts are zero-padded to two digits, e.g. ko3 -> komodo03).
  #
  # These are internal research hosts: reaching them requires jumping via opk1
  # (emu3), the same ProxyJump the `*.doc.res.ic.ac.uk` wildcard in
  # ssh.local.nix applies. Because `ssh ko1` matches Host against the alias
  # `ko1` (not the resolved hostname), that wildcard no longer fires, so we set
  # ProxyJump here explicitly. opk1 only exists on laptops (ssh.local.nix), so
  # gate it on isLaptop to avoid a dangling ProxyJump on other machines.
  mkCluster = prefix: host: count:
    builtins.listToAttrs (map (i: {
      name = "${prefix}${toString i}";
      value = {
        HostName = "${host}${lib.fixedWidthNumber 2 i}.doc.res.ic.ac.uk";
        User = "ow20";
      } // lib.optionalAttrs isLaptop { ProxyJump = "opk1"; };
    }) (lib.range 1 count));
in
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

      boogle = {
        HostName = "135.181.56.36";
        User = "ow20";
        ControlMaster = "auto";
      };

      emu3_ansible = {
        HostName = "emu3.doc.res.ic.ac.uk";
        User = "ansible";
      };

      e3 = {
        HostName = "emu3.doc.res.ic.ac.uk";
        User = "ow20";
      };

      lsds = {
        HostName = "lsds.doc.ic.ac.uk";
        User = "ow20";
      };
    }
    # ko1..ko4, ke1..ke8, q1..q5 -> komodo/kea/quokka NN.doc.res.ic.ac.uk
    // mkCluster "ko" "komodo" 4
    // mkCluster "ke" "kea" 8
    // mkCluster "q" "quokka" 5;
  };
}
