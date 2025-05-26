import sys
import grader
import parse

def policy_evaluation(problem):
    valueGrid = []
    for i in range(len(problem["grid"])):
        valueGrid.append([])
        for j in range(len(problem["grid"][i])):
            if problem["grid"][i][j]["State"] == '#':
                valueGrid[i].append("#")
            else:
                valueGrid[i].append(0)

    return_value = "V^pi_k=0\n"
    return_value += get_val_grid(valueGrid)

    for k in range(1, problem["numIter"]):
        new_valueGrid = [[0 for _ in range(len(problem["grid"][0]))] for __ in range(len(problem["grid"]))]
        for i in range(len(problem["grid"])):
            for j in range(len(problem["grid"][i])):
                if problem["grid"][i][j]["State"] == '#':
                    new_valueGrid[i][j] = '#'
                else:
                    new_valueGrid[i][j] = calculate_value(i, j, problem, valueGrid)
        valueGrid = new_valueGrid
        return_value += f"V^pi_k={k}\n"
        return_value += get_val_grid(valueGrid)
    return return_value[:-1]

def calculate_value(i, j, problem, valueGrid):
    perp_action = {'N': ['E', 'W'], 'E': ['S', 'N'], 'S': ['W', 'E'], 'W': ['N', 'S']}
    d_vec = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
    noise, grid, policy, gamma = problem["noise"], problem["grid"], problem["policy"], problem["discount"]
    intended_action = policy[i][j]

    if intended_action == "exit":
        return grid[i][j]["Reward"]

    succ_position = [
        (i + d_vec[intended_action][0], j + d_vec[intended_action][1]),
        (i + d_vec[perp_action[intended_action][0]][0], j + d_vec[perp_action[intended_action][0]][1]),
        (i + d_vec[perp_action[intended_action][1]][0], j + d_vec[perp_action[intended_action][1]][1])
    ]

    for pos in succ_position:
        if not (0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0]) and grid[pos[0]][pos[1]]["State"] != '#'):
            succ_position[succ_position.index(pos)] = (i, j)

    curr_reward = grid[i][j]["Reward"]
    return (
        (1 - 2 * noise) * (curr_reward + gamma * valueGrid[succ_position[0][0]][succ_position[0][1]]) +
        noise * (curr_reward + gamma * valueGrid[succ_position[1][0]][succ_position[1][1]]) +
        noise * (curr_reward + gamma * valueGrid[succ_position[2][0]][succ_position[2][1]])
    )

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

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)
