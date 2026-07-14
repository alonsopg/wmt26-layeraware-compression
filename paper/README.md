# WMT26 system paper draft

This directory contains the non-anonymous ACL-format draft for team `alonso`'s WMT26 Model Compression system paper.

Build from the repository root with:

```bash
make -C paper
```

The ACL style is pinned as the `paper/acl-style-files` Git submodule. Clone with `--recurse-submodules`, or initialize an existing clone with:

```bash
git submodule update --init --recursive
```

Current status: local-development results are complete; official WMT26 blind-test quality and organizer H100 measurements must be inserted when released. The draft deliberately labels every current measurement as local and lists the global-FP4 versus selective-NF4 configuration confound.

Official WMT26 guidance says system papers are non-anonymous and normally 4--6 pages, use EMNLP/ACL formatting, and are due August 7, 2026 AoE. Check the task mailing list and WMT26 page again before submission in case instructions change.
