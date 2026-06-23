{ ... }:

{
  # Laptop-only SSH config: assumes we are OUTSIDE the DoC network and must
  # tunnel in via a gateway. Do NOT import this on cluster-internal machines,
  # where the ProxyJump below would add a wrong/extra hop (or self-loop).
  programs.ssh.settings = {
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
}
