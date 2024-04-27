{
  description = "Otto Dev Environment";

  inputs = {
        # This is pinning to the latest stable nixpkgs version
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";

        # This imports the flake-utils library which allows you to build for multiple systems more easily
        # Otherwise you would need to specify the system in the flake.nix
        # devShells.x86_64-linux = nixpkgs.legacyPackages.x86_64-linux.mkShell {
    #   buildInputs = [
    #     # Add necessary packages here
    #   ];
    # };
        # devShells.x86_64-darwin = nixpkgs.legacyPackages.x86_64-darwin.mkShell {
    #   buildInputs = [
    #     # Add necessary packages here
    #   ];
    # };

    # This is another flake that we're importing, can do this arbitrarily with flakes
    flake-utils.url = "github:numtide/flake-utils";
  };

  # These are the inputs that generate the outputs
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let

	# Get the correct packages for each of the architectures we're building for
	# If we didn't 
        pkgs = import nixpkgs {
          inherit system;
        };
      in {
	# Default shell that launches when we write nix develop (devShells -> nix develop)
        devShells.default = pkgs.mkShell {

          # Add buildInputs here i.e packages you want to be available in the dev shell
          packages = (with pkgs; [
            zsh
          ]);
	  # Goes for the cowsay package in nix packages
          # buildInputs = [
          #               pkgs.cowsay
          # ];

          #  whatever you want to run when entering a dev shell
          shellHook = ''
	    ln -s .zshenv ~/.zshenv
	    mkdir -p ~/.config/zsh
	    ln -s .zshrc ~/.config/zshrc
            exec zsh
          '';
        };
      }
    );
}

