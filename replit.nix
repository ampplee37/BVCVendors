{ pkgs }: {
  deps = [
    pkgs.python39
    pkgs.python39Packages.pip
    pkgs.python39Packages.setuptools
    pkgs.libffi
    pkgs.git-lfs
    pkgs.pkg-config
    pkgs.libxml2
    pkgs.python39Packages.cryptography
    pkgs.python39Packages.cffi
    pkgs.gcc
    pkgs.python39Packages.twisted
    pkgs.python39Packages.scrapy
  ];
}