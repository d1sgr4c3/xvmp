cmake_minimum_required(VERSION 3.20)
project(xVMP LANGUAGES CXX)

find_package(LLVM REQUIRED CONFIG)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION} at ${LLVM_DIR}")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

separate_arguments(LLVM_DEFINITIONS_LIST NATIVE_COMMAND ${LLVM_DEFINITIONS})
add_definitions(${LLVM_DEFINITIONS_LIST})
include_directories(SYSTEM ${LLVM_INCLUDE_DIRS})

if(NOT LLVM_ENABLE_RTTI)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-rtti")
endif()
if(NOT LLVM_ENABLE_EH)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-exceptions")
endif()

set(XVMP_VM_SEED "" CACHE STRING "Fixed seed for the opcode permutation")
set(XVMP_CLANG "" CACHE FILEPATH "clang used to compile the xVMP interpreter")

if(XVMP_CLANG)
  set(XVMP_CLANG_PATH ${XVMP_CLANG})
else()
  find_program(XVMP_CLANG_FROM_LLVM clang HINTS ${LLVM_TOOLS_BINARY_DIR} NO_DEFAULT_PATH)
  if(XVMP_CLANG_FROM_LLVM)
    set(XVMP_CLANG_PATH ${XVMP_CLANG_FROM_LLVM})
  else()
    find_program(XVMP_CLANG_PATH clang)
  endif()
endif()

if(NOT XVMP_CLANG_PATH)
  message(FATAL_ERROR "clang not found, pass -DXVMP_CLANG=/path/to/clang")
endif()
message(STATUS "xVMP interpreter compiler: ${XVMP_CLANG_PATH}")

set(XVMP_GEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/gen)
file(MAKE_DIRECTORY ${XVMP_GEN_DIR})

set(XVMP_OPCODES_H ${XVMP_GEN_DIR}/xvmp_opcodes.h)
set(XVMP_INTERPRETER_BC ${CMAKE_CURRENT_BINARY_DIR}/xVMPInterpreter.bc)
set(XVMP_VM_H ${XVMP_GEN_DIR}/vm.h)

set(XVMP_GEN_OPCODES_CMD
    ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/scripts/gen_vm_config.py
    --out ${XVMP_OPCODES_H})
if(XVMP_VM_SEED)
  list(APPEND XVMP_GEN_OPCODES_CMD --seed ${XVMP_VM_SEED})
endif()

add_custom_command(
  OUTPUT ${XVMP_OPCODES_H}
  COMMAND ${XVMP_GEN_OPCODES_CMD}
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/scripts/gen_vm_config.py
  VERBATIM)

add_custom_command(
  OUTPUT ${XVMP_INTERPRETER_BC}
  COMMAND ${XVMP_CLANG_PATH} -O0 -Xclang -disable-O0-optnone -emit-llvm
          -I ${XVMP_GEN_DIR}
          -c ${CMAKE_CURRENT_SOURCE_DIR}/vm/xVMPInterpreter.c
          -o ${XVMP_INTERPRETER_BC}
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/vm/xVMPInterpreter.c
          ${CMAKE_CURRENT_SOURCE_DIR}/vm/xVMPInterpreter.h
          ${XVMP_OPCODES_H}
  VERBATIM)

add_custom_command(
  OUTPUT ${XVMP_VM_H}
  COMMAND ${Python3_EXECUTABLE}
          ${CMAKE_CURRENT_SOURCE_DIR}/scripts/interpreter-ir2str.py
          ${XVMP_INTERPRETER_BC} ${XVMP_VM_H}
  DEPENDS ${XVMP_INTERPRETER_BC}
          ${CMAKE_CURRENT_SOURCE_DIR}/scripts/interpreter-ir2str.py
  VERBATIM)

add_library(xVMP SHARED xVMP/xVMP.cpp Plugin.cpp ${XVMP_OPCODES_H} ${XVMP_VM_H})
target_include_directories(xVMP PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/xVMP
  ${XVMP_GEN_DIR})
