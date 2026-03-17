class PerDirectoryConfig:
    bannedFunctions: list[str]
    bannedStructs: list[str]
    bannedArguments: list[str]
    bannedLocals: list[str]
    bannedActions: list[str]
    bannedEnumVariants: list[str]
    bannedEnums: list[str]
    def __init__(
        self,
        bannedFunctions=[],
        bannedStructs=[],
        bannedArguments=[],
        bannedLocals=[],
        bannedActions=[],
        bannedEnumVariants=[],
        bannedEnums=[],
    ):
        self.bannedFunctions = bannedFunctions
        self.bannedStructs = bannedStructs
        self.bannedArguments = bannedArguments
        self.bannedLocals = bannedLocals
        self.bannedActions = bannedActions
        self.bannedEnumVariants = bannedEnumVariants
        self.bannedEnums = bannedEnums

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
    "anthropic",
    "auto_update",
    "auto_update_ui",
    "bedrock",
    "collab",
    "deepseek",
    "feedback",
    "google_ai",
    "lmstudio",
    "mistral",
    "open_router",
    "telemetry",
    "telemetry_events",
    "vercel",
    "x_ai",
]

CONFIG.bannedModules = [
    ("agent_servers", "claude"),
    ("agent_servers", "codex"),
    ("agent_servers", "gemini"),
    ("agent_ui", "acp_onboarding_modal"),
    ("agent_ui", "claude_agent_onboarding_modal"),
    ("agent_ui", "end_trial_upsell"),
    ("client", "telemetry"),
    ("edit_prediction", "mercury"),
    ("edit_prediction", "onboarding_modal"),
    ("edit_prediction", "sweep_ai"),
    ("edit_prediction_ui", "rate_prediction_modal"),
    ("language_model", "telemetry"),
    ("project", "telemetry_snapshot"),
    ("title_bar", "update_version"),
    ("web_search_providers", "cloud"),
    ("zed", "reliability"),
    ("zed", "telemetry_log"),
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
            "generate_telemetry",
            "register_zed_web_search_provider",
            "render_telemetry_section",
            "report_discovered_project_type_events",
            "send_telemetry",
            "set_authenticated_user_info",
            "telemetry",
            "telemetry_event_text",
            "telemetry_report_accepted_edits",
            "telemetry_report_rejected_edits",
            "telemetry_settings_content",
            "telemetry_string",
        ],
        bannedStructs=[
            "ActionLogTelemetry",
            "AiUpsellCard",
            "EditPredictionOnboarding",
            "LlmApiToken",
            "SystemSpecs",
            "Telemetry",
            "TelemetrySettings",
            "TelemetrySettingsContent",
            "TelemetrySource",
            "TelemetryState",
            "ZedAiOnboarding",
        ],
        bannedArguments=[
            "enable_telemetry",
            "llm_api_token",
            "telemetry",
        ],
        bannedLocals=[
            "agent_telemetry_id",
            "enable_telemetry",
            "metrics_id",
            "model_telemetry_id",
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
    "crates/agent/": PerDirectoryConfig(
        bannedFunctions=[
            "project_snapshot",
        ],
        bannedStructs=[
            "ProjectSnapshot",
        ],
        bannedArguments=[
            "initial_project_snapshot",
        ],
        bannedLocals=[
            "initial_project_snapshot",
        ]
    ),
    "crates/agent_ui/": PerDirectoryConfig(
        bannedStructs=[
            "AcpOnboardingModal",
            "AnthropicCompletionType",
            "AnthropicEventData",
            "AnthropicEventType",
            "ClaudeCodeOnboardingModal",
            "EndTrialUpsell",
            "OnboardingUpsell",
            "ThreadFeedbackState",
            "TrialEndUpsell",
        ],
        bannedActions=[
            "OpenAcpOnboardingModal",
            "OpenClaudeAgentOnboardingModal",
            "ResetTrialUpsell",
            "ResetTrialEndUpsell",
        ],
        bannedFunctions=[
            "emit_configuration_error_telemetry_if_needed",
            "emit_load_error_telemetry",
            "emit_thread_error_telemetry",
            "emit_token_limit_telemetry_if_needed",
            "fire_started_telemetry",
            "handle_feedback_click",
            "render_feedback_feedback_editor",
            "render_onboarding",
            "render_trial_end_upsell",
            "render_zed_plan_info",
            "report_anthropic_event",
            "should_render_onboarding",
            "should_render_trial_end_upsell",
            "submit_feedback_message",
        ],
        bannedArguments=[
            "enable_feedback",
            "last_configuration_error_telemetry",
            "last_token_limit_telemetry",
            "onboarding",
            "thread_feedback",
        ],
        bannedLocals=[
            "anthropic_event_type",
            "anthropic_reporter",
            "comments_editor",
            "is_signed_in",
            "onboarding",
        ],
        bannedEnumVariants=[
            "ClaudeAgent",
            "ClaudeCode",
            "Codex",
            "Gemini",
            "Mercury",
            "Sweep",
        ]
    ),
    "crates/assistant_text_thread/": PerDirectoryConfig(
        bannedStructs=[
            "AnthropicCompletionType",
            "AnthropicEventData",
            "AnthropicEventType",
        ],
        bannedFunctions=[
            "report_anthropic_event",
        ]
    ),
    "crates/command_palette/": PerDirectoryConfig(
        bannedLocals=[
            "is_zed_link",
        ]
    ),
    "crates/edit_prediction/": PerDirectoryConfig(
        bannedArguments=[
            "llm_token",
            "mercury",
            "onboarding",
            "rating",
            "sweep_ai",
        ],
        bannedStructs=[
            "EditPredictionRating",
            "ZedPredictModal",
        ],
        bannedLocals=[
            "llm_token",
            "token",
        ],
        bannedActions=[
            "OpenZedPredictOnboarding",
        ],
        bannedFunctions=[
            "has_mercury_api_token",
            "has_sweep_api_token",
            "is_prediction_rated",
            "rate_prediction",
        ],
        bannedEnumVariants=[
            "Mercury",
            "Sweep",
        ]
    ),
    "crates/edit_prediction_ui/": PerDirectoryConfig(
        bannedLocals=[
            "mercury_api_token_task",
            "sweep_api_token_task",
        ],
        bannedEnumVariants=[
            "Mercury",
            "Sweep",
        ],
        bannedFunctions=[
            "feature_gate_predict_edits_actions",
        ],
        bannedActions=[
            "RatePredictions",
        ]
    ),
    "crates/language_model/": PerDirectoryConfig(
        bannedEnums=[
            "AnthropicError",
            "OpenRouterError",
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
    "crates/settings_content/": PerDirectoryConfig(
        bannedEnumVariants=[
            "Mercury",
            "Sweep",
        ]
    ),
    "crates/settings_ui/": PerDirectoryConfig(
        bannedFunctions=[
            "auto_update_section",
            "privacy_section",
            "render_api_key_provider",
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
        ],
        bannedEnumVariants=[
            "Mercury",
            "Sweep",
        ]
    )
}
