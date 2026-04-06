{
  lib,
  rustPlatform,
  cmake,
  copyDesktopItems,
  curl,
  perl,
  pkg-config,
  protobuf,
  fontconfig,
  freetype,
  libgit2,
  openssl,
  sqlite,
  zlib,
  zstd,
  glib,
  alsa-lib,
  libxkbcommon,
  wayland,
  libxcb,
  stdenv,
  makeFontsConf,
  vulkan-loader,
  envsubst,
  cargo-about,
  versionCheckHook,
  libGL,
  libx11,
  libxext,
  livekit-libwebrtc,
  writableTmpDirAsHomeHook,
  source,
}:

rustPlatform.buildRustPackage (finalAttrs: {
  pname = "zedless";
  inherit (source) version;

  outputs = [
    "out"
    "remote_server"
  ];

  src = source;

  postPatch = ''
    # Dynamically link WebRTC instead of static
    substituteInPlace $cargoDepsCopy/*/webrtc-sys-*/build.rs \
      --replace-fail "cargo:rustc-link-lib=static=webrtc" "cargo:rustc-link-lib=dylib=webrtc"

    # The generate-licenses script wants a specific version of cargo-about eventhough
    # newer versions work just as well.
    substituteInPlace script/generate-licenses \
      --replace-fail '$CARGO_ABOUT_VERSION' '${cargo-about.version}'
    # webrtc-sys expects glib headers to be in the sysroot, so we have to point it in the right direction
    substituteInPlace $cargoDepsCopy/*/webrtc-sys-*/build.rs \
      --replace-fail 'builder.include(&glib_path);' 'builder.include("${lib.getInclude glib}/include/glib-2.0");' \
      --replace-fail 'builder.include(&glib_path_config);' 'builder.include("${lib.getLib glib}/lib/glib-2.0/include");'
  '';

  # remove package that has a broken Cargo.toml
  # see: https://github.com/NixOS/nixpkgs/pull/445924#issuecomment-3334648753
  depsExtraArgs.postBuild = ''
    rm -r $out/git/*/candle-book/
  '';

  cargoHash = "sha256-0V1FamKm96yCKOaTUyROELdgs6olQ4d15WaWpNazpbQ=";

  nativeBuildInputs = [
    cmake
    copyDesktopItems
    curl
    perl
    pkg-config
    protobuf
    rustPlatform.bindgenHook
    cargo-about
  ];

  dontUseCmakeConfigure = true;

  buildInputs = [
    curl
    fontconfig
    freetype
    libgit2
    openssl
    sqlite
    zlib
    zstd
    glib
    alsa-lib
    libxkbcommon
    wayland
    libxcb
    # required by livekit:
    libGL
    libx11
    libxext
  ];

  cargoBuildFlags = [
    "--package=zed"
    "--package=cli"
    "--package=remote_server"
  ];

  env = {
    ALLOW_MISSING_LICENSES = true;
    ZSTD_SYS_USE_PKG_CONFIG = true;
    FONTCONFIG_FILE = makeFontsConf {
      fontDirectories = [
        "${finalAttrs.src}/assets/fonts/plex-mono"
        "${finalAttrs.src}/assets/fonts/plex-sans"
      ];
    };
    # Setting this environment variable allows to disable auto-updates
    # https://zed.dev/docs/development/linux#notes-for-packaging-zed
    ZED_UPDATE_EXPLANATION = "Zed has been installed using Nix. Auto-updates have thus been disabled.";
    # Used by `zed --version`
    RELEASE_VERSION = finalAttrs.version;
    LK_CUSTOM_WEBRTC = livekit-libwebrtc;
  };

  preBuild = ''
    bash script/generate-licenses
  '';

  postFixup = ''
    patchelf --add-rpath ${vulkan-loader}/lib $out/libexec/*
    patchelf --add-rpath ${wayland}/lib $out/libexec/*
  '';

  nativeCheckInputs = [
    writableTmpDirAsHomeHook
  ];

  doCheck = false;

  installPhase = ''
    runHook preInstall

    release_target="target/${stdenv.hostPlatform.rust.cargoShortTarget}/release"
    install -Dm755 $release_target/zed $out/libexec/zedless-editor
    install -Dm755 $release_target/cli $out/bin/zedless

    install -Dm644 $src/crates/zed/resources/app-icon@2x.png $out/share/icons/hicolor/1024x1024@2x/apps/zedless.png
    install -Dm644 $src/crates/zed/resources/app-icon.png $out/share/icons/hicolor/512x512/apps/zedless.png

    # extracted from https://github.com/zed-industries/zed/blob/v0.141.2/script/bundle-linux (envsubst)
    # and https://github.com/zed-industries/zed/blob/v0.141.2/script/install.sh (final desktop file name)
    (
      export DO_STARTUP_NOTIFY="true"
      export APP_CLI="zedless"
      export APP_ICON="zedless"
      export APP_NAME="Zedless"
      export APP_ARGS="%U"
      mkdir -p "$out/share/applications"
      ${lib.getExe envsubst} < "crates/zed/resources/zed.desktop.in" > "$out/share/applications/org.zedless.Zedless.desktop"
    )
    install -Dm755 $release_target/remote_server $remote_server/bin/zed-remote-server-stable-''${version}+stable
    runHook postInstall
  '';

  nativeInstallCheckInputs = [
    versionCheckHook
  ];
  versionCheckProgram = "${placeholder "out"}/bin/zedless";
  versionCheckProgramArg = "--version";
  doInstallCheck = true;

  meta = {
    homepage = "https://zedless.org";
    license = lib.licenses.gpl3Only;
    mainProgram = "zedless";
  };
})
