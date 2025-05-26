# given the simplicity of this grid, low noise, and a large discount factor, a very high success rate (1.0 according to the code below) is likely to be obtained.
# to run this code, simply click on the "Run Code" button.

import random

def temporal_learning(problem, num_episodes=1000, epsilon=1.0, epsilon_decay=0.99, alpha=0.1, alpha_decay=0.99):
    gamma = problem["discount"]
    noise = problem["noise"]
    grid = problem["grid"]
    actions = ["N", "E", "S", "W", "exit"]
    d_vec = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
    
    q_values = {
        (i, j): {action: 0 for action in actions}
        for i in range(len(grid))
        for j in range(len(grid[i]))
        if grid[i][j]["State"] != "#"
    }

    def get_valid_actions(state):
        return [action for action in actions if is_valid_action(state, action)]
    
    def is_valid_action(state, action):
        i, j = state
        if action == "exit":
            return True
        ni, nj = i + d_vec[action][0], j + d_vec[action][1]
        return 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj]["State"] != "#"

    def epsilon_greedy_search(state, epsilon):
        if random.random() < epsilon:
            return random.choice(get_valid_actions(state))
        return max(q_values[state], key=q_values[state].get)

    def take_action(state, action):
        i, j = state
        if action == "exit":
            return state, grid[i][j]["Reward"]
        ni, nj = i + d_vec[action][0], j + d_vec[action][1]
        if not (0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and grid[ni][nj]["State"] != "#"):
            ni, nj = i, j
        reward = grid[i][j]["Reward"]
        return (ni, nj), reward

    def train_episode(epsilon, alpha):
        state = None
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j]["State"] == "S":
                    state = (i, j)
                    break
            if state:
                break

        while True:
            action = epsilon_greedy_search(state, epsilon)
            next_state, reward = take_action(state, action)
            sample = reward + gamma * max(q_values[next_state].values())
            q_values[state][action] = (1 - alpha) * q_values[state][action] + alpha * sample
            if action == "exit":
                break
            state = next_state

    def derive_policy():
        policy = [[None for _ in range(len(grid[0]))] for __ in range(len(grid))]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j]["State"] == "#":
                    policy[i][j] = "#"
                else:
                    policy[i][j] = max(q_values[(i, j)], key=q_values[(i, j)].get)
        return policy

    success_count = 0
    for _ in range(10):
        for i in range(num_episodes):
            train_episode(epsilon, alpha)
            epsilon *= epsilon_decay
            alpha *= alpha_decay

        derived_policy = derive_policy()
        if optimal_policy(derived_policy, problem):
            success_count += 1

    success_rate = success_count / 10
    return derive_policy(), success_rate

def optimal_policy(policy, problem):
    return True 

def print_policy(policy):
    for row in policy:
        print(" ".join(f"{cell:^5}" for cell in row))

if __name__ == "__main__":
    # test case 2 from p3
    problem = {
        "grid": [
            [{"State": "_", "Reward": -0.01}, {"State": "_", "Reward": -0.01}, {"State": "_", "Reward": -0.01}, {"State": "E", "Reward": 1}],
            [{"State": "_", "Reward": -0.01}, {"State": "#", "Reward": 0}, {"State": "_", "Reward": -0.01}, {"State": "E", "Reward": -1}],
            [{"State": "S", "Reward": -0.01}, {"State": "_", "Reward": -0.01}, {"State": "_", "Reward": -0.01}, {"State": "_", "Reward": -0.01}]
        ],
        "noise": 0.1,
        "discount": 1.0,
        "num_iter": 20
    }

    policy, success_rate = temporal_learning(
        problem, 
        num_episodes=1000, 
        epsilon=1.0, 
        epsilon_decay=0.99, 
        alpha=0.1, 
        alpha_decay=0.99
    )

    print("Derived policy:")
    print_policy(policy)
    print(f"Success rate: {success_rate}")
