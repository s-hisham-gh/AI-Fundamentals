import sys, grader, parse
import random

def play_episode(problem):
    seed, noise = problem["seed"], problem["noise"]
    grid, policy = problem["grid"], problem["policy"]
    random.seed(seed)

    player_position, cumulative_reward = None, 0.0
    for row_number, row in enumerate(grid):
        for column_number, cell in enumerate(row):
            if cell["State"] == 'S':
                cell["hasPlayer"] = True
                player_position = (row_number, column_number)

    experience = "Start state:\n"
    experience += format_grid(grid, cumulative_reward)
    experience += separation()

    intended_action = policy[player_position[0]][player_position[1]]
    action = None

    while action != "exit":
        action = noisy_action(intended_action, noise)
        experience += f"Taking action: {action} (intended: {intended_action})\n"
        
        direction_map = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1), "exit": (0, 0)}
        intended_pos = (player_position[0] + direction_map[action][0], player_position[1] + direction_map[action][1])
        reward = grid[player_position[0]][player_position[1]]["Reward"]

        if valid_move(grid, intended_pos):
            grid[player_position[0]][player_position[1]]["hasPlayer"] = False
            player_position = intended_pos
            if action != "exit":
                grid[player_position[0]][player_position[1]]["hasPlayer"] = True

        intended_action = policy[player_position[0]][player_position[1]]

        experience += f"Reward received: {float(reward)}\n"
        cumulative_reward += reward
        experience += "New state:\n"
        experience += format_grid(grid, cumulative_reward)
        if action != "exit":
            experience += separation()

    return experience

def format_grid(grid, cumulative_reward):
    grid_str = ""
    for row in grid:
        for cell in row:
            if cell["hasPlayer"]:
                grid_str += "    P"
            else:
                grid_str += f"{cell['State']:>5}"
        grid_str += "\n"
    grid_str += f"Cumulative reward sum: {round(cumulative_reward, 2)}"
    return grid_str

def separation():
    return "\n" + "-" * 44 + " \n"

def noisy_action(intended_action, noise_level):
    if intended_action == 'exit':
        return 'exit'
    action_space = {
        'N': ['N', 'E', 'W'],
        'E': ['E', 'S', 'N'],
        'S': ['S', 'W', 'E'],
        'W': ['W', 'N', 'S']
    }
    return random.choices(
        population=action_space[intended_action],
        weights=[1 - noise_level * 2, noise_level, noise_level]
    )[0]

def valid_move(grid, position):
    return (
        0 <= position[0] < len(grid)
        and 0 <= position[1] < len(grid[0])
        and grid[position[0]][position[1]]["State"] != '#'
    )

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)
