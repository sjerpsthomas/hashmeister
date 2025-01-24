
# (Executes the 'hash' command)
def execute_hash(dir: str | None, out: str | None, thorough: bool) -> None:
    import os

    # Handle defaults
    if dir == None:
        dir = os.getcwd()
    if out == None:
        out = os.path.join(dir, "hash.hm")
    
    # Hash and save
    import hash
    hash.hash_and_save(dir, out, thorough)


# (Executes the 'compare' command)
def execute_compare(first: str, second: str) -> None:
    import compare

    # Print the difference between the two files
    compare.print_difference(first, second)


# (Main entrypoint)
if __name__ == "__main__":
    import argparse

    # Create parser
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    command = parser.add_subparsers(dest="command",required=True)

    # 'hash' command: hashes the contents of a folder
    hash_parser: argparse.ArgumentParser = command.add_parser("hash")
    # The directory to hash
    hash_parser.add_argument("-d", "--dir")
    # The file to output the hashed contents to
    hash_parser.add_argument("-o", "--out")
    # A flag to enable thorough (byte-wise, instead of only file size) lookup
    hash_parser.add_argument("-t", "--thorough", action="store_true")

    # 'compare' command: compares two files containing hashed folder contents
    compare_parser: argparse.ArgumentParser = command.add_parser("compare")
    # The first output file to compare
    compare_parser.add_argument("first", type=str)
    # The second output file to compare
    compare_parser.add_argument("second", type=str)

    args = parser.parse_args()

    # Execute corresponding command
    if args.command == "hash":
        execute_hash(args.dir, args.out, args.thorough)
    elif args.command == "compare":
        execute_compare(args.first, args.second)
