#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
BUILD_DIR="${SW_BUILD_DIR:-$ROOT/build}"
CC="${CC:-gcc}"
CFLAGS=(-std=c99 -Wall -Wextra)

usage() {
    cat <<'EOF'
Uso: ./sw <comando> [argumentos]

  ./sw run arquivo.starwars      transpila, compila e executa (aceita entrada com <)
  ./sw build arquivo.starwars    gera build/<nome>.c e build/<nome> sem executar
  ./sw c arquivo.starwars        mostra o C gerado (aceita --tokens e --ast)
  ./sw check arquivo.starwars    só verifica erros léxicos, sintáticos e semânticos
  ./sw test                      roda a suíte de testes
  ./sw regen [pasta]             regenera o C dos exemplos (padrão: examples/generated)
  ./sw demo                      executa os exemplos válidos e mostra cada tipo de erro
  ./sw clean                     apaga a pasta build

Exemplo: ./sw run examples/valid/02_complete.starwars < examples/valid/02_complete.input.txt
EOF
}

fail() {
    echo "$1" >&2
    exit "${2:-1}"
}

transpiler() {
    PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}" python3 -B -m starwars "$@"
}

require_source() {
    [[ $# -gt 0 ]] || fail "informe o arquivo .starwars. Veja ./sw para ajuda." 2
    [[ -f "$1" ]] || fail "arquivo não encontrado: $1"
}

build_program() {
    local source="$1"
    local name
    name="$(basename "$source" .starwars)"
    C_FILE="$BUILD_DIR/$name.c"
    BINARY="$BUILD_DIR/$name"
    command -v "$CC" >/dev/null || fail "compilador C '$CC' não encontrado. Instale o GCC (Fedora: sudo dnf install gcc; Debian/Ubuntu: sudo apt install gcc)."
    mkdir -p "$BUILD_DIR"
    local errors
    if ! errors="$(transpiler "$source" -o "$C_FILE" 2>&1 >/dev/null)"; then
        fail "$errors"
    fi
    "$CC" "${CFLAGS[@]}" "$C_FILE" -o "$BINARY"
}

show_program() {
    local source="$1"
    local input="${source%.starwars}.input.txt"
    echo "==> ${source#"$ROOT"/}"
    build_program "$source"
    if [[ -f "$input" ]]; then
        echo "(entrada: ${input#"$ROOT"/})"
    else
        input=/dev/null
    fi
    printf '%s\n\n' "$("$BINARY" <"$input")"
}

show_error() {
    local source="$1"
    echo "==> ${source#"$ROOT"/}"
    sed 's/^/    /' "$source"
    transpiler "$source" 2>&1 >/dev/null || true
    echo
}

command="${1:-help}"
shift || true

case "$command" in
    run)
        require_source "$@"
        build_program "$1"
        exec "$BINARY"
        ;;
    build)
        require_source "$@"
        build_program "$1"
        echo "C gerado: $(realpath --relative-base=. "$C_FILE")"
        echo "Executável: $(realpath --relative-base=. "$BINARY")"
        ;;
    c)
        require_source "$@"
        transpiler "$@"
        ;;
    check)
        require_source "$@"
        transpiler "$@" >/dev/null
        echo "$1: nenhum erro encontrado."
        ;;
    test)
        cd "$ROOT"
        python3 -B -m unittest discover -s tests "$@"
        ;;
    regen)
        destination="${1:-$ROOT/examples/generated}"
        for source in "$ROOT"/examples/valid/*.starwars "$ROOT"/examples/demo.starwars; do
            transpiler "$source" -o "$destination/$(basename "$source" .starwars).c"
        done
        ;;
    demo)
        for source in "$ROOT"/examples/valid/*.starwars "$ROOT"/examples/demo.starwars; do
            show_program "$source"
        done
        for source in "$ROOT"/examples/invalid/*.starwars; do
            show_error "$source"
        done
        ;;
    clean)
        rm -rf "$BUILD_DIR"
        ;;
    help | -h | --help)
        usage
        ;;
    *)
        usage >&2
        fail "comando desconhecido: $command" 2
        ;;
esac
