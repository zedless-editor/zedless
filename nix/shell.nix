{
  mkShell,
  makeFontsConf,

  zedless,

  rust-analyzer,
  cargo-nextest,
  cargo-hakari,
  cargo-machete,
  nixfmt-rfc-style,
  rustfmt,
  protobuf,
  gdb,
  python3,
  writeShellScriptBin,
}:
(mkShell.override { inherit (zedless) stdenv; }) {
  inputsFrom = [ zedless ];
  packages = [
    rust-analyzer
    cargo-nextest
    cargo-hakari
    cargo-machete
    nixfmt-rfc-style
    rustfmt
    gdb
    (python3.withPackages (
      python3Packages: with python3Packages; [
        click
      ]
    ))
    (writeShellScriptBin "zlt" ''
      set -eu
      exec python3 "$ZEDLESS_ZLT_SRC_PATH/zlt.py" "$@"
    '')
  ];

  env =
    let
      baseEnvs =
        (zedless.overrideAttrs (attrs: {
          passthru = { inherit (attrs) env; };
        })).env; # exfil `env`; it's not in drvAttrs
    in
    (removeAttrs baseEnvs [
      "CARGO_PROFILE" # let you specify the profile
      "TARGET_DIR"
    ])
    // {
      # note: different than `$FONTCONFIG_FILE` in `build.nix` – this refers to relative paths
      # outside the nix store instead of to `$src`
      FONTCONFIG_FILE = makeFontsConf {
        fontDirectories = [
          "./assets/fonts/plex-mono"
          "./assets/fonts/plex-sans"
        ];
      };
      PROTOC = "${protobuf}/bin/protoc";
    };

  shellHook = ''
    export ZEDLESS_ZLT_SRC_PATH="$PWD/tooling/zlt/src"
  '';
}
