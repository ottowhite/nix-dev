{
  description = "Otto's Nix Configuration";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager/master";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, home-manager, ... }:
    let
      # Helper function to create a home configuration
      mkHomeConfiguration = { system, username, homeDirectory }:
        home-manager.lib.homeManagerConfiguration {
          pkgs = import nixpkgs {
            inherit system;
            config.allowUnfree = true;
          };
          extraSpecialArgs = { inherit username homeDirectory; };
          modules = [ ./home.nix ];
        };
    in
    {
      # Home Manager configurations for different machines/users
      homeConfigurations = {
        # NixOS desktop
        "otto@nixos" = mkHomeConfiguration {
          system = "x86_64-linux";
          username = "otto";
          homeDirectory = "/home/otto";
        };

        # Generic Linux server (add more as needed)
        "ow20@server" = mkHomeConfiguration {
          system = "x86_64-linux";
          username = "ow20";
          homeDirectory = "/home/ow20";
        };

        # Example: different user on a server
        # "otto@production" = mkHomeConfiguration {
        #   system = "x86_64-linux";
        #   username = "otto";
        #   homeDirectory = "/home/otto";
        # };

        # Example: macOS
        # "otto@macbook" = mkHomeConfiguration {
        #   system = "aarch64-darwin";
        #   username = "otto";
        #   homeDirectory = "/Users/otto";
        # };
      };

      # Keep the dev shell for backwards compatibility during transition
      devShells = nixpkgs.lib.genAttrs [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ] (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            config.allowUnfree = true;
          };
        in
        {
          default = pkgs.mkShell {
            packages = [
              home-manager.packages.${system}.default
            ];
            shellHook = ''
              echo "Home Manager dev shell"
              echo ""
              echo "To apply your home configuration:"
              echo "  home-manager switch --flake .#ow20@nixos"
              echo ""
              echo "Or for a different machine:"
              echo "  home-manager switch --flake .#ow20@server"
            '';
          };
        }
      );
    };
}
