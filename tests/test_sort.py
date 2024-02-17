import time
import unittest

from definitions import DATA_DIR
from src.main.csvNodeSort import HierarchicalTree, compare


def test_data_small_input():
    in_file = f"{DATA_DIR}/data-small-input.txt"
    out_file = f"{DATA_DIR}/data-small-output.txt"

    with open(out_file) as file:
        output = file.read()
        file.close()
        s = HierarchicalTree(in_file, "net_sales").sorted
        assert compare(s, output)


def test_data_big_input():
    in_file = f"{DATA_DIR}/data-big-input.txt"
    out_file = f"{DATA_DIR}/data-big-output.txt"

    with open(out_file) as file:
        output = file.read()
        file.close()
        s = HierarchicalTree(in_file, "net_sales").sorted
        assert compare(s, output)


@unittest.skip("Used for performance testing")
def test_performance():
    in_file = f"{DATA_DIR}/data-big-input.txt"
    starttime = time.time()
    runs = 1000
    for i in range(runs):
        HierarchicalTree(in_file, "net_sales").sorted

    print(f"total time for {runs} big sorts: ", round((time.time() - starttime), 2))

