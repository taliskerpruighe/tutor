#!/usr/bin/env bash
# Builds the fixtures and runs validate.py against the passing fixture and
# each of the nine deliberately-broken fixtures, demonstrating that every
# check can PASS and every check can FAIL (by name).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CT_DIR="$(dirname "$HERE")"          # lab/challenge-three
VALIDATE="$CT_DIR/validate.py"

echo "=== building fixtures ==="
python3 "$HERE/build_fixtures.py"

run_good() {
    echo
    echo "=== GOOD fixture (expect all PASS) ==="
    CHALLENGE3_LAB_DIR="$HERE/good" \
    CHALLENGE3_REPO_ROOT="$HERE/good/reporoot" \
    CHALLENGE3_MATERIALS_ROOT="$HERE/good/reporoot/content/21-challenges/materials/challenge-three/fixtureco" \
    CHALLENGE3_BASELINE_MANIFEST="$HERE/good/baseline.txt" \
    python3 "$VALIDATE" fixtureco
    echo "exit code: $?"
}

run_broken() {
    n="$1"
    dir="$HERE/broken/check$n"
    if [ "$n" = "8" ]; then
        reporoot="$dir/reporoot"
        materials="$reporoot/content/21-challenges/materials/challenge-three/fixtureco"
        baseline="$dir/baseline.txt"
    else
        reporoot="$HERE/good/reporoot"
        materials="$HERE/good/reporoot/content/21-challenges/materials/challenge-three/fixtureco"
        baseline="$HERE/good/baseline.txt"
    fi
    echo
    echo "=== BROKEN fixture check$n (expect check_${n}_* to FAIL) ==="
    set +e
    CHALLENGE3_LAB_DIR="$dir" \
    CHALLENGE3_REPO_ROOT="$reporoot" \
    CHALLENGE3_MATERIALS_ROOT="$materials" \
    CHALLENGE3_BASELINE_MANIFEST="$baseline" \
    python3 "$VALIDATE" fixtureco
    code=$?
    set -e
    echo "exit code: $code"
    if [ "$code" -eq 0 ]; then
        echo "!!! expected non-zero exit for broken/check$n, got 0"
        exit 1
    fi
}

run_good

for n in 1 2 3 4 5 6 7 8 9; do
    run_broken "$n"
done

echo
echo "=== all broken fixtures correctly failed; good fixture correctly passed ==="
