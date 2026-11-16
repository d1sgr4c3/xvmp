#include <stdint.h>
#include <assert.h>

#include "xvmp_opcodes.h"

uint64_t unpack_code(int size);
uint64_t unpack_data(uint64_t offset, int size);
uint64_t unpack_addr(uint64_t address, int size);
void pack_store_addr(uint64_t address, uint64_t value, int size);
uint64_t get_value_with_size(uint8_t value_size, uint8_t value_type);
uint64_t get_value();
void alloca_handler();
void load_handler();
void store_handler();
void binaryOperator_handler();
void gep_handler();
void cmp_handler();
void cast_handler();
void br_handler();
void return_handler();
void vm_interpreter();
void data_seg_clear();
