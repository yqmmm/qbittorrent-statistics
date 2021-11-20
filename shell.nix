{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = [
    (import ./default.nix { inherit pkgs; })
    # Development dependencies
    pkgs.python3Packages.python-lsp-server
    pkgs.python3Packages.python-lsp-black
    pkgs.python3Packages.python-lsp-jsonrpc
    pkgs.python3Packages.pyls-isort
  ];
}
