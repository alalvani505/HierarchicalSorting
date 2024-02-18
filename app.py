import argparse

from utils.logger import log
from utils.csvNodeSort import HierarchicalTree, compare

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "file",
        type=str,
        help="absolute path to csv file to sort"
    )
    parser.add_argument(
        "--sort_column",
        type=str,
        default="net_sales",
        help="optional parameter to change sort column. defaults to net_sales"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="absolute path to output sorted csv file"
    )
    parser.add_argument(
        "-va", "--validate",
        type=str,
        help="absolute path to csv file to validate against"
    )
    parser.add_argument(
        "-v", "--verbose",
        help="Print sorted list to standard out",
        action="store_true"
    )
    args = parser.parse_args()

    # if args.verbose:
    #     log.setLevel(logging.DEBUG)

    output = HierarchicalTree(args.file, "net_sales").sorted
    if args.verbose:
        log.info(output)

    if args.output:
        with open(args.output, "w+") as f:
            f.write(output)
            f.close()

    if args.validate:
        with open(args.validate) as file:
            validate = file.read()
            file.close()
            log.info(compare(output, validate))
