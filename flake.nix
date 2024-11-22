{
  description = "ude ies development environments";
  inputs.nixpkgs.url = "https://github.com/NixOS/nixpkgs/archive/c69a9bffbecde46b4b939465422ddc59493d3e4d.tar.gz";
  inputs.systems.url = "github:nix-systems/default";
  inputs.flake-utils = {
    url = "github:numtide/flake-utils";
    inputs.systems.follows = "systems";
  };

  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {inherit system; config.allowUnfree = true; };
        python = pkgs.python312.withPackages (ps: with ps; [
        ## these packages and python are not supposed to be used as build
        ## or run dep but just as development tools, that happen
        ## to be written in python
          jedi
          python-lsp-server
          mypy
          rope
          websockets
          pylsp-mypy
          pylsp-rope          
          python-lsp-jsonrpc
        ]);
      in
      {
        devShells.default = pkgs.mkShell {
          packages = with pkgs; [ 
            pre-commit
            commitlint
            git
            # uv will use its own python executables instead of the ones from nix.
            # as mentioned on https://github.com/astral-sh/uv/issues/4450
            # uv will try to write into nix store to install packages otherwise.
            # Using the uv distributed cpython will not work on nixos, though, because
            # of the usual dynamic linking issues. Could possibly try a fhs environment
            # for that. 
            uv
            ruff
            python
            asciidoctor-with-extensions
          ]; 
        };
      }
    );
}
