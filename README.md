# Zedless

Matrix Room: [#zedless:privatevoid.net](https://matrix.to/#/#zedless:privatevoid.net)

This is Zedless, a fork of Zed that's designed to be privacy-friendly and local-first.

This repository contains scripts to patch the Zed source code.

Patching is done by structurally editing the syntax tree using [ast-grep](https://ast-grep.github.io/) (powered by [tree-sitter](https://tree-sitter.github.io/tree-sitter/)). This should allow the project to keep up with the fast pace of upstream development.

Zedless is currently work-in-progress. Feel free to contribute!

---

### Planned Changes from Upstream

This is a list of things that Zedless will do differently.

- No reliance on proprietary cloud services
  - Components and features that strictly rely on non-selfhostable cloud services will be removed.
- No spyware
  - Telemetry and automatic crash reporting will be removed.
- Priority on bringing your own infrastructure
  - Any feature that makes use of a network service will allow you to configure which provider to use in a standard format, e.g. by specifying the base URL of an API.
  - Any such feature will not have a list of "default providers".
  - Any such feature will be disabled by default.
- No CLA
  - Contributors' copyright shall not be reassigned.
  - No rugpulls.
