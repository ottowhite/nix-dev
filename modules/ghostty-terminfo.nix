{ pkgs, lib, ... }:

# Install Ghostty's terminfo so remote shells render correctly when connecting
# from a Ghostty terminal, which sets TERM=xterm-ghostty. Without this entry in
# the terminfo database, programs fall back to a generic terminal and misrender.
#
# The compiled entries are linked into ~/.terminfo, which ncurses always
# searches first — so this needs no root access and no TERMINFO_DIRS tweaking.
#
# Linux-only: macOS gets the terminfo from Ghostty.app itself, and the ghostty
# package does not build on Darwin (so referencing it there would error).
lib.mkIf pkgs.stdenv.hostPlatform.isLinux {
  home.file = {
    ".terminfo/x/xterm-ghostty".source =
      "${pkgs.ghostty.terminfo}/share/terminfo/x/xterm-ghostty";
    ".terminfo/g/ghostty".source =
      "${pkgs.ghostty.terminfo}/share/terminfo/g/ghostty";
  };
}
