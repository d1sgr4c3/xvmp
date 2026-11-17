# xVMP

Code virtualization pass plugin for LLVM 21.

## Build

```
cmake . -DLLVM_DIR=/path/to/llvm-build/lib/cmake/llvm
make
```

`LLVM_DIR` points at a built LLVM (directory containing `LLVMConfig.cmake`), not a source checkout.

The interpreter compiler is resolved in order: `-DXVMP_CLANG`, clang from the LLVM build, clang from `PATH`.

Options:

- `-DXVMP_CLANG=/path/to/clang`
- `-DXVMP_VM_SEED=42` — fixed opcode permutation seed, default is random per clean build

Builds `libxVMP.so`; generates `gen/xvmp_opcodes.h` and `gen/vm.h` (regenerated when the interpreter sources or scripts change).

## Use

Selection is annotation-based, function names are irrelevant:

| Annotation | Effect |
|---|---|
| `annotate("vmp")` on a function | virtualize this function |
| `annotate("novmp")` on a function | exclude this function, overrides `vmp` |
| `annotate("cpp_vmp")` on any function in a module | virtualize the whole module |
| `annotate("cpp_novmp")` on any function in a module | exclude the whole module |

The virtualized body is replaced with a call to `vm_interpreter_<function>`.

```c
#ifdef ENABLE_GOVMP
__attribute__((annotate("vmp")))
#endif
uint32_t SECRET(unsigned long input) { ... }
```

```
clang -fpass-plugin=/path/to/libxVMP.so -DENABLE_GOVMP input.c -o out
```

If you prefer to work with bitcode directly:

```
opt -load-pass-plugin=/path/to/libxVMP.so -passes=xvmp input.bc
```
