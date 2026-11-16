import argparse
import binascii


def chunks(s, n):
    return [s[i:i + n] for i in range(0, len(s), n)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("bitcode")
    parser.add_argument("header")
    args = parser.parse_args()

    with open(args.bitcode, "rb") as f:
        data = f.read()
    data_hex = binascii.b2a_hex(data).decode("ascii")

    with open(args.header, "w") as f:
        f.write("#include <string>\n")
        f.write("const int binary_ir_length = %d;\n" % len(data))
        f.write("std::vector<std::string> binary_ir_vector = \n{")
        for chunk in chunks(data_hex, 10000):
            f.write('\tstd::string("')
            for i in range(len(chunk) // 2):
                f.write("\\x" + chunk[2 * i:2 * (i + 1)])
            f.write('", %d),\n' % (len(chunk) // 2))
        f.write("\n};\n\n")
        f.write("std::string binary_ir;")
        f.write("\n")

    print("[*] %s: %d bytes -> %s" % (args.bitcode, len(data), args.header))


if __name__ == "__main__":
    main()
