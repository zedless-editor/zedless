use anyhow::Result;
use gpui::App;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};
use settings::Settings;

pub fn init(cx: &mut App) {
    ZedlessSettings::register(cx);
}

/// Zedless settings.
#[derive(Clone, Debug, Default, Serialize, Deserialize, PartialEq, Eq, JsonSchema)]
pub struct ZedlessSettings {
}

impl Settings for ZedlessSettings {
    const KEY: Option<&'static str> = Some("zedless");

    type FileContent = Self;
    fn load(sources: settings::SettingsSources<Self::FileContent>, _: &mut App) -> Result<Self>
    where
        Self: Sized,
    {
        sources.json_merge::<Self>()
    }

    fn import_from_vscode(_vscode: &settings::VsCodeSettings, _current: &mut Self::FileContent) {}
}
