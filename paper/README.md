# WMT26 camera-ready system paper

This directory contains the non-anonymous ACL-format camera-ready paper for team `alonso`'s WMT26 Model Compression system.

Build from the repository root with:

```bash
make -C paper
```

The ACL style is pinned as the `paper/acl-style-files` Git submodule. Clone with `--recurse-submodules`, or initialize an existing clone with:

```bash
git submodule update --init --recursive
```

Current status: the paper includes the official WMT26 blind-test CometKiwi-XXL, MetricX-24-XXL, artifact-size, and H100-throughput results. It keeps local A6000 results clearly separated, states that the organizer's released peak-memory field is host RSS rather than GPU VRAM, and retains the global-FP4 versus selective-NF4 configuration confound.

Official WMT26 guidance says system papers are non-anonymous and normally 4--6 pages and use EMNLP/ACL formatting. Before uploading, confirm that the author metadata exactly matches the submission system and follow any venue-specific camera-ready instructions.
