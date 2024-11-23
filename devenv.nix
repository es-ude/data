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

  packages = [ pkgs.git ];

  languages.python = {
    enable = true;
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
