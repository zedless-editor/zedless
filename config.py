class PerDirectoryConfig:
    bannedFunctions: list[str]
    bannedStructs: list[str]
    bannedArguments: list[str]
    def __init__(self, bannedFunctions=[], bannedStructs=[], bannedArguments=[]):
        self.bannedFunctions = bannedFunctions
        self.bannedStructs = bannedStructs
        self.bannedArguments = bannedArguments

class Config:
    bannedCrates: list[str]
    bannedModules: list[tuple[str,str]]
    perDirectory: dict[str, PerDirectoryConfig]

CONFIG = Config()
CONFIG.bannedCrates = [
    "ai_onboarding",
    "auto_update",
    "auto_update_ui",
    "feedback",
    "telemetry",
]

CONFIG.bannedModules = [
    ("web_search_providers", "cloud")
]

CONFIG.perDirectory = {
    "crates/": PerDirectoryConfig(
        bannedFunctions=[
            "download_server_binary_locally",
            "register_zed_web_search_provider",
            "render_telemetry_section",
            "report_discovered_project_type_events",
            "send_telemetry",
            "set_authenticated_user_info",
            "telemetry",
            "telemetry_report_accepted_edits",
            "telemetry_report_rejected_edits",
            "telemetry_settings_content",
        ],
        bannedStructs=[
            "AiUpsellCard",
            "EditPredictionOnboarding",
            "LlmApiToken",
            "SystemSpecs",
            "Telemetry",
            "TelemetrySettings",
            "TelemetryState",
            "ZedAiOnboarding",
        ],
        bannedArguments=[
            "llm_api_token",
            "telemetry",
        ]
    )
}
