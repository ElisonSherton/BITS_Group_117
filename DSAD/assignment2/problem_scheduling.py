'''
@author Vinayak
@email vnayak@okkular.io / nayakvinayak95@gmail.com
@create date 2022-03-04 21:06:47
@modify date 2022-03-07 16:25:30
@desc [Problem Scheduling algorithm]
'''

from typing import List, Tuple
from pathlib import Path

# Define two global variables one for indicating if we need to finish all problems
# And another to tell if the order of processes needs to be mentioned
SCHEDULE_ALL = False
SCHEDULE_ORDER = False

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
    
    def __repr__(self) -> str:
        return f"Problem: {self.name:<5}, Deadline:{self.deadline:2d}, Bonus:{self.bonus:2d}\n"

def custom_sort(problem_list:List, attribute:str, descending:bool = True):
    """[Given a list of problems and the attribute on which to sort (i.e. deadline or bonus), sorts the sequence of problems accordingly and returns the same]

    Args:
        problem_list (List): [A list of problem objects]
        attribute (str): [A string based on which the given set of problems need to be sorted]
        descending (bool): [A boolean which tells whether to sort in increasing/decreasing order]

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
                if descending:
                    comparison = left[i].deadline > right[j].deadline
                else:
                    comparison = left[i].deadline < right[j].deadline
                
            elif attribute == "bonus":
                if descending:
                    comparison = left[i].bonus > right[j].bonus
                else:
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

def schedule_problems(problem_list:List, attribute:str, schedule_all:bool = False) -> Tuple:
    """[Given a list of problems, schedules them to maximize the bonus]

    Args:
        problem_list (List): [List of problems]
        attribute (str): [Attribute which needs to be maximized]

    Returns:
        Tuple: [Ideal sequence of problems, best possible bonus]
    """
    # Sort the problem list based on the attribute to be maximized
    custom_sort(problem_list, attribute)

    # Find the total number of problems in the problem list
    total_problems = len(problem_list)

    # Generate a slots array for scheduling the best problems
    slots = [""] * total_problems

    # Accumulate bonus in a variable, initialize it to zero
    max_bonus = 0

    # Iterate over the problem list
    for problem in problem_list:
        deadline = problem.deadline
        bonus = problem.bonus
        
        # Look for the latest time slot for this problem which is not empty
        for idx in range(min(deadline - 1, total_problems),-1,-1):
            slt = slots[idx]
            if slt == "":
                slots[idx] = problem.name
                max_bonus += bonus
                break
    
    if schedule_all:
        # Look at the problems which haven't been scheduled so far
        # They can be scheduled in any order but it makes sense to schedule 
        # them in the ascending order of their deadlines from a practical point of view
        unscheduled_problems = []
        for problem in problem_list:
            if not problem.name in slots:
                unscheduled_problems.append(problem)
        custom_sort(unscheduled_problems, "deadline", descending = False)

        unscheduled_problems_counter = 0
        for idx in range(total_problems):
            if slots[idx] == "":
                slots[idx] = unscheduled_problems[unscheduled_problems_counter].name
                unscheduled_problems_counter += 1            
            
    return (slots, max_bonus)

    

# Write the main logic of the code here
if __name__ == "__main__":
    # Read the input file
    inputs = [x.replace("\n", "") for x in Path("inputPS5.txt").read_text().splitlines()]
    
    # Infer the number of test cases from the file
    n_test_cases = int(inputs[0].split(":")[-1].strip())

    # Create two containers to hold the bonuses and sequence of completion for each problem
    final_bonuses = []
    final_sequences = []

    for c in range(n_test_cases):
        # Read the deadlines and bonuses for the cth test case
        deadlines = inputs[1 + 2*c].split(":")[-1].strip()
        bonuses = inputs[(c + 1) * 2].split(":")[-1].strip()
        
        deadlines = [int(x.strip()) for x in deadlines.split(" ")]
        bonuses = [int(x.strip()) for x in bonuses.split(" ")]

        # Iterate over the deadlines and bonuses and create a problem list for this test case
        problem_list = []
        for idx, (deadline, bonus) in enumerate(zip(deadlines, bonuses)):
            name = f"Problem_{idx + 1}"
            pb = problem(name, deadline, bonus)
            problem_list.append(pb)
        
        # Run the scheduling algorithm and accumulate the sequence of problems and the bonus accrued
        slots, bonus = schedule_problems(problem_list, "bonus", schedule_all = SCHEDULE_ALL)
        final_bonuses.append(bonus)
        final_sequences.append(slots)
    
    # Log the bonuses to an output file
    with open("outputPS5.txt", "w") as f:
        for bonus in final_bonuses:
            f.writelines(f"{bonus}\n")
    
    # Log the order in which problems are scheduled if asked
    if SCHEDULE_ORDER:
        with open("output_with_order.txt", "w") as f:
            for idx, (sequence, bonus) in enumerate(zip(final_sequences, final_bonuses), start = 1):
                f.writelines(f"Test case: {idx:2d} Bonus: {bonus:4d} Job Sequence: {str(sequence):<20}\n")