{ pkgs ? import <nixpkgs> {} }:
(pkgs.callPackage (import ./replit.nix) {})