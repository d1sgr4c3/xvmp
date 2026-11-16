#!/bin/bash
set -ex

ROOT_PATH=$(cd "$(dirname "$0")/.." && pwd)
CLANG="${XVMP_CLANG:-clang}"
OUT_DIR="${XVMP_OUT_DIR:-$ROOT_PATH/manual-build}"
SEED="${XVMP_VM_SEED:-}"

mkdir -p "$OUT_DIR/gen"

if [ -n "$SEED" ]; then
    python3 "$ROOT_PATH/scripts/gen_vm_config.py" --seed "$SEED" --out "$OUT_DIR/gen/xvmp_opcodes.h"
else
    python3 "$ROOT_PATH/scripts/gen_vm_config.py" --out "$OUT_DIR/gen/xvmp_opcodes.h"
fi

"$CLANG" -O0 -Xclang -disable-O0-optnone -emit-llvm -I "$OUT_DIR/gen" -c "$ROOT_PATH/vm/xVMPInterpreter.c" -o "$OUT_DIR/xVMPInterpreter.bc"

python3 "$ROOT_PATH/scripts/interpreter-ir2str.py" "$OUT_DIR/xVMPInterpreter.bc" "$OUT_DIR/gen/vm.h"

llvm-dis "$OUT_DIR/xVMPInterpreter.bc" -o "$OUT_DIR/xVMPInterpreter.ll" || true
