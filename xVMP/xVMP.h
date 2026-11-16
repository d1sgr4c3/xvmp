#ifndef XVMP_XVMP_H
#define XVMP_XVMP_H

#include "llvm/IR/Module.h"
#include "llvm/IR/PassManager.h"
#include <string>

struct XVMPPass : public llvm::PassInfoMixin<XVMPPass> {
  llvm::PreservedAnalyses run(llvm::Module &M,
                              llvm::ModuleAnalysisManager &AM);
  static bool isRequired() { return true; }
};

bool is_interpreter_function(llvm::Function *targetFunction);
std::string get_vm_function_name(llvm::Function *targetFunction);

#endif
