{pkgs}: {
  deps = [
    pkgs.swig
    pkgs.mecab
    pkgs.glibcLocales
    pkgs.postgresql
    pkgs.openssl
  ];
}
