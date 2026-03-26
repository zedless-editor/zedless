class PerDirectoryConfig:
    bannedFunctions: list[str]
    bannedStructs: list[str]
    bannedArguments: list[str]
    bannedLocals: list[str]
    bannedActions: list[str]
    bannedEnumVariants: list[str]
    bannedEnums: list[str]
    disabledFunctions: list[str]
    def __init__(
        self,
        bannedFunctions=[],
        bannedStructs=[],
        bannedArguments=[],
        bannedLocals=[],
        bannedActions=[],
        bannedEnumVariants=[],
        bannedEnums=[],
        disabledFunctions=[],
    ):
        self.bannedFunctions = bannedFunctions
        self.bannedStructs = bannedStructs
        self.bannedArguments = bannedArguments
        self.bannedLocals = bannedLocals
        self.bannedActions = bannedActions
        self.bannedEnumVariants = bannedEnumVariants
        self.bannedEnums = bannedEnums
        self.disabledFunctions = disabledFunctions

class PerCrateConfig(PerDirectoryConfig):
    pass

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
    perCrate: dict[str, PerCrateConfig]
    perDirectory: dict[str, PerDirectoryConfig]

CONFIG = Config()
CONFIG.bannedCrates = [
    "ai_onboarding",
    "anthropic",
    "auto_update",
    "auto_update_ui",
    "aws_http_client",
    "bedrock",
    "collab",
    "copilot",
    "copilot_chat",
    "copilot_ui",
    "deepseek",
    "feedback",
    "google_ai",
    "lmstudio",
    "mistral",
    "open_router",
    "supermaven",
    "supermaven_api",
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
    ("title_bar", "onboarding_banner"),
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
    LanguageModelProvider("VercelAiGateway", "vercel_ai_gateway"),
    LanguageModelProvider("XAi", "x_ai"),
]

CONFIG.perCrate = {
    "anthropic": PerCrateConfig(
        bannedEnums=[
            "Speed"
        ]
    )
}

CONFIG.perDirectory = {
    "crates/": PerDirectoryConfig(
        bannedFunctions=[
            "download_server_binary_locally",
            "generate_telemetry",
            "register_zed_web_search_provider",
            "render_telemetry_section",
            "report_anthropic_event",
            "report_call_event",
            "report_discovered_project_type_events",
            "report_edit_prediction_event",
            "report_editor_event",
            "report_inline_completion_event",
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
        ],
        bannedEnums=[
            "TelemetrySpawnLocation",
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
            "copilot_enabled",
            "copilot_enabled_for_language",
            "initial_project_snapshot",
        ]
    ),
    "crates/agent_servers/": PerDirectoryConfig(
        bannedFunctions=[
            "api_key_for_gemini_cli"
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
            "should_render_onboarding",
            "should_render_trial_end_upsell",
            "submit_feedback_message",
            "thumbs_down",
            "thumbs_up",
        ],
        bannedArguments=[
            "enable_feedback",
            "last_configuration_error_telemetry",
            "last_token_limit_telemetry",
            "on_boarding_upsell_dismissed",
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
            "Copilot",
            "Gemini",
            "Mercury",
            "Supermaven",
            "Sweep",
        ],
        bannedEnums=[
            "ThreadFeedback",
        ]
    ),
    "crates/assistant_text_thread/": PerDirectoryConfig(
        bannedStructs=[
            "AnthropicCompletionType",
            "AnthropicEventData",
            "AnthropicEventType",
        ]
    ),
    "crates/command_palette/": PerDirectoryConfig(
        bannedLocals=[
            "is_zed_link",
        ]
    ),
    "crates/edit_prediction/": PerDirectoryConfig(
        bannedArguments=[
            "copilot",
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
            "Reinstall",
            "SignIn",
            "SignOut",
        ],
        bannedFunctions=[
            "copilot_for_project",
            "has_mercury_api_token",
            "has_sweep_api_token",
            "is_prediction_rated",
            "rate_prediction",
            "refresh_available_experiments",
            "start_copilot_for_project",
        ],
        bannedEnumVariants=[
            "Copilot",
            "Mercury",
            "Supermaven",
            "Sweep",
        ]
    ),
    "crates/edit_prediction_ui/": PerDirectoryConfig(
        bannedLocals=[
            "copilot",
            "copilot_config",
            "mercury_api_token_task",
            "sweep_api_token_task",
        ],
        bannedEnumVariants=[
            "Copilot",
            "Mercury",
            "Supermaven",
            "Sweep",
        ],
        bannedFunctions=[
            "build_copilot_context_menu",
            "build_copilot_start_menu",
            "build_supermaven_context_menu",
            "copilot_settings_url",
            "feature_gate_predict_edits_actions",
            "hide_copilot",
            "test_copilot_settings_url_with_enterprise_uri",
            "test_copilot_settings_url_with_enterprise_uri_trailing_slash",
            "test_copilot_settings_url_without_enterprise_uri",
        ],
        bannedActions=[
            "RatePredictions",
        ],
        bannedStructs=[
            "CopilotErrorToast",
        ]
    ),
    "crates/editor/": PerDirectoryConfig(
        bannedEnums=[
            "ReportEditorEvent"
        ]
    ),
    "crates/language/": PerDirectoryConfig(
        bannedStructs=[
            "CopilotSettings",
        ],
        bannedArguments=[
            "copilot",
        ],
        bannedLocals=[
            "copilot",
            "copilot_settings",
        ]
    ),
    "crates/language_model/": PerDirectoryConfig(
        bannedEnums=[
            "AnthropicError",
            "OpenRouterError",
        ]
    ),
    "crates/language_tools/": PerDirectoryConfig(
        bannedFunctions=[
            "try_ensure_copilot_for_project",
        ],
        bannedLocals=[
            "copilot_enabled",
        ]
    ),
    "crates/paths/": PerDirectoryConfig(
        bannedFunctions=[
            "copilot_dir",
        ]
    ),
    "crates/project/": PerDirectoryConfig(
        bannedFunctions=[
            "copilot_state_for_project",
        ],
        bannedArguments=[
            "copilot_log_subscription",
        ]
    ),
    "crates/title_bar/": PerDirectoryConfig(
        bannedArguments=[
            "banner",
            "show_onboarding_banner",
            "update_version",
        ],
        bannedFunctions=[
            "render_connection_status",
            "render_sign_in_button",
            "render_user_menu_button",
            "toggle_update_simulation",
        ],
        bannedStructs=[
            "UpdateVersion",
        ],
        bannedLocals=[
            "banner",
            "is_signed_in",
            "show_update_badge",
            "update_version",
        ]
    ),
    "crates/settings_content/": PerDirectoryConfig(
        bannedEnumVariants=[
            "Copilot",
            "Mercury",
            "Supermaven",
            "Sweep",
        ],
        bannedStructs=[
            "CopilotSettingsContent",
        ],
        bannedArguments=[
            "copilot",
        ]
    ),
    "crates/settings_ui/": PerDirectoryConfig(
        bannedFunctions=[
            "auto_update_section",
            "privacy_section",
            "render_api_key_provider",
            "render_github_copilot_provider",
        ]
    ),
    "crates/zed/": PerDirectoryConfig(
        bannedArguments=[
            "join_channel",
            "open_channel_notes",
        ],
        bannedFunctions=[
            "authenticate",
            "installation_id",
            "parse_zed_link",
            "system_id",
            "register_backward_compatible_actions",
        ],
        bannedLocals=[
            "copilot_chat_configuration",
            "installation_id",
            "is_zed_link",
            "system_specs",
            "telemetry_log_item",
        ],
        bannedEnums=[
            "IdType"
        ],
        bannedEnumVariants=[
            "Copilot",
            "Mercury",
            "Supermaven",
            "Sweep",
        ],
        bannedActions=[
            "RestoreBanner",
        ]
    )
}
