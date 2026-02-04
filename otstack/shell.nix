{pkgs ? import <nixpkgs> {}}:

pkgs.mkShell {
	buildInputs = with pkgs; [
		uv
	];

	shellHook = ''
	unset PYTHONPATH
	unset PYTHONHOME
	unset PYTHONNOUSERSITE
	uv sync
	'';
}