## Feature Parity Rule

All features and bug fixes **must** be implemented in **all three client
languages** (Python, Rust, Go) before a release is cut. No single-language
changes are permitted unless the feature is inherently language-specific
(e.g. the Home Assistant `custom_components/` which is Python-only).

**Rationale:** the three clients share the same API surface and serve the
same user base. Leaving one behind creates confusion and support burden.
