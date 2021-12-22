'''
@author Vinayak, Sai, Niyati
@email 2021fc04135@wilp.bits-pilani.ac.in
@create date 2021-12-19 16:43:05
@modify date 2021-12-22 16:22:22
@desc [Code to implement company acquisition in the form of a general tree using linked lists]
'''

from typing import List
from pathlib import Path
import re, time

class Node:
    def __init__(self, parent_company: object, company_name: str):
        """[Create a node object given the company's name and it's parent company]

        Args:
            parent_company (str): [Name of the parent company]
            company_name (str): [Name of this company]
        """

        self.company_name = company_name
        self.parent_company = parent_company
        
        # Maintain a list of companies acquired by this company
        self.acquired_companies = []

class Tree:
    def __init__(self, root: Node):
        """[Create a tree data structure to hold the organization hierarchy]

        Args:
            root (Node): [The root node/ super parent company]
        """
        self.root = root
    
    def search(self, company_name: str) -> List:
        """[Searches for a given company in the organization structure and returns the same using BFS]

        Args:
            company_name (str): [Name of the company to be searched]

        Returns:
            List: [boolean: whether or not found, Node/String: Node if found, empty string if not found]
        """
        
        # Create a queue for traversing the tree
        search_queue = []
        
        # Load the root in the queue to start processing
        search_queue.append(self.root)
        n = len(search_queue)

        while n > 0:
            # Pop the first element from the front
            front = search_queue.pop(0)

            # Check if this node is the company we're looking for
            if front.company_name == company_name:
                return [True, front]
            
            # Otherwise load the current company's subsidiaries into the queue
            for subsidiary in front.acquired_companies:
                search_queue.append(subsidiary)
            
            n = len(search_queue)

        return [False, "Requested company doesn't exist"]
    
    def acquire(self, parent_company: str, acquired_company: str) -> str:
        """[Given a parent and subsidiary company, add the subsidiary company to the list of companies acquired by parent company]

        Args:
            parent_company (str): [Name of the parent company]
            acquired_company (str): [Name of the acquired company]

        Returns:
            str: [Status of the acquisition]
        """

        if self.root is None:
            return "No company data available"
        
        presence = self.search(parent_company)
        acquired_presence = self.search(acquired_company)
        # Check if the company which is acquiring (parent company) is already present in the hierarchy or not
        if not presence[0]:
            return f"ACQUIRED FAILED: {acquired_company} BY:{parent_company}"
        # Check if the company that is to be acquired is already in the hierarchy
        elif acquired_presence[0]:
            return f"ACQUIRED FAILED: {acquired_company} BY:{parent_company}"
        # Otherwise, add the acquired company as a subsidiary of the parent company
        else:
            subsidiary_company = Node(presence[1], acquired_company)
            presence[1].acquired_companies.append(subsidiary_company)
            return f"ACQUIRED SUCCESS: {parent_company} Successfully acquired {acquired_company}"
    
    def detail(self, company_name: str) -> str:
        """[Given a company's name, prints out the details of that company]

        Args:
            company_name (str): [Name of the company]

        Returns:
            str: [Details of the company]
        """
        
        if self.root is None:
            return "No company data available"

        presence = self.search(company_name)
        
        # Check if the company requested for exists in the organization hierarchy
        # If not, then print detail failed
        if not presence[0]:
            return f"DETAIL: {company_name} does not exist"
        
        else:
            # Get the node for the company
            company = presence[1]

            # Construct the detail string as per the output format
            details_string =  f"DETAIL: {company_name}"
            subsidiaries = [x.company_name for x in company.acquired_companies]
            if len(subsidiaries):
                details_string += f"\nAcquired companies: {', '.join(subsidiaries)}"
                details_string += f"\nNo of companies acquired: {len(subsidiaries)}"
            else:
                details_string += f"\nAcquired companies: none\nNo of companies acquired: 0"
                
        return details_string
    
    def release(self, company_name: str) -> str:
        """[Given a company name, releases the company from the organizational hierarchy]

        Args:
            company_name (str): [Name of the company to be removed]

        Returns:
            str: [Status of the removal operation]
        """
        if self.root is None:
            return "No company data available"

        presence = self.search(company_name)

        # Check if the requested company to release exists in the organizational hierarchy
        if not presence[0]:
            return f"RELEASED FAILED: released {company_name} failed."
        # Check if the requested company is the master company, if so raise an exception
        else:
            to_remove = presence[1]
            if self.root.company_name == company_name:
                self.root = None
                return f"RELEASED SUCCESS: released {company_name} successfully."
            else:
                # Create an empty list for new subsidiaries (devoid of this company)
                new_subsidiaries = []
                
                # In this company's parent, find the mention of this company and remove it
                for subsidiary in to_remove.parent_company.acquired_companies:
                    if not(subsidiary.company_name == company_name):
                        new_subsidiaries.append(subsidiary)
                    else:
                        for grandson_subsidiary in to_remove.acquired_companies:
                            grandson_subsidiary.parent_company = to_remove.parent_company
                            new_subsidiaries.append(grandson_subsidiary)

                to_remove.parent_company.acquired_companies = new_subsidiaries
            return f"RELEASED SUCCESS: released {company_name} successfully."
            
def parse_input(input_pth: str):
    """[Reads an input file, performs the operations in it in a line by line fashion and prints the output to another file]
    """  
    # Strip leading and trailing whitespaces from instructions and read it
    instructions = [x.strip() for x in Path(input_pth).read_text().split("\n")]
    
    # Open an output file and start logging everything over there
    with open("outputPS5.txt", "w") as f:
        # Read the base company name and number of operations
        base_conglomerate = instructions[0].replace("Company: ", "")
        n = int(re.findall(r"\d+", instructions[1])[0])
        f.writelines(f"Company: {base_conglomerate}\nNo of operations: {n}\n")
        company_hierarchy = Tree(Node(None, base_conglomerate))
            
        # Start from the third line of instruction from the input text file and read next n lines
        for instruction in instructions[2 : (n + 2)]:
            try:
                # Write the details of a company
                if instruction.lower().startswith("detail"):
                    company_name = instruction[7:]
                    to_write = company_hierarchy.detail(company_name)
                # Acquire a company and log it to the output file
                elif instruction.lower().startswith("acquired"):
                    instruction = instruction[9:]
                    acquired_company = re.findall(r"(.+?) BY", instruction)[0]
                    parent_company = re.findall(r"BY:(.+)", instruction)[0]
                    to_write = company_hierarchy.acquire(parent_company, acquired_company)
                # Release a company and log it to the output file
                elif instruction.lower().startswith("release"):
                    to_release = instruction[8:]
                    to_write = company_hierarchy.release(to_release)
            except Exception as e:
                to_write = "ERROR: Couldn't interpret the instruction"

            f.writelines(f"{to_write}\n")

if __name__ == "__main__":
    start = time.time()
    parse_input("inputPS5.txt")                
    print(time.time()-start)