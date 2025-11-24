use std::sync::Arc;

use anyhow::Result;
use client::Client;
use gpui::{
    App, AppContext as _, AsyncApp, Context, Entity, EventEmitter, Global, ReadGlobal as _,
};
use proto::{TypedEnvelope};
use smol::lock::{RwLock, RwLockUpgradableReadGuard, RwLockWriteGuard};

#[derive(Clone, Default)]
pub struct LlmApiToken(Arc<RwLock<Option<String>>>);

impl LlmApiToken {
    pub async fn acquire(&self, client: &Arc<Client>) -> Result<String> {
        let lock = self.0.upgradable_read().await;
        if let Some(token) = lock.as_ref() {
            Ok(token.to_string())
        } else {
            Self::fetch(RwLockUpgradableReadGuard::upgrade(lock).await, client).await
        }
    }

    pub async fn refresh(&self, client: &Arc<Client>) -> Result<String> {
        Self::fetch(self.0.write().await, client).await
    }

    async fn fetch(
        mut lock: RwLockWriteGuard<'_, Option<String>>,
        client: &Arc<Client>,
    ) -> Result<String> {
        let response = client.request(proto::GetLlmToken {}).await?;
        *lock = Some(response.token.clone());
        Ok(response.token.clone())
    }
}

struct GlobalRefreshLlmTokenListener(Entity<RefreshLlmTokenListener>);

impl Global for GlobalRefreshLlmTokenListener {}

pub struct RefreshLlmTokenEvent;

pub struct RefreshLlmTokenListener {
    _llm_token_subscription: client::Subscription,
}

impl EventEmitter<RefreshLlmTokenEvent> for RefreshLlmTokenListener {}

impl RefreshLlmTokenListener {
    pub fn register(client: Arc<Client>, cx: &mut App) {
        let listener = cx.new(|cx| RefreshLlmTokenListener::new(client, cx));
        cx.set_global(GlobalRefreshLlmTokenListener(listener));
    }

    pub fn global(cx: &App) -> Entity<Self> {
        GlobalRefreshLlmTokenListener::global(cx).0.clone()
    }

    fn new(client: Arc<Client>, cx: &mut Context<Self>) -> Self {
        Self {
            _llm_token_subscription: client
                .add_message_handler(cx.weak_entity(), Self::handle_refresh_llm_token),
        }
    }

    async fn handle_refresh_llm_token(
        this: Entity<Self>,
        _: TypedEnvelope<proto::RefreshLlmToken>,
        mut cx: AsyncApp,
    ) -> Result<()> {
        this.update(&mut cx, |_this, cx| cx.emit(RefreshLlmTokenEvent))
    }
}
