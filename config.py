class PerDirectoryConfig:
    bannedFunctions: list[str]
    bannedStructs: list[str]
    bannedArguments: list[str]
    bannedLocals: list[str]
    bannedActions: list[str]
    bannedEnumVariants: list[str]
    def __init__(
        self,
        bannedFunctions=[],
        bannedStructs=[],
        bannedArguments=[],
        bannedLocals=[],
        bannedActions=[],
        bannedEnumVariants=[],
    ):
        self.bannedFunctions = bannedFunctions
        self.bannedStructs = bannedStructs
        self.bannedArguments = bannedArguments
        self.bannedLocals = bannedLocals
        self.bannedActions = bannedActions
        self.bannedEnumVariants = bannedEnumVariants

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
    ("web_search_providers", "cloud"),
    ("edit_prediction", "onboarding_modal"),
    ("title_bar", "update_version"),
    ("agent_ui", "claude_agent_onboarding_modal"),
    ("agent_ui", "acp_onboarding_modal"),
    ("agent_ui", "end_trial_upsell"),
    ("zed", "telemetry_log"),
    ("zed", "reliability"),
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
        ],
        bannedLocals=[
            "metrics_id",
            "system_id",
            "telemetry",
        ]
    ),
    "crates/activity_indicator/": PerDirectoryConfig(
        bannedFunctions=[
            "dismiss_message",
        ],
        bannedLocals=[
            "checking_for_update",
            "downloading",
        ]
    ),
    "crates/agent_ui/": PerDirectoryConfig(
        bannedStructs=[
            "AcpOnboardingModal",
            "ClaudeCodeOnboardingModal",
            "EndTrialUpsell",
            "ThreadFeedbackState",
        ],
        bannedActions=[
            "OpenAcpOnboardingModal",
            "OpenClaudeAgentOnboardingModal",
            "ResetTrialUpsell",
            "ResetTrialEndUpsell",
        ],
        bannedFunctions=[
            "emit_configuration_error_telemetry_if_needed",
            "handle_feedback_click",
            "render_feedback_feedback_editor",
            "render_onboarding",
            "render_trial_end_upsell",
            "should_render_onboarding",
            "should_render_trial_end_upsell",
            "submit_feedback_message",
        ],
        bannedArguments=[
            "enable_feedback",
            "onboarding",
            "thread_feedback",
        ],
        bannedLocals=[
            "comments_editor",
            "is_signed_in",
            "onboarding",
        ]
    ),
    "crates/command_palette/": PerDirectoryConfig(
        bannedLocals=[
            "is_zed_link",
        ]
    ),
    "crates/edit_prediction/": PerDirectoryConfig(
        bannedArguments=[
            "onboarding",
            "llm_token",
        ],
        bannedStructs=[
            "ZedPredictModal",
        ],
        bannedLocals=[
            "llm_token",
            "token",
        ],
        bannedActions=[
            "OpenZedPredictOnboarding",
        ]
    ),
    "crates/title_bar/": PerDirectoryConfig(
        bannedArguments=[
            "update_version",
        ],
        bannedFunctions=[
            "render_connection_status",
            "render_sign_in_button",
            "toggle_update_simulation",
        ],
        bannedStructs=[
            "UpdateVersion",
        ],
        bannedLocals=[
            "is_signed_in",
            "show_update_badge",
            "update_version",
        ]
    ),
    "crates/settings_ui/": PerDirectoryConfig(
        bannedFunctions=[
            "privacy_section",
            "auto_update_section",
        ]
    ),
    "crates/zed/": PerDirectoryConfig(
        bannedArguments=[
            "open_channel_notes",
        ],
        bannedFunctions=[
            "authenticate",
            "installation_id",
            "parse_zed_link",
            "system_id",
        ],
        bannedLocals=[
            "installation_id",
            "is_zed_link",
            "system_specs",
            "telemetry_log_item",
        ],
        bannedStructs=[
            "IdType"
        ]
    )
}
