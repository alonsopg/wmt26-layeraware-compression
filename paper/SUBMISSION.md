# WMT26 camera-ready submission package

Submission number: **46**

The repository includes a reproducible packager for the final paper. From the repository root, run:

```bash
scripts/package_camera_ready.sh
```

Equivalently:

```bash
make -C paper submission
```

The command rebuilds the paper, rejects unresolved citations, overfull boxes, non-A4 output, or unembedded fonts, and runs ACL PubCheck when it is installed. It also verifies that the isolated LaTeX source bundle compiles.

Generated files are written to `artifacts/camera-ready/`:

- `wmt26-submission-46-camera-ready.pdf` — upload-ready paper.
- `wmt26-submission-46-camera-ready-source.zip` — self-contained LaTeX source.
- `wmt26-submission-46-camera-ready.sha256` — checksums for both files.

The generated directory is intentionally ignored by Git because the canonical PDF and source are already tracked as `paper/main.pdf`, `paper/main.tex`, and `paper/references.bib`.

Before uploading through SoftConf:

1. Confirm that the author name, affiliation, title, and email exactly match the submission metadata.
2. Upload the generated PDF and the source ZIP if the camera-ready form requests source files.
3. Download the uploaded PDF once and visually inspect it.
4. Save the final SoftConf confirmation or receipt.

WMT26 states that system papers are non-anonymous, normally 4–6 pages, and follow the EMNLP/ACL format. The published camera-ready deadline is September 11, 2026 AoE: <https://www2.statmt.org/wmt26/>.
