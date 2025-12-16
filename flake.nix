{
  description = "Otto's Bedroom";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
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
            cp CLAUDE.md $out
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
            mkdir -p temp/oh-my-zsh/custom/plugins
            cp -rL ${pkgs.oh-my-zsh}/share/oh-my-zsh temp
            cp -rL ${pkgs.zsh-syntax-highlighting}/share/zsh-syntax-highlighting temp/oh-my-zsh/custom/plugins/
            cp -rL ${pkgs.zsh-autosuggestions}/share/zsh-autosuggestions temp/oh-my-zsh/custom/plugins/
            chmod -R u+w temp
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
            direnv
	    nix-direnv
	    claude-code
	    shell-gpt
	    opkssh
	    nodejs_24
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

            copy_and_own_with_confirmation() {
              filename=$1
              src=$2
              dst=$3

              src_file="$src/$filename"
              dst_file="$dst/$filename"

              # If destination file doesn't exist, just copy it
              if [ ! -f "$dst_file" ]; then
                echo "$filename does not exist at $dst_file, copying..."
                sudo cp -ra "$src_file" "$dst"
                sudo chown -R $(whoami) "$dst_file"
                return
              fi

              # If files are the same, nothing to do
              if diff -q "$src_file" "$dst_file" >/dev/null 2>&1; then
                return
              fi

              # Files are different - show diff and ask for confirmation
              echo ""
              echo "========================================"
              echo "WARNING: $filename files are different!"
              echo "========================================"
              echo ""
              echo "Diff between $src_file and $dst_file:"
              echo "----------------------------------------"
              diff --color=always "$dst_file" "$src_file" || true
              echo "----------------------------------------"
              echo ""
              echo "If there are changes that you want in nix, run nixup to add them"
              echo ""
              echo -n "Do you want to overwrite $dst_file with the version from nix-dev-deps? [y/N]: "
              read -r response
              case "$response" in
                [yY][eE][sS]|[yY])
                  echo "Overwriting $dst_file..."
                  sudo rm -rf "$dst_file"
                  sudo cp -ra "$src_file" "$dst"
                  sudo chown -R $(whoami) "$dst_file"
                  sudo chmod 770 "$dst_file"
                  echo "Done."
                  ;;
                *)
                  echo "Skipping overwrite of $dst_file."
                  ;;
              esac
            }

            mkdir_and_own() {
              directory=$1
              if [ ! -d $directory ]; then
                sudo mkdir -p $directory
                sudo chown -R $(whoami) $directory
              fi
            }

            mkdir_and_own ~/.claude
            mkdir_and_own ~/.config
            mkdir_and_own ~/.config/zsh
            mkdir_and_own ~/.config/nvim

            # NOTE: This kind of copy is recommended for configuration files that are changed indirectly by other applications
            copy_and_own_with_confirmation CLAUDE.md ${nix-dev-deps} ~/.claude

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

# The way to do bind mounts for linux, and architecture dependent execution

# touch ~/.config/zsh/.zshrc
# touch ~/.config/nvim/init.vim
# touch ~/.zshenv
# touch ~/.tmux.conf
# sudo mount --bind ${nix-dev-deps}/.zshenv ~/.zshenv
# sudo mount --bind ${nix-dev-deps}/.zshrc ~/.config/zsh/.zshrc
# sudo mount --bind ${nix-dev-deps}/init.vim ~/.config/nvim/init.vim
# sudo mount --bind ${nix-dev-deps}/.tmux.conf ~/.tmux.conf
# sudo mount --bind ${oh-my-zsh-custom}/.oh-my-zsh ~/.config/zsh/.oh-my-zsh

# Bind mounts teardown

# packdown = if pkgs.stdenv.isDarwin then '' '' else ''
#          sudo umount ~/.zshenv
#          sudo umount ~/.tmux.conf
#          sudo umount ~/.config/zsh/.zshrc
#          sudo umount ~/.config/nvim/init.vim
#          sudo umount ~/.config/zsh/.oh-my-zsh
# '';
