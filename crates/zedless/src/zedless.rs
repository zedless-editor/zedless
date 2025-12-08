/// Provides a way to handle errors that can be ignored.
pub enum SilentError {
    /// The operation failed, but the error should be ignored.
    Silent,
    /// The operation failed, and the error should be handled normally.
    Error { error: anyhow::Error },
}

impl From<anyhow::Error> for SilentError {
    fn from(err: anyhow::Error) -> Self {
        SilentError::Error { error: err }
    }
}

pub const ZEDLESS_VERSION: &'static str = env!("CARGO_PKG_VERSION");