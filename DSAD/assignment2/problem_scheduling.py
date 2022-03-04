'''
@author Vinayak
@email vnayak@okkular.io / nayakvinayak95@gmail.com
@create date 2022-03-04 21:06:47
@modify date 2022-03-04 22:24:40
@desc [Job Scheduling algorithm]
'''

from typing import List
from pathlib import Path

class problem:
    def __init__(self, name:str, deadline:int, bonus:int):
        """[initializes a problem node/struct to hold name, deadline, bonus for the problem]

        Args:
            deadline (int): _description_
            bonus (int): _description_
        """
        self.name = name
        self.deadline = deadline
        self.bonus = bonus

def custom_sort(problem_list:List, attribute:str):
    """[Given a list of problems and the attribute on which to sort (i.e. deadline or bonus), sorts the sequence of problems accordingly and returns the same]

    Args:
        problem_list (List): [A list of problem objects]
        attribute (str): [A string based on which the given set of problems need to be sorted]

    Returns:
        Nothing, sorts the given list in place
    """
    
    if len(problem_list) > 1:
        
        # Find the mid of the array
        mid = len(problem_list) // 2
        
        # Divide the array into two halves
        left, right = problem_list[:mid], problem_list[mid:]

        # Sort the first half
        custom_sort(left, attribute)

        # Sort the second half
        custom_sort(right, attribute)

        i, j, k = [0] * 3

        # Copy the data temporarily to left and right arrays
        while i < len(left) and j < len(right):
            if attribute == "deadline":
                comparison = left[i].deadline < right[j].deadline
            elif attribute == "bonus":
                comparison = left[i].bonus < right[j].bonus
            
            if comparison:
                problem_list[k] = left[i]
                i += 1
            else:
                problem_list[k] = right[j]
                j += 1
        
            k += 1
        
        # Check whether any elements are pending in the left array
        while i < len(left):
            problem_list[k] = left[i]
            i += 1
            k += 1

        # Check whether any elements are pending in the right array 
        while j < len(right):
            problem_list[k] = right[j]
            j += 1
            k += 1

    
# Write the main logic of the code here
if __name__ == "__main__":
    # Read the input file
    inputs = [x.replace("\n", "") for x in Path("inputPS5.txt").read_text().splitlines()]
    
    # Infer the number of test cases from the file
    n_test_cases = int(inputs[0].replace("No of use-cases:", "").strip())

    for c in range(n_test_cases):
        # Read the deadlines and bonuses for the cth test case
        deadlines = inputs[1 + 2*c]
        bonuses = inputs[(c + 1) * 2]

        deadlines = [int(x.strip()) for x in deadlines.replace("Deadlines: ", "").split(" ")]
        bonuses = [int(x.strip()) for x in bonuses.replace("Bonus: ", "").split(" ")]

        # Iterate over the deadlines and bonuses and create a problem list for this test case
        problem_list = []
        for idx, (deadline, bonus) in enumerate(zip(deadlines, bonuses)):
            name = chr(65 + idx)
            pb = problem(name, deadline, bonus)
            problem_list.append(pb)
        
        for node in problem_list:
            print(f"Name {node.name:<3} Deadline {node.deadline:<.2f} Bonus {node.bonus:<.2f}")

        print("Sorted")

        custom_sort(problem_list, "bonus")
        for node in problem_list:
            print(f"Name {node.name:<3} Deadline {node.deadline:<.2f} Bonus {node.bonus:<.2f}")
        
        print("_"*50)
