let
  mkCratePath = crate: "crates/${crate}/";
in

rec {
  deleteFileGlobs = [
    "**/Dockerfile"
    ".github/"
    "GEMINI.md"
  ]
  ++ map mkCratePath bannedCrates;

  bannedCrates = [
    "telemetry"
  ];
}
