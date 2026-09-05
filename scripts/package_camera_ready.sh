#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PAPER_DIR="$ROOT/paper"
PDF="$PAPER_DIR/main.pdf"
LOG="$PAPER_DIR/main.log"
SUBMISSION_ID="${SUBMISSION_ID:-46}"
STEM="wmt26-submission-${SUBMISSION_ID}-camera-ready"
OUT="${OUT_DIR:-$ROOT/artifacts/camera-ready}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

check_latex_log() {
  local log_file="$1"
  local warning_pattern='Overfull \\hbox|undefined citations|undefined references|LaTeX Warning'

  if grep -Eq "$warning_pattern" "$log_file"; then
    grep -En "$warning_pattern" "$log_file" >&2
    fail "LaTeX log contains a blocking warning: $log_file"
  fi
}

for command_name in latexmk pdfinfo pdffonts zip sha256sum; do
  command -v "$command_name" >/dev/null 2>&1 ||
    fail "required command not found: $command_name"
done

[[ -f "$PAPER_DIR/acl-style-files/acl.sty" ]] ||
  fail "ACL style submodule is missing; run: git submodule update --init --recursive"

make -C "$PAPER_DIR"

[[ -f "$PDF" && -f "$LOG" ]] || fail "paper build did not produce main.pdf and main.log"
check_latex_log "$LOG"

pages="$(pdfinfo "$PDF" | awk '/^Pages:/ {print $2}')"
page_size="$(pdfinfo "$PDF" | awk -F: '/^Page size:/ {sub(/^[[:space:]]+/, "", $2); print $2}')"
[[ "$page_size" == *A4* ]] || fail "paper is not A4: $page_size"

if ! pdffonts "$PDF" | awk 'NR > 2 && $5 != "yes" {bad=1} END {exit bad}'; then
  fail "one or more PDF fonts are not embedded"
fi

aclpubcheck_bin="${ACLPUBCHECK:-}"
if [[ -z "$aclpubcheck_bin" ]] && command -v aclpubcheck >/dev/null 2>&1; then
  aclpubcheck_bin="$(command -v aclpubcheck)"
fi
if [[ -z "$aclpubcheck_bin" && -x "$HOME/miniconda3/envs/iwslt-2026/bin/aclpubcheck" ]]; then
  aclpubcheck_bin="$HOME/miniconda3/envs/iwslt-2026/bin/aclpubcheck"
fi
if [[ -n "$aclpubcheck_bin" ]]; then
  [[ -x "$aclpubcheck_bin" ]] || fail "ACLPUBCHECK is not executable: $aclpubcheck_bin"
  (cd "$TMP" && "$aclpubcheck_bin" -p other "$PDF")
else
  echo "WARNING: aclpubcheck not found; PDF structural checks still passed" >&2
fi

source_dir="$TMP/source"
mkdir -p "$source_dir/acl-style-files" "$OUT"
cp "$PAPER_DIR/main.tex" "$PAPER_DIR/references.bib" "$PAPER_DIR/Makefile" "$source_dir/"
cp "$PAPER_DIR/acl-style-files/acl.sty" \
   "$PAPER_DIR/acl-style-files/acl_natbib.bst" \
   "$source_dir/acl-style-files/"

# Confirm that the standalone source bundle builds without repository-local files.
make -C "$source_dir"
check_latex_log "$source_dir/main.log"
make -C "$source_dir" clean

(cd "$source_dir" && zip -X -q -r "$TMP/${STEM}-source.zip" .)
cp "$PDF" "$TMP/${STEM}.pdf"

(
  cd "$TMP"
  sha256sum "${STEM}.pdf" "${STEM}-source.zip" > "${STEM}.sha256"
)

cp "$TMP/${STEM}.pdf" "$TMP/${STEM}-source.zip" "$TMP/${STEM}.sha256" "$OUT/"

echo "Camera-ready package created:"
echo "  PDF:    $OUT/${STEM}.pdf"
echo "  source: $OUT/${STEM}-source.zip"
echo "  hashes: $OUT/${STEM}.sha256"
echo "  pages:  $pages ($page_size)"
