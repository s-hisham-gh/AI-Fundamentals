import sys
import grader
import parse

def value_iteration(problem):
    valueGrid = []
    for i in range(len(problem["grid"])):
        valueGrid.append([])
        for j in range(len(problem["grid"][i])):
            if problem["grid"][i][j]["State"] == '#':
                valueGrid[i].append("#")
            else:
                valueGrid[i].append(0)

    return_value = "V_k=0\n"
    return_value += get_val_grid(valueGrid)

    for k in range(1, problem["numIter"]):
        new_valueGrid = [[0 for _ in range(len(problem["grid"][0]))] for __ in range(len(problem["grid"]))]
        policyGrid = [[0 for _ in range(len(problem["grid"][0]))] for __ in range(len(problem["grid"]))]
        for i in range(len(problem["grid"])):
            for j in range(len(problem["grid"][i])):
                if problem["grid"][i][j]["State"] == '#':
                    new_valueGrid[i][j], policyGrid[i][j] = '#', '#'
                else:
                    new_valueGrid[i][j], policyGrid[i][j] = get_val_act(i, j, problem, valueGrid)

        valueGrid = new_valueGrid
        return_value += f"V_k={k}\n"
        return_value += get_val_grid(valueGrid)
        return_value += f"pi_k={k}\n"
        return_value += get_pol_grid(policyGrid)
    return return_value[:-1]

def get_val_grid(valueGrid):
    val_str = ''
    for i in range(len(valueGrid)):
        for j in range(len(valueGrid[i])):
            if valueGrid[i][j] == "#":
                val_str += "| ##### |"
            else:
                val_str += f"|{valueGrid[i][j]:7.2f}|"
        val_str += '\n'
    return val_str

def get_pol_grid(policyGrid):
    pol_str = ''
    for i in range(len(policyGrid)):
        for j in range(len(policyGrid[i])):
            if policyGrid[i][j] == "exit":
                pol_str += "| x |"
            elif policyGrid[i][j] == "#":
                pol_str += "| # |"
            else:
                pol_str += f"|{policyGrid[i][j]:^3}|"
        pol_str += '\n'
    return pol_str

def get_val_act(i, j, problem, valueGrid):
    if problem["grid"][i][j]["State"] == '#':
        return "#", "#"
    elif problem["grid"][i][j]["State"] in ('S', '_'):
        actValMap = {act: calculate_value(i, j, problem, valueGrid, act) for act in ["N", "E", "S", "W"]}
        return actValMap[max(actValMap, key=actValMap.get)], max(actValMap, key=actValMap.get)
    else:
        return problem["grid"][i][j]["Reward"], "exit"

def calculate_value(i, j, problem, valueGrid, intended_action):
    perp_action = {'N': ['E', 'W'], 'E': ['S', 'N'], 'S': ['W', 'E'], 'W': ['N', 'S']}
    d_vec = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    noise, grid, gamma = problem["noise"], problem["grid"], problem["discount"]

    if intended_action == "exit":
        return grid[i][j]["Reward"]

    succ_pos = [
        (i + d_vec[intended_action][0], j + d_vec[intended_action][1]),
        (i + d_vec[perp_action[intended_action][0]][0], j + d_vec[perp_action[intended_action][0]][1]),
        (i + d_vec[perp_action[intended_action][1]][0], j + d_vec[perp_action[intended_action][1]][1])
    ]

    for pos in succ_pos:
        if not (0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]) and grid[pos[0]][pos[1]]["State"] != '#'):
            succ_pos[succ_pos.index(pos)] = (i, j)

    curr_reward = grid[i][j]["Reward"]

    return (
        (1 - 2 * noise) * (curr_reward + gamma * valueGrid[succ_pos[0][0]][succ_pos[0][1]]) +
        noise * (curr_reward + gamma * valueGrid[succ_pos[1][0]][succ_pos[1][1]]) +
        noise * (curr_reward + gamma * valueGrid[succ_pos[2][0]][succ_pos[2][1]])
    )

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)
