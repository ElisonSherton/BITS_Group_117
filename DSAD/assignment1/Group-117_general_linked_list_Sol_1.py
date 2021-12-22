# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 2021 19:40:29 2020
@Program: BITS WILP SEM_1 DSAD Assignment 1
@author: Sai Prabhanjan Reddy, Vinayak Nayak and Niyati Aagarwal
@Section: Sec-2
@Group: 117
"""
import time


class LinkedTreeNode:
    """
    A General Tree linked list structure, Kept minimal to parent child relationship with no weights
    child_list: list of children for searched node
    company_name: input company name
    basic_tree: initial tree with company root node (boolean)
    """
    child_list = []
    company_name = None
    basic_tree = None

    def __init__(self, company_name):
        self.company_name = company_name
        self.child_list = []

    def add_node(self, node):
        # Add a preceding node
        self.child_list.append(node)

    def remove_node(self, node):
        # Remove the searched node
        self.child_list.remove(node)

    def find_child_and_parent(self, child_company, parent_company=None):
        # Get the node and parent
        if self.company_name == child_company:
            return self, parent_company
        for child in self.child_list:
            child_node, parent_company = child.find_child_and_parent(child_company, self)
            if child_node is not None:
                return child_node, parent_company
        return None, None


class InputParser:
    """
    This class is defined to parse the input file from given structure and call the required operations
    of a tree
    """
    input_lines = []
    list_ops = []
    write_out = None

    # Operations Naming Keywords
    add_root_node = "Company:"
    ops_count = "No of operations:"
    operation_acquire = "ACQUIRED"
    operation_detail = "DETAIL"
    operation_release = "RELEASE"

    def __init__(self, input_file="inputPS5.txt", output_file="outputPS5.txt"):
        """
        Takes the input file and parses it line by line and executes the required operations based on the
        listed keywords as mentioned in the below code.
        :param input_file: Set of instructions regarding Company general tree of operations
        :param output_file: Status of each operation from input list
        """

        self.list_ops = []
        self.input_lines = []
        try:
            with open(input_file) as f:
                self.input_lines = f.readlines()
                f.close()
                # print(self.lines)
        except EnvironmentError:
            print("Failed to read input_file")

        try:
            InputParser.write_out = open(output_file, "w")
        except EnvironmentError:
            print("Failed to open file in write mode", input_file)

    def execute_input(self):
        """
        Function to execute the instructions received from input and keywords as mentioned in parser function
        :return: executes the operations as per directive and exits if invalid input is supplied
        """
        # print(self.lines)
        if len(self.input_lines) > 0:
            for _l in self.input_lines:
                # print(line)
                task = _l.split()
                # print(self.operations)
                # print(task)
                # print(cmd, len(cmd))
                if len(task) == 2:
                    # Root node
                    if task[0].lower() == self.add_root_node.lower():
                        LinkedTreeNode.basic_tree = LinkedTreeNode(task[1])
                    if task[0].lower() == self.operation_detail.lower():
                        detail(task[1])
                    if task[0].lower() == self.operation_release.lower():
                        release(task[1])
                    if task[0].split(":")[0].lower() == self.operation_acquire.lower():
                        child = task[0].split(":")[-1]
                        parent = task[1].split(":")[-1]
                        acquire(parent, child)
        else:
            print("Input file is Invalid, Please check again")
            exit()

    def Print(str):
        if InputParser.write_out is None:
            print(str)
        else:
            print(str, file=InputParser.write_out)


def detail(company_name):
    """
    this function prints the parent and immediate children of company
    :param company_name: input company name to get the details
    :return: Company details such as list of child company names and count
    """
    if LinkedTreeNode.basic_tree is None:
        InputParser.Print("No Company information available")
    searched_node, parent = LinkedTreeNode.basic_tree.find_child_and_parent(company_name)
    if searched_node is not None:
        InputParser.Print("DETAIL: {0}".format(searched_node.company_name))
        if len(searched_node.child_list):
            children = [child.company_name for child in searched_node.child_list]
            # InputParser.Print("Parent Company: {0}".format(parent.company_name))
            InputParser.Print("Acquired companies: {0}".format(",".join(children)))
        else:
            # InputParser.Print("Parent Company: {0}".format(parent.company_name))
            InputParser.Print("Acquired companies: none")
        InputParser.Print("No of companies acquired: {0}".format(len(searched_node.child_list)))
    else:
        InputParser.Print("Company does not exist")


def acquire(parent_company, acquired_company):
    """
     Inserts the acquired_company as a new child node to the parent_company
    :param parent_company: The name of the company to which the child needs to be added
    :param acquired_company: The acquired company name
    :return: Prints the status of Acquisition as Success or Failure if no mentioned parent available
    """

    if LinkedTreeNode.basic_tree is None:
        InputParser.Print("No Company data exist")

    searched_node, parent = LinkedTreeNode.basic_tree.find_child_and_parent(acquired_company)

    if parent is not None:
        InputParser.Print("ACQUIRED FAILED: {0} BY:{1}".format(acquired_company, parent_company))
        return

    searched_node, parent = LinkedTreeNode.basic_tree.find_child_and_parent(parent_company)

    if searched_node is not None:
        searched_node.add_node(LinkedTreeNode(acquired_company))
        InputParser.Print("ACQUIRED SUCCESS:{1} Successfully acquired {0}".format(acquired_company, searched_node.company_name))
    else:
        InputParser.Print("ACQUIRED FAILED:{0} BY:{1}".format(acquired_company, parent_company))


def release(released_company):
    """
    removes the node mentioned in the released_company.
    :param released_company: The company name which to be removed
    :return: Prints the status of release as Success or Failure if no mentioned parent available
    """

    if LinkedTreeNode.basic_tree is None:
        InputParser.Print("No Company data exist")

    search_node, parent = LinkedTreeNode.basic_tree.find_child_and_parent(released_company)
    # Checking for node existance
    if search_node is not None:
        if parent is None:  # Root node
            LinkedTreeNode.basic_tree = None
        else:
            if len(search_node.child_list) > 0:
                for _child in search_node.child_list:
                    parent.add_node(LinkedTreeNode(_child.company_name))
                    # InputParser.Print("Child stitched Company: {0}".format(parent.company_name))
                parent.remove_node(search_node)
            else:
                parent.remove_node(search_node)
            InputParser.Print("RELEASED SUCCESS: released {0} successfully.".format(search_node.company_name))
    else:
        InputParser.Print("RELEASED FAILED: released {0} failed".format(released_company))


if __name__ == "__main__":
    stat = time.time()
    gTree = InputParser()
    gTree.execute_input()
    gTree.write_out.close()
    print(time.time()-stat)
