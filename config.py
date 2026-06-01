class PerDirectoryConfig:
    bannedFunctions: list[str]
    bannedStructs: list[str]
    bannedArguments: list[str]
    bannedLocals: list[str]
    bannedActions: list[str]
    bannedEnumVariants: list[str]
    bannedEnums: list[str]
    disabledFunctions: list[str]
    stringReplacements: list[tuple[str,str]]
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
        stringReplacements=[],
    ):
        self.bannedFunctions = bannedFunctions
        self.bannedStructs = bannedStructs
        self.bannedArguments = bannedArguments
        self.bannedLocals = bannedLocals
        self.bannedActions = bannedActions
        self.bannedEnumVariants = bannedEnumVariants
        self.bannedEnums = bannedEnums
        self.disabledFunctions = disabledFunctions
        self.stringReplacements = stringReplacements

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
    "crashes",
    "deepseek",
    "feedback",
    "google_ai",
    "language_models_cloud",
    "lmstudio",
    "mistral",
    "open_router",
    "opencode",
    "supermaven",
    "supermaven_api",
    "telemetry",
    "telemetry_events",
    "vercel",
    "web_search_providers",
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
    ("client", "llm_token"),
    ("edit_prediction", "mercury"),
    ("edit_prediction", "onboarding_modal"),
    ("edit_prediction", "sweep_ai"),
    ("edit_prediction_ui", "rate_prediction_modal"),
    ("language_model", "telemetry"),
    ("project", "telemetry_snapshot"),
    ("title_bar", "onboarding_banner"),
    ("title_bar", "plan_chip"),
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
    LanguageModelProvider("OpenAiSubscribed", "openai_subscribed", lmProviderStructName="OpenAiSubscribedProvider"),
    LanguageModelProvider("OpenCode", "opencode"),
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
            "global_llm_token",
            "needs_llm_token_refresh",
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
            "NeedsLlmTokenRefresh",
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
        ],
        stringReplacements=[
            ("../lib/zed/zed-editor", "../lib/zedless/zedless-editor"),
            ("../libexec/zed-editor", "../libexec/zedless-editor"),
            ("/app/libexec/zed-editor", "/app/libexec/zedless-editor"),
            ("Open Zed Log", "Open Zedless Log"),
            ("Welcome to Zed", "Welcome to Zedless"),
            ("Welcome back to Zed", "Welcome back to Zedless"),
            ("Zed (Default)", "Zedless (Default)"),
            ("Zed Default", "Zedless Default"),
            ("Zed Dev", "Zedless Dev"),
            ("Zed Nightly", "Zedless Nightly"),
            ("Zed Preview", "Zedless Preview"),
            ("Zed", "Zedless"),
            ("dev.zed.Zed", "org.zedless.Zedless"),
            ("dev.zed.Zed-Dev", "org.zedless.Zedless-Dev"),
            ("dev.zed.Zed-Nightly", "org.zedless.Zedless-Nightly"),
            ("dev.zed.Zed-Preview", "org.zedless.Zedless-Preview"),
            ("zed-editor", "zedless-editor"),
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
            "dismiss_ai_onboarding",
            "emit_configuration_error_telemetry_if_needed",
            "emit_load_error_telemetry",
            "emit_thread_error_telemetry",
            "emit_token_limit_telemetry_if_needed",
            "fire_started_telemetry",
            "handle_feedback_click",
            "render_feedback_feedback_editor",
            "render_new_user_onboarding",
            "render_onboarding",
            "render_trial_end_upsell",
            "render_zed_plan_info",
            "should_render_new_user_onboarding",
            "should_render_onboarding",
            "should_render_trial_end_upsell",
            "submit_feedback_message",
            "thumbs_down",
            "thumbs_up",
        ],
        bannedArguments=[
            "enable_feedback",
            "is_new_install",
            "last_configuration_error_telemetry",
            "last_token_limit_telemetry",
            "new_user_onboarding",
            "new_user_onboarding_upsell_dismissed",
            "on_boarding_upsell_dismissed",
            "onboarding",
            "thread_feedback",
        ],
        bannedLocals=[
            "anthropic_event_type",
            "anthropic_reporter",
            "comments_editor",
            "enable_thread_feedback",
            "is_new_install",
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
    "crates/cli/":  PerDirectoryConfig(
        stringReplacements=[
            ("zed", "zedless")
        ]
    ),
    "crates/client/": PerDirectoryConfig(
        bannedFunctions=[
            "acquire_llm_token",
            "add_message_to_client_handler",
            "authenticated_llm_request",
            "cached_llm_token",
            "clear_and_refresh_llm_token",
            "connect_to_cloud",
            "handle_message_to_client",
            "refresh_llm_token",
            "set_current_organization",
        ],
        bannedArguments=[
            "_handle_sign_out",
            "_maintain_current_user",
            "system_id",
        ],
        bannedActions=[
            "SignIn",
            "SignOut",
            "Reconnect",
        ]
    ),
    "crates/command_palette/": PerDirectoryConfig(
        bannedLocals=[
            "is_zed_link",
        ]
    ),
    "crates/edit_prediction/": PerDirectoryConfig(
        bannedArguments=[
            "_fetch_experiments_task",
            "can_collect_data",
            "capture_data",
            "copilot",
            "legacy_data_collection_enabled",
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
            "can_collect_data",
            "capture_data",
            "fetch_experiments_task",
            "is_cloud",
            "legacy_data_collection_enabled",
            "llm_token",
            "raw_config",
            "token",
        ],
        bannedActions=[
            "OpenZedPredictOnboarding",
            "Reinstall",
            "SignIn",
            "SignOut",
        ],
        bannedFunctions=[
            "can_toggle_data_collection",
            "copilot_for_project",
            "data_collection_state",
            "edit_prediction_accepted",
            "handle_rejected_predictions",
            "has_mercury_api_token",
            "has_sweep_api_token",
            "is_data_collection_allowed_by_organization",
            "is_data_collection_enabled",
            "is_prediction_rated",
            "load_legacy_data_collection_enabled",
            "mercury_has_payment_required_error",
            "rate_prediction",
            "refresh_available_experiments",
            "run_settled_predictions_worker",
            "send_api_request",
            "send_raw_llm_request",
            "send_v3_request",
            "start_copilot_for_project",
            "toggle_data_collection",
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
            "mercury_has_error",
            "mercury_payment_required",
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
    "crates/languages/": PerDirectoryConfig(
        disabledFunctions=[
            "cached_server_binary",
            "fetch_latest_server_version",
            "fetch_server_binary",
        ],
        bannedFunctions=[
            "get_cached_server_binary",
            "get_cached_ts_server_binary",
            "get_cached_version_server_binary",
        ]
    ),
    "crates/node_runtime/": PerDirectoryConfig(
        disabledFunctions=[
            "binary_path",
            "npm_command",
            "npm_install_packages",
            "npm_package_installed_version",
            "npm_package_latest_version",
            "run_npm_subcommand",
        ],
        bannedFunctions=[
            "build_npm_command_args",
            "configure_npm_command",
            "npm_command_env",
            "path_with_node_binary_prepended",
            "proxy_argument",
            "test_build_npm_command_args_inserts_prefix_before_subcommand",
            "test_build_npm_command_args_keeps_entrypoint_before_prefix",
            "test_proxy_argument_map_localhost_proxy",
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
    "crates/remote/": PerDirectoryConfig(
        bannedFunctions = [
            "download_binary_on_server",
            "extract_server_binary",
            "extract_server_binary_posix",
            "extract_server_binary_windows",
            "get_download_url",
            "upload_local_server_binary",
        ]
    ),
    "crates/remote_connection/": PerDirectoryConfig(
        bannedFunctions = [
            "get_download_url",
        ]
    ),
    "crates/remote_server/": PerDirectoryConfig(
        bannedFunctions=[
            "crash_server",
            "handle_crash_files_requests",
        ],
        bannedLocals=[
            "crash_handler",
            "should_install_crash_handler",
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
            "render_organization_menu_button",
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
            "is_new_install",
            "join_channel",
            "open_channel_notes",
        ],
        bannedFunctions=[
            "authenticate",
            "crash_server",
            "installation_id",
            "parse_zed_link",
            "register_backward_compatible_actions",
            "set_gpu_info",
            "set_user_info",
            "system_id",
        ],
        bannedLocals=[
            "channels_panel",
            "copilot_chat_configuration",
            "crash_handler",
            "installation_id",
            "is_new_install",
            "is_zed_link",
            "notification_panel",
            "should_install_crash_handler",
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
        ],
        bannedStructs=[
            "CrashHandler",
            "RefreshLlmTokenListener",
        ]
    ),
    "crates/zeta_prompt/": PerDirectoryConfig(
        bannedArguments=[
            "can_collect_data",
        ]
    )
}
