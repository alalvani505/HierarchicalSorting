import csv

from collections import defaultdict
from src.logger import log


class TreeNode:

    def __init__(self, key, value, parent_key, data):
        self.key = key
        self.parent_key = parent_key
        self.value = value
        self.children = []
        self.data = data


class HierarchicalTree:

    def __init__(self, data_path, sort_column):
        self.nodes = {}
        self.levels = defaultdict(list)
        self.sort_column = sort_column
        self.delimiter = "|" # todo: input?
        self.properties = [] # updated in _load_csv
        self.fieldnames = [] # updated in _load_csv
        self.has_decimals = False # updated in _load_csv
        self._load_csv(data_path)
        self._build_tree()
        if self.has_decimals:
            self._update_for_decimals()
        self.sorted = self._sort()

    def _load_csv(self, data_path):
        """
        Using csv dict reader: https://docs.python.org/3/library/csv.html#csv.DictReader
        This avoids any split string problems, while also allowing looping through single columns

        :param data_path: csv file to parse
        """
        with open(data_path) as file:
            reader = csv.DictReader(file, delimiter=self.delimiter)

            self.fieldnames = reader.fieldnames
            self.properties = [x for x in reader.fieldnames if x.startswith("prop")]
            self._load(reader)

    def _load(self, data):
        """
        Helper function that loops through a dictionary object to:
        1. build a tree node
        2. store tree node in a nodes dict to reference later

        :param data: dictionary object
        """
        for row in data:
            metric_data = float(row[self.sort_column])
            if not self.has_decimals and not metric_data.is_integer():
                self.has_decimals = True

            key = ""
            parent_key = ""
            level = 0
            for p in self.properties:
                if row[p] != "$total":
                    parent_key = key
                    key += self.delimiter + row[p] if len(parent_key) > 0 else row[p]
                    level += 1
            log.debug(f"_load: {level} [{key}] -> [{parent_key}]: {row}")
            self.levels[level] += [key]
            self.nodes[key] = TreeNode(key, metric_data, parent_key, row)

    def _build_tree(self):
        """
        Builds a tree from the leaf nodes back to the roots using the parent key:
        2: 1 2 5 7
        1:  3   6
        0:    4    root
        """
        for level in range(len(self.properties), -1, -1):
            log.debug(f"_build: level {level}: {self.levels[level]}")
            for node_key in self.levels[level]:
                child = self.nodes[node_key]
                parent = self.nodes[child.parent_key]
                if child.parent_key != node_key:
                    # this is to avoid a cycle from root -> root
                    parent.children.append(child)

    def _update_for_decimals(self):
        """
        Noticed a difference between input and output.
        This might be caused by using a dataset and setting the field to a decimal

        In CSV, we have to hack our way through this issue
        :return:
        """
        cols = [x for x in self.fieldnames if x not in self.properties]
        for node in self.nodes.values():
            for col in cols:
                node.data[col] = str(float(node.data[col]))

    def _sort(self):
        """
       This is where some sorting happens and reading the tree
       todo: optimize by only sorting once when called.
       :return: sorted output
       """
        result = "|".join(self.fieldnames) + "\n"
        q = [self.nodes[self.levels[0][0]]]
        while q:
            node = q.pop()
            result += "|".join(node.data.values()) + "\n"
            # sort ascending, pop descending
            q.extend(sorted(node.children, key=lambda x: x.value))
        return result[:-1]  # remove trailing new line

    # def __str__(self):
    #    return self.sorted


def compare(actual, result):
    """
    Helper function to validate
    :param actual: string result from output of hierarchical sort
    :param result: file.open() some file
    :return: True or False
    """
    actual = actual.split('\n')
    result = result.split('\n')
    if len(actual) != len(result):
        log.info("failed on line counts")
        log.info(f"Actual:{len(actual)}")
        log.info(f"Result:{len(result)}")
        return False
    loop = True
    for i in range(len(result)):
        if result[i] != actual[i]:
            loop = False
            log.info(f"diff on line {i}")
            log.info(f"Actual:{actual[i]}")
            log.info(f"Result:{result[i]}")
    return loop