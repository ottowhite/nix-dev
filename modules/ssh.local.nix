{ ... }:

{
  programs.ssh.settings = {
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
    "*.doc.res.ic.ac.uk *.doc.ic.ac.uk !emu3.doc.res.ic.ac.uk !shell1.doc.res.ic.ac.uk" = {
      User = "ow20";
      ProxyJump = "opk1";
    };
  };
}
