import os, sys

def read_graph_search_problem(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    start_state = lines[0].split(':')[1].strip()
    goal_state = lines[1].split(':')[1].strip()

    stateSpaceGraph = {}
    heuristic = {}
    for line in lines[2:]:
        parts = line.split()
        if len(parts) == 3:
            from_node, to_node, cost = parts
            cost = float(cost) 
            if from_node not in stateSpaceGraph:
                stateSpaceGraph[from_node] = []
            stateSpaceGraph[from_node].append(( cost,to_node))
        elif len(parts) == 2:  
            node, heuristic_value = parts
            heuristic[node] = float(heuristic_value)  
    problem = [start_state, [goal_state], stateSpaceGraph, heuristic]
    return problem

def read_8queens_search_problem(file_path):
    problem = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for row, line in enumerate(lines):
            for column, character in enumerate(line.strip()):
                if character == 'q':
                    problem.append((row, column)) 
    return problem

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')