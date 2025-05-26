def read_grid_mdp_problem_p1(file_path):
    problem = {}
    with open(file_path) as file:
        problem["seed"] = int(file.readline().split()[-1])
        problem["noise"] = float(file.readline().split()[-1])
        problem["livingReward"] = float(file.readline().split()[-1])
        
        # Parse and store the grid
        problem["grid"] = getGrid(file, problem)

        # Parse and store the policy
        policy = []
        for line in file:
            policy.append(line.split())
        problem["policy"] = policy

    return problem

def read_grid_mdp_problem_p2(file_path):
    problem = {}
    with open(file_path) as file:
        problem["discount"] = float(file.readline().split()[-1])
        problem["noise"] = float(file.readline().split()[-1])
        problem["livingReward"] = float(file.readline().split()[-1])
        problem["numIter"] = int(file.readline().split()[-1])
        
        # Parse and store the grid
        problem["grid"] = getGrid(file, problem)

        # Parse and store the policy
        policy = []
        for line in file:
            policy.append(line.split())
        problem["policy"] = policy

    return problem

def read_grid_mdp_problem_p3(file_path):
    problem = {}
    with open(file_path) as file:
        problem["discount"] = float(file.readline().split()[-1])
        problem["noise"] = float(file.readline().split()[-1])
        problem["livingReward"] = float(file.readline().split()[-1])
        problem["numIter"] = int(file.readline().split()[-1])
        
        # Parse and store the grid
        problem["grid"] = getGrid(file, problem)
    
    return problem


def getGrid(file, problem):
    file.readline() # Skip the grid header
    grid, line = [], file.readline()
    while "policy" not in line and line != '':
        # Parse the grid line
        path = []
        for state in line.split():
            if state == 'S' or state == '_':
                path.append({"State": state, "hasPlayer": False, "Reward": problem["livingReward"]})
            elif state == '#':
                path.append({"State": '#', "hasPlayer": False, "Reward": 0})
            else:   # Terminal States
                try:
                    reward = int(state)
                except ValueError:
                    reward = float(state)
                finally:
                    path.append({"State": str(reward), "hasPlayer": False, "Reward": reward})
        
        grid.append(path)
        # Read the next line
        line = file.readline()
    return grid
