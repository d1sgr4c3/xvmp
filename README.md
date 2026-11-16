# xVMP

Code virtualization pass plugin for LLVM 21.

## Build

```
cmake . -DLLVM_DIR=/path/to/llvm-21/lib/cmake/llvm
make
```

Builds `libxVMP.so`.

## Use

Select functions with the `vmp` annotation:

```c
#ifdef ENABLE_GOVMP
__attribute__((annotate("vmp")))
#endif
uint32_t SECRET(unsigned long input) { ... }
```

```
clang -fpass-plugin=/path/to/libxVMP.so -DENABLE_GOVMP input.c -o out
opt -load-pass-plugin=/path/to/libxVMP.so -passes=xvmp input.bc
```
