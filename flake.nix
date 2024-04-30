{
  description = "Otto Dev Environment";

  inputs = {
    # This is pinning to the latest stable nixpkgs version
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";

    # This imports the flake-utils library which allows you to build for multiple systems more easily
    # Otherwise you would need to specify the system in the flake.nix
    # devShells.x86_64-linux = nixpkgs.legacyPackages.x86_64-linux.mkShell {
    #   buildInputs = [
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
            cp .tmux.conf $out
            cp init.vim $out
          '';
        };

        oh-my-zsh-custom = pkgs.stdenv.mkDerivation {
          name = "ottowhite-oh-my-zsh";
          version = "1";
          src = ./.;

          buildInputs = [
            pkgs.oh-my-zsh
            pkgs.zsh-syntax-highlighting
            pkgs.zsh-autosuggestions
          ];

          buildPhase = ''
            mkdir -p temp/oh-my-zsh/custom/plugins/zsh-syntax-highlighting
            mkdir -p temp/oh-my-zsh/custom/plugins/zsh-autosuggestions
            cp -r ${pkgs.oh-my-zsh}/share/oh-my-zsh temp
            cp -r ${pkgs.zsh-syntax-highlighting}/share/zsh-syntax-highlighting temp/oh-my-zsh/custom/plugins/
            cp -r ${pkgs.zsh-autosuggestions}/share/zsh-autosuggestions temp/oh-my-zsh/custom/plugins/
            cp zsh-syntax-highlighting.plugin.zsh temp/oh-my-zsh/custom/plugins/zsh-syntax-highlighting
            cp zsh-autosuggestions.plugin.zsh temp/oh-my-zsh/custom/plugins/zsh-autosuggestions
            mkdir -p $out
            cp -r temp/oh-my-zsh $out
          '';
        };
      in
      {
        devShells.default = pkgs.mkShell {
          packages = (with pkgs; [
            zsh
            fzf
            tree
            neovim
            tmux
          ] ++ [
            nix-dev-deps
            oh-my-zsh-custom
          ]);

	  shellHook = 
	    let
	      setup = if pkgs.stdenv.isDarwin then ''
		copy_and_own() {
		  sudo cp -ra $1 $2
		  sudo chown -R $(whoami) $2
		}

                copy_and_own ${nix-dev-deps}/.zshenv ~/.zshenv
                copy_and_own ${nix-dev-deps}/.zshrc ~/.config/zsh/.zshrc
                copy_and_own ${nix-dev-deps}/init.vim ~/.config/nvim/init.vim
                copy_and_own ${nix-dev-deps}/.tmux.conf ~/.tmux.conf
                copy_and_own ${oh-my-zsh-custom}/oh-my-zsh ~/.config/zsh/.oh-my-zsh
	      '' else ''
                touch ~/.config/zsh/.zshrc
                touch ~/.config/nvim/init.vim
                touch ~/.zshenv
                touch ~/.tmux.conf
                sudo mount --bind ${nix-dev-deps}/.zshenv ~/.zshenv
                sudo mount --bind ${nix-dev-deps}/.zshrc ~/.config/zsh/.zshrc
                sudo mount --bind ${nix-dev-deps}/init.vim ~/.config/nvim/init.vim
                sudo mount --bind ${nix-dev-deps}/.tmux.conf ~/.tmux.conf
                sudo mount --bind ${oh-my-zsh-custom}/oh-my-zsh ~/.config/zsh/.oh-my-zsh
	      '';

	      packdown = if pkgs.stdenv.isDarwin then '' '' else ''
                sudo umount ~/.zshenv
                sudo umount ~/.tmux.conf
                sudo umount ~/.config/zsh/.zshrc
                sudo umount ~/.config/nvim/init.vim
                sudo umount ~/.config/zsh/.oh-my-zsh
	      '';
            in
              ''
	        ${setup}
                export SHELL=${pkgs.zsh}/bin/zsh
                zsh
	        ${packdown}
                exit
              '';
        };
      }
    );
}

