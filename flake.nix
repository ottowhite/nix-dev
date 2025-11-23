# TODO: Add a flag that either drops you into the nix environment or the local environment
# TODO: Add a flag to potentially install all of the packages on host (arch dependent)
# TODO: Synchronise with my VSCode config
# TODO: Synchronise with my Windows keybindings files from the other git repo
# TODO: Synchronise with my mac keybindings from karabiner elements / others

{
  description = "Otto Dev Environment";

  inputs = {
    # This is pinning to the latest stable nixpkgs version
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";

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
          config.allowUnfree = true;
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
            mv temp/oh-my-zsh temp/.oh-my-zsh
            cp -r temp/.oh-my-zsh $out
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
            watch
            mosh
            stgit
            claude-code
          ] ++ [
            nix-dev-deps
            oh-my-zsh-custom
          ]);

          shellHook = 
          ''
            copy_and_own() {
              filename=$1
              src=$2
              dst=$3

              if ! diff -r $src/$filename $dst/$filename >/dev/null 2>&1; then
                echo $filename is different, synchronizing contents.
                sudo rm -rf $dst/$filename
                sudo cp -ra $src/$filename $dst
                sudo chown -R $(whoami) $dst/$filename
              fi
            }
            mkdir_and_own() {
              directory=$1
              if [ ! -d $directory ]; then
                sudo mkdir -p $directory
                sudo chown -R $(whoami) $directory
              fi
            }

            mkdir_and_own ~/.config
            mkdir_and_own ~/.config/zsh
            mkdir_and_own ~/.config/nvim

            echo "Copying configuration files..."
            copy_and_own .zshenv    ${nix-dev-deps}     ~
            copy_and_own .tmux.conf ${nix-dev-deps}     ~
            copy_and_own .zshrc     ${nix-dev-deps}     ~/.config/zsh
            copy_and_own .oh-my-zsh ${oh-my-zsh-custom} ~/.config/zsh
            copy_and_own init.vim   ${nix-dev-deps}     ~/.config/nvim

            export SHELL=${pkgs.zsh}/bin/zsh
            exec zsh
          '';
      };
    }
  );
}

#             echo "Development environment setup complete!"
#             echo "Configuration files have been synced to your home directory."
#             export SHELL=${pkgs.zsh}/bin/zsh

# Old linux bind mounts
# Add these lines before the exit to enter the nix shell
# ---------
# export SHELL=${pkgs.zsh}/bin/zsh
# zsh
# exit
# ---------

# Setup ----
# touch ~/.config/zsh/.zshrc
# touch ~/.config/nvim/init.vim
# touch ~/.zshenv
# touch ~/.tmux.conf
# sudo mount --bind ${nix-dev-deps}/.zshenv ~/.zshenv
# sudo mount --bind ${nix-dev-deps}/.zshrc ~/.config/zsh/.zshrc
# sudo mount --bind ${nix-dev-deps}/init.vim ~/.config/nvim/init.vim
# sudo mount --bind ${nix-dev-deps}/.tmux.conf ~/.tmux.conf
# sudo mount --bind ${oh-my-zsh-custom}/.oh-my-zsh ~/.config/zsh/.oh-my-zsh
# Teardown ----
# packdown = if pkgs.stdenv.isDarwin then '' '' else ''
#          sudo umount ~/.zshenv
#          sudo umount ~/.tmux.conf
#          sudo umount ~/.config/zsh/.zshrc
#          sudo umount ~/.config/nvim/init.vim
#          sudo umount ~/.config/zsh/.oh-my-zsh
# '';
