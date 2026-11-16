import argparse
import random

OPCODES = [
    "ALLOCA_OP",
    "LOAD_OP",
    "STORE_OP",
    "BinaryOperator_OP",
    "GEP_OP",
    "CMP_OP",
    "CAST_OP",
    "BR_OP",
    "Call_OP",
    "Ret_OP",
]

BINOPS = [
    ("BINOP_ADD", 13),
    ("BINOP_FADD", 14),
    ("BINOP_SUB", 15),
    ("BINOP_FSUB", 16),
    ("BINOP_MUL", 17),
    ("BINOP_FMUL", 18),
    ("BINOP_UDIV", 19),
    ("BINOP_SDIV", 20),
    ("BINOP_FDIV", 21),
    ("BINOP_UREM", 22),
    ("BINOP_SREM", 23),
    ("BINOP_FREM", 24),
    ("BINOP_SHL", 25),
    ("BINOP_LSHR", 26),
    ("BINOP_ASHR", 27),
    ("BINOP_AND", 28),
    ("BINOP_OR", 29),
    ("BINOP_XOR", 30),
]

ICMPS = [
    ("ICMP_EQ", 32),
    ("ICMP_NE", 33),
    ("ICMP_UGT", 34),
    ("ICMP_UGE", 35),
    ("ICMP_ULT", 36),
    ("ICMP_ULE", 37),
    ("ICMP_SGT", 38),
    ("ICMP_SGE", 39),
    ("ICMP_SLT", 40),
    ("ICMP_SLE", 41),
]

REMAP_SIZE = 64


def build_header(rng):
    op_values = list(range(1, len(OPCODES) + 1))
    rng.shuffle(op_values)

    binop_values = rng.sample(range(1, 256), len(BINOPS))
    icmp_values = rng.sample(range(1, 256), len(ICMPS))
    br_values = rng.sample(range(1, 256), 2)

    binop_remap = [0] * REMAP_SIZE
    for (_, llvm_opcode), value in zip(BINOPS, binop_values):
        binop_remap[llvm_opcode] = value

    icmp_remap = [0] * REMAP_SIZE
    for (_, llvm_predicate), value in zip(ICMPS, icmp_values):
        icmp_remap[llvm_predicate] = value

    lines = []
    lines.append("#ifndef XVMP_OPCODES_H")
    lines.append("#define XVMP_OPCODES_H")
    lines.append("")
    lines.append("#include <stdint.h>")
    lines.append("")
    for name, value in zip(OPCODES, op_values):
        lines.append("#define %-18s 0x%02X" % (name, value))
    lines.append("")
    lines.append("#define OP_TOTAL            0x%02X" % len(OPCODES))
    lines.append("#define POINTER_SIZE 8")
    lines.append("")
    for (name, _), value in zip(BINOPS, binop_values):
        lines.append("#define %-12s 0x%02X" % (name, value))
    lines.append("")
    for (name, _), value in zip(ICMPS, icmp_values):
        lines.append("#define %-8s 0x%02X" % (name, value))
    lines.append("")
    lines.append("#define BR_TYPE_UNCOND 0x%02X" % br_values[0])
    lines.append("#define BR_TYPE_COND   0x%02X" % br_values[1])
    lines.append("")
    lines.append("#define XVMP_BINOP_REMAP_SIZE %d" % REMAP_SIZE)
    lines.append(
        "static const uint8_t XVMP_BINOP_REMAP[XVMP_BINOP_REMAP_SIZE] = {%s};"
        % ",".join(str(v) for v in binop_remap)
    )
    lines.append("#define XVMP_ICMP_REMAP_SIZE %d" % REMAP_SIZE)
    lines.append(
        "static const uint8_t XVMP_ICMP_REMAP[XVMP_ICMP_REMAP_SIZE] = {%s};"
        % ",".join(str(v) for v in icmp_remap)
    )
    lines.append("")
    lines.append("#endif")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    if args.seed is None:
        rng = random.SystemRandom()
    else:
        rng = random.Random(args.seed)

    header = build_header(rng)
    with open(args.out, "w") as f:
        f.write(header)
    print("[*] %s" % args.out)


if __name__ == "__main__":
    main()
