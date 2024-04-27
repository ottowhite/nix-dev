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
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in {
        devShells.default = pkgs.mkShell {

                    # Add buildInputs here i.e packages you want to be available in the dev shell
          buildInputs = (with pkgs; [
                        # Add packages here e.g
                        cowsay
          ]);
                    #  whatever you want to run when entering a dev shell
                    shellHook = ''
                    cowsay "Hello Otto"
                    '';
        };
      }
    );
}

