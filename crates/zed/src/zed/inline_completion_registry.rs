use client::Client;
use collections::HashMap;
use editor::Editor;
use gpui::{AnyWindowHandle, App, AppContext as _, Context, WeakEntity};
use language::language_settings::{EditPredictionProvider, all_language_settings};
use settings::SettingsStore;
use smol::stream::StreamExt;
use std::{cell::RefCell, rc::Rc, sync::Arc};
use ui::Window;
use util::ResultExt;
use zeta::{ZetaInlineCompletionProvider};

pub fn init(client: Arc<Client>, cx: &mut App) {
    let editors: Rc<RefCell<HashMap<WeakEntity<Editor>, AnyWindowHandle>>> = Rc::default();
    cx.observe_new({
        let editors = editors.clone();
        let client = client.clone();
        move |editor: &mut Editor, window, cx: &mut Context<Editor>| {
            if !editor.mode().is_full() {
                return;
            }

            let Some(window) = window else {
                return;
            };

            let editor_handle = cx.entity().downgrade();
            cx.on_release({
                let editor_handle = editor_handle.clone();
                let editors = editors.clone();
                move |_, _| {
                    editors.borrow_mut().remove(&editor_handle);
                }
            })
            .detach();

            editors
                .borrow_mut()
                .insert(editor_handle, window.window_handle());
            let provider = all_language_settings(None, cx).edit_predictions.provider;
            assign_edit_prediction_provider(
                editor,
                provider,
                &client,
                window,
                cx,
            );
        }
    })
    .detach();

    cx.on_action(clear_zeta_edit_history);

    let mut provider = all_language_settings(None, cx).edit_predictions.provider;
    cx.spawn({
        let editors = editors.clone();
        let client = client.clone();

        async move |cx| {
            let mut status = client.status();
            while let Some(_status) = status.next().await {
                cx.update(|cx| {
                    assign_edit_prediction_providers(
                        &editors,
                        provider,
                        &client,
                        cx,
                    );
                })
                .log_err();
            }
        }
    })
    .detach();

    cx.observe_global::<SettingsStore>({
        let editors = editors.clone();
        let client = client.clone();
        move |cx| {
            let new_provider = all_language_settings(None, cx).edit_predictions.provider;

            if new_provider != provider {

                provider = new_provider;
                assign_edit_prediction_providers(
                    &editors,
                    provider,
                    &client,
                    cx,
                );
            }
        }
    })
    .detach();
}

fn clear_zeta_edit_history(_: &zeta::ClearHistory, cx: &mut App) {
    if let Some(zeta) = zeta::Zeta::global(cx) {
        zeta.update(cx, |zeta, _| zeta.clear_history());
    }
}

fn assign_edit_prediction_providers(
    editors: &Rc<RefCell<HashMap<WeakEntity<Editor>, AnyWindowHandle>>>,
    provider: EditPredictionProvider,
    client: &Arc<Client>,
    cx: &mut App,
) {
    for (editor, window) in editors.borrow().iter() {
        _ = window.update(cx, |_window, window, cx| {
            _ = editor.update(cx, |editor, cx| {
                assign_edit_prediction_provider(
                    editor,
                    provider,
                    &client,
                    window,
                    cx,
                );
            })
        });
    }
}

fn assign_edit_prediction_provider(
    editor: &mut Editor,
    provider: EditPredictionProvider,
    client: &Arc<Client>,
    window: &mut Window,
    cx: &mut Context<Editor>,
) {
    // TODO: Do we really want to collect data only for singleton buffers?
    let singleton_buffer = editor.buffer().read(cx).as_singleton();

    match provider {
        EditPredictionProvider::None => {
            editor.set_edit_prediction_provider::<ZetaInlineCompletionProvider>(None, window, cx);
        }
        EditPredictionProvider::Zed => {
            let zeta =
                zeta::Zeta::register(client.clone(), cx);

            if let Some(buffer) = &singleton_buffer {
                if buffer.read(cx).file().is_some() {
                    zeta.update(cx, |zeta, cx| {
                        zeta.register_buffer(&buffer, cx);
                    });
                }
            }

            let provider =
                cx.new(|_| zeta::ZetaInlineCompletionProvider::new(zeta));

            editor.set_edit_prediction_provider(Some(provider), window, cx);
        }
    }
}
