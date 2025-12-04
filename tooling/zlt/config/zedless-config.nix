let
  mkCratePath = crate: "crates/${crate}/";

  mkLanguageModelProviderModule = provider: "crates/language_models/src/provider/${provider}.rs";
in

rec {
  deleteFileGlobs = [
    "**/Dockerfile*"
    ".github/"
    "CONTRIBUTING.md"
    "GEMINI.md"
    "crates/**/*telemetry*.rs"
    "crates/**/onboarding_*.rs"
    "crates/agent_servers/src/claude.rs"
    "crates/agent_servers/src/gemini.rs"
    "crates/agent_ui/src/ui/end_trial_upsell.rs"
    "crates/http_client/src/github.rs"
    "crates/project/src/prettier_store.rs"
    "crates/zed/resources/app-icon-nightly*.png"
    "crates/zed/src/reliability.rs"
    "crates/zeta/src/license_detection.rs"
    "crates/zeta/src/rate_completion_modal.rs"
    "legal/subprocessors.md"
  ]
  ++ map mkCratePath bannedCrates
  ++ map mkLanguageModelProviderModule [
    "anthropic"
    "bedrock"
    "cloud"
    "copilot_chat"
    "deepseek"
    "google"
    "lmstudio"
    "mistral"
    "open_router"
  ];

  bannedCrates = [
    "ai_onboarding"
    "anthropic"
    "auto_update"
    "auto_update_helper"
    "auto_update_ui"
    "aws_http_client"
    "bedrock"
    "collab"
    "copilot"
    "deepseek"
    "google_ai"
    "livekit_api"
    "livekit_client"
    "lmstudio"
    "mistral"
    "node_runtime"
    "open_router"
    "prettier"
    "supermaven"
    "supermaven_api"
    "system_specs"
    "telemetry"
    "telemetry_events"
    "vercel"
    "x_ai"
  ];

  conflicts = {
    ourFiles = [
      "README.md"
      "flake.lock"
      "flake.nix"
      "nix/**"
    ];
    acceptTheirDeletions = [
      "crates/**/*.rs"
      "crates/**/*.toml"
    ];
  };
}
