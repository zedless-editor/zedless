{ pkgs, zedless }:

let
  zedless-fhs = pkgs.runCommand "zedless-fhs-${zedless.version}" {
  } ''
    cp -r --no-preserve=mode ${zedless} $out
    patchelf $out/bin/zedless $out/libexec/zedless-editor --set-interpreter /lib64/ld-linux-x86-64.so.2 --remove-rpath
  '';

  nfpmConfig = pkgs.writeText "nfpm.json" (builtins.toJSON {
    name = zedless.pname;
    inherit (zedless) version;
    arch = "amd64";
    platform = "linux";
    homepage = "https://zedless.org";
    description = "Zedless Editor";
    license = zedless.meta.license.spdxId;
    contents = [
      {
        type = "tree";
        src = zedless-fhs;
        dst = "/usr";
      }
    ];
    rpm.compression = "zstd";
  });
in

{
  rpm = pkgs.runCommand "zedless-rpm-${zedless.version}" {
    nativeBuildInputs = [
      pkgs.elfdeps
      pkgs.nfpm
      pkgs.jq
    ];
  } ''
    mkdir $out
    (
        elfdeps --requires ${zedless-fhs}/bin/zedless
        elfdeps --requires ${zedless-fhs}/libexec/zedless-editor
    ) | sort -u | jq --raw-input --slurp --slurpfile config ${nfpmConfig} '
        $config[0] * {
            overrides: {
                rpm: {
                    depends: split("\n") | map(select(length > 0))
                }
            }
        }
    ' > nfpm.json
    nfpm package --config nfpm.json --target $out/${zedless.name}.rpm --packager rpm
  '';
}
