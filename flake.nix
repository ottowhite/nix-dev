{
  description = "Otto's Nix Configuration";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager/master";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = { nixpkgs, home-manager, ... }:
    let
      mkHomeConfiguration = { system, username, homeDirectory, isLaptop ? false }:
        home-manager.lib.homeManagerConfiguration {
          pkgs = import nixpkgs {
            inherit system;
            config.allowUnfree = true;
          };
          extraSpecialArgs = {
            inherit username homeDirectory isLaptop;
          };
          modules = [ ./home.nix ];
        };
    in
    {
      homeConfigurations = {
        "ottowhite@Ottos-MacBook-Pro.local" = mkHomeConfiguration {
          system = "aarch64-darwin";
          username = "ottowhite";
          homeDirectory = "/Users/ottowhite";
          isLaptop = true;
        };
        "otto@nixos" = mkHomeConfiguration {
          system = "x86_64-linux";
          username = "otto";
          homeDirectory = "/home/otto";
          isLaptop = true;
        };
        "ow20@server" = mkHomeConfiguration {
          system = "x86_64-linux";
          username = "ow20";
          homeDirectory = "/home/ow20";
        };
        "ansible@server" = mkHomeConfiguration {
          system = "x86_64-linux";
          username = "ansible";
          homeDirectory = "/home/ansible";
        };
        "ow20@csgserver" = mkHomeConfiguration {
          system = "x86_64-linux";
          username = "ow20";
          homeDirectory = "/homes/ow20";
        };
      };
    };
}
