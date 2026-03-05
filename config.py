class PerDirectoryConfig:
    bannedFunctions: list[str]
    bannedStructs: list[str]
    bannedArguments: list[str]
    def __init__(self, bannedFunctions=[], bannedStructs=[], bannedArguments=[]):
        self.bannedFunctions = bannedFunctions
        self.bannedStructs = bannedStructs
        self.bannedArguments = bannedArguments

class LanguageModelProvider:
    structPrefix: str
    crate: str
    module: str
    param: str
    lmProviderStructName: str
    settingsStructName: str
    def __init__(self, structPrefix, crate, module=None, param=None, lmProviderStructName=None, settingsStructName=None):
        self.structPrefix = structPrefix
        self.crate = crate
        self.module = module or crate
        self.param = param or crate
        self.lmProviderStructName = lmProviderStructName or f"{structPrefix}LanguageModelProvider"
        self.settingsStructName = settingsStructName or f"{structPrefix}Settings"

class Config:
    bannedCrates: list[str]
    bannedModules: list[tuple[str,str]]
    bannedLanguageModelProviders: list[LanguageModelProvider]
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

CONFIG.bannedLanguageModelProviders = [
    LanguageModelProvider("Anthropic", "anthropic"),
    LanguageModelProvider("Bedrock", "bedrock", settingsStructName="AmazonBedrockSettings"),
    LanguageModelProvider("ZedDotDev", "cloud_llm_client", "cloud", "zed_dot_dev", lmProviderStructName="CloudLanguageModelProvider"),
    LanguageModelProvider("CopilotChat", "copilot_chat"),
    LanguageModelProvider("DeepSeek", "deepseek"),
    LanguageModelProvider("Google", "google"),
    LanguageModelProvider("LmStudio", "lmstudio"),
    LanguageModelProvider("Mistral", "mistral"),
    LanguageModelProvider("OpenAi", "openai"),
    LanguageModelProvider("OpenRouter", "open_router"),
    LanguageModelProvider("Vercel", "vercel"),
    LanguageModelProvider("XAi", "x_ai"),
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
