{ pkgs ? import <nixpkgs> {} }:
let
  python = pkgs.python3;
  pythonPackages = python.pkgs;
in
pkgs.mkShell {
  buildInputs = [
    python
    pythonPackages.pydispatcher
    pythonPackages.scrapy
    pythonPackages.email_validator
    pythonPackages.phonenumbers
    pythonPackages.tldextract
    pythonPackages.tldextract
    pythonPackages.twisted
    pythonPackages.python-dotenv
  ];
}