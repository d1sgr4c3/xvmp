#include "llvm/Config/llvm-config.h"
#include "llvm/IR/PassManager.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"

#include "xVMP.h"

using namespace llvm;

static void addXVMP(ModulePassManager &MPM, OptimizationLevel) {
  MPM.addPass(XVMPPass());
}

extern "C" LLVM_ATTRIBUTE_WEAK PassPluginLibraryInfo llvmGetPassPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "xVMP", LLVM_VERSION_STRING,
          [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, ModulePassManager &MPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "xvmp") {
                    MPM.addPass(XVMPPass());
                    return true;
                  }
                  return false;
                });
            PB.registerPipelineStartEPCallback(addXVMP);
          }};
}
