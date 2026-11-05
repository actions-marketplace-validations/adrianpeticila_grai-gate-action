#!/usr/bin/env bash
set -uo pipefail

root="${GITHUB_WORKSPACE:-$PWD}"
cd "$root" || exit 2

target="${GRAI_PATH:-.}"
base="${GITHUB_BASE_REF:-}"
verbose=""
if [ "${GRAI_VERBOSE:-false}" = "true" ]; then
  verbose="-v"
fi

files=()
if [ -n "$base" ]; then
  git fetch --no-tags origin "$base" >/dev/null 2>&1 || true
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    if [ "$target" != "." ]; then
      case "$f" in
        "$target"/*) ;;
        *) continue ;;
      esac
    fi
    [ -f "$f" ] && files+=("$f")
  done < <(git diff --name-only --diff-filter=ACMR "origin/$base...HEAD" -- '*.md' '*.mdx' '*.txt' 2>/dev/null || true)
else
  while IFS= read -r -d '' f; do
    files+=("$f")
  done < <(find "$target" -type f \( -name '*.md' -o -name '*.mdx' -o -name '*.txt' \) -not -path '*/.git/*' -not -path '*/node_modules/*' -print0)
fi

if [ "${#files[@]}" -eq 0 ]; then
  echo "grai-gate: no markdown files to score."
  exit 0
fi

status=0
if [ -n "$verbose" ]; then
  grai-gate "$verbose" "${files[@]}" || status=$?
else
  grai-gate "${files[@]}" || status=$?
fi

if [ "$status" -eq 2 ]; then
  echo "grai-gate: input error."
  exit 2
fi

if [ "${GRAI_FAIL:-false}" = "true" ] && [ "$status" -eq 1 ]; then
  echo "grai-gate: slop found and fail-on-slop is on."
  exit 1
fi

echo "grai-gate: advisory run finished. The job stays green."
exit 0
