# Limitations

- Local hardware is one RTX A6000 (48 GiB), not the organizer H100 80 GiB.
- The native layer-aware system is validated locally, but its speed and memory behavior must still be confirmed on the organizer H100 environment.
- COMET and MetricX are intentionally omitted from local smoke testing unless compatible reference data and metric environments are available.
- Reference-backed WMT25 data was used locally; WMT26 blind-test quality remains unknown.
- The full local comparison covers English–Chinese only; Czech–German, English–Egyptian Arabic, and WMT26 blind-test behavior remain unknown.
- Storage-codec generation time reflects an eager quality-equivalent decoded-weight emulation and excludes Zstd decompression, so only its quality, exact encoded payload, and post-decode VRAM are directly interpretable.
