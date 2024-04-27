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

        nix-dev-deps = pkgs.stdenv.mkDerivation {
          name = "ottowhite-nix-dev-deps";
          version = "1";
          src = ./.;
          installPhase = ''
            	    mkdir -p $out
                        cp .zshrc $out
                        cp .zshenv $out
            	  '';
        };
      in
      {
        # Default shell that launches when we write nix develop (devShells -> nix develop)
        devShells.default = pkgs.mkShell {

          # Add buildInputs here i.e packages you want to be available in the dev shell
          packages = (with pkgs; [
            zsh
            zsh-syntax-highlighting
            zsh-autosuggestions
            oh-my-zsh
            fzf
            tree
            neovim
          ] ++ [ nix-dev-deps ]);
          # Goes for the cowsay package in nix packages
          # buildInputs = [
          #               pkgs.cowsay
          # ];

          #  whatever you want to run when entering a dev shell
          shellHook = ''
            mkdir -p ~/.config/zsh
            mkdir -p ~/.config/zsh/.oh-my-zsh
            touch ~/.config/zsh/.zshrc
            touch ~/.zshenv
            sudo mount --bind ${nix-dev-deps}/.zshenv ~/.zshenv
            sudo mount --bind ${nix-dev-deps}/.zshrc ~/.config/zsh/.zshrc
            sudo mount --bind ${pkgs.oh-my-zsh}/share/oh-my-zsh ~/.config/zsh/.oh-my-zsh
            zsh
            echo Hi
            sudo umount ~/.zshenv
            sudo umount ~/.config/zsh/.zshrc
            sudo umount ~/.config/zsh/.oh-my-zsh
          '';
        };
      }
    );
}

