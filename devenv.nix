{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

let
  unstablePkgs = import inputs.nixpkgs-unstable { system = pkgs.stdenv.system; };
in
{

  packages =
    let
      p3 = unstablePkgs.python312Packages;
    in
    [
      pkgs.git
      unstablePkgs.mypy
      p3.python-lsp-server
      p3.pluggy
      p3.pylsp-rope
      p3.pylsp-mypy
      unstablePkgs.asciidoctor
      unstablePkgs.uv
      unstablePkgs.ruff
    ];

  languages.python = {
    enable = true;
    package = unstablePkgs.python312;
    uv.enable = true;
    uv.package = unstablePkgs.uv;
    uv.sync.enable = true;
    uv.sync.allExtras = true;
  };

  pre-commit.hooks = {
    shellcheck.enable = true;
    ripsecrets.enable = true; # don't commit secrets
    ruff.enable = true; # lint and automatically fix simple problems/reformat
    taplo.enable = true; # reformat toml
    nixfmt-rfc-style.enable = true; # reformat nix
    mypy = {
      enable = true;
    }; # check type annotations
    end-of-file-fixer.enable = true;
    commitizen.enable = true; # help adhering to commit style guidelines
    check-toml.enable = true; # check toml syntax
    check-case-conflicts.enable = true;
    check-added-large-files.enable = true;
  };
}
