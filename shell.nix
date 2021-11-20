{ pkgs ? import <nixpkgs> {} }:

let
  python-with-packages = pkgs.python3.withPackages (p: with p; [
    requests
    python-pushover 
    matplotlib
    # Dev
    python-lsp-server
    python-lsp-black
    python-lsp-jsonrpc
    pyls-isort
  ]);
in

pkgs.mkShell {
  buildInputs = [
    python-with-packages
  ];
}
