#!/usr/bin/env bash
# build.sh -- renders the challenge-two noncompete corpus from
# lab/challenge-two/sources/manifest.tsv into
# content/21-challenges/materials/challenge-two/{contracts,to-do}/.
#
# Safe to re-run: overwrites its own outputs. Skips gracefully (with a
# clear message) for any source file that has not been authored yet, so
# this can be run at any point during authoring.
#
# Usage:
#   bash lab/challenge-two/build.sh
#
# Env overrides (used by the smoke test to avoid touching real output
# dirs):
#   OUTDIR      contracts output directory (default: real corpus path)
#   TODO_OUTDIR to-do output directory      (default: real corpus path)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

SOURCES_DIR="${SCRIPT_DIR}/sources"
MANIFEST="${SOURCES_DIR}/manifest.tsv"
CONTRACTS_SRC_DIR="${SOURCES_DIR}/contracts"
TODO_SRC_DIR="${SOURCES_DIR}/to-do"
RENDER_PDF="${SCRIPT_DIR}/render_pdf.py"

OUTDIR="${OUTDIR:-${REPO_ROOT}/content/21-challenges/materials/challenge-two/contracts}"
TODO_OUTDIR="${TODO_OUTDIR:-${REPO_ROOT}/content/21-challenges/materials/challenge-two/to-do}"

LO_PROFILE="file:///tmp/lo-challenge-two"

mkdir -p "${OUTDIR}" "${TODO_OUTDIR}"

if [[ ! -f "${MANIFEST}" ]]; then
    echo "error: manifest not found at ${MANIFEST}" >&2
    exit 1
fi

TMPDIR_BUILD="$(mktemp -d /tmp/challenge-two-build.XXXXXX)"
trap 'rm -rf "${TMPDIR_BUILD}"' EXIT

echo "== challenge-two build =="
echo "manifest:      ${MANIFEST}"
echo "contracts out: ${OUTDIR}"
echo "to-do out:     ${TODO_OUTDIR}"
echo "temp dir:      ${TMPDIR_BUILD}"
echo

render_pandoc_docx() {
    local src="$1" out="$2"
    pandoc "${src}" -f markdown -t docx -o "${out}" < /dev/null
}

render_reportlab_pdf() {
    local src="$1" out="$2"
    python3 "${RENDER_PDF}" "${src}" "${out}" < /dev/null
}

render_soffice_pdf() {
    # markdown -> docx (via pandoc, into a temp dir) -> pdf (via soffice,
    # into a temp dir), then moved to the final output filename. The
    # intermediate docx never lands in the contracts/ output directory.
    local src="$1" out="$2"
    local base tmp_docx tmp_pdf tmp_stem

    base="$(basename "${src}")"
    tmp_stem="${base%.*}"
    tmp_docx="${TMPDIR_BUILD}/${tmp_stem}.docx"

    pandoc "${src}" -f markdown -t docx -o "${tmp_docx}" < /dev/null

    soffice --headless --norestore \
        "-env:UserInstallation=${LO_PROFILE}" \
        --convert-to pdf --outdir "${TMPDIR_BUILD}" \
        "${tmp_docx}" < /dev/null >/dev/null

    tmp_pdf="${TMPDIR_BUILD}/${tmp_stem}.pdf"
    if [[ ! -f "${tmp_pdf}" ]]; then
        echo "  error: soffice did not produce expected output ${tmp_pdf}" >&2
        return 1
    fi
    mv "${tmp_pdf}" "${out}"
}

render_copy_txt() {
    local src="$1" out="$2"
    cp "${src}" "${out}"
}

render_count=0
skip_count=0

# Read the manifest on file descriptor 3 so that converters invoked
# inside the loop (pandoc, soffice, python3) cannot consume the
# manifest's remaining lines from stdin.
{
    read -r -u 3 _header
    while IFS=$'\t' read -r -u 3 n source_file output_filename producer state ancillary style confvar sevform flags; do
        [[ -z "${n:-}" ]] && continue

        src_path="${CONTRACTS_SRC_DIR}/${source_file}"
        out_path="${OUTDIR}/${output_filename}"

        printf 'contract %s: %s (%s)\n' "${n}" "${output_filename}" "${producer}"

        if [[ ! -f "${src_path}" ]]; then
            printf '  skip: source not yet authored (%s)\n' "${src_path}"
            skip_count=$((skip_count + 1))
            continue
        fi

        case "${producer}" in
            pandoc-docx)
                render_pandoc_docx "${src_path}" "${out_path}"
                ;;
            reportlab-pdf)
                render_reportlab_pdf "${src_path}" "${out_path}"
                ;;
            soffice-pdf)
                render_soffice_pdf "${src_path}" "${out_path}"
                ;;
            copy-txt)
                render_copy_txt "${src_path}" "${out_path}"
                ;;
            *)
                echo "  error: unknown producer '${producer}' for contract ${n}" >&2
                exit 1
                ;;
        esac

        printf '  done: %s\n' "${out_path}"
        render_count=$((render_count + 1))
    done
} 3< "${MANIFEST}"

echo
echo "-- to-do materials --"
if compgen -G "${TODO_SRC_DIR}"/*.txt > /dev/null 2>&1; then
    for f in "${TODO_SRC_DIR}"/*.txt; do
        dest="${TODO_OUTDIR}/$(basename "${f}")"
        cp "${f}" "${dest}"
        printf '  copied: %s\n' "${dest}"
    done
else
    echo "  skip: no *.txt files yet in ${TODO_SRC_DIR}"
fi

echo
echo "== build summary =="
echo "contracts rendered: ${render_count}"
echo "contracts skipped (source not yet authored): ${skip_count}"
