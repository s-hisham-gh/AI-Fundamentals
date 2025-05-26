import os, sys

def read_layout_problem(file_name):
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, file_name)
    try:
        with open(file_path, 'r') as file:
            seed = file.readline()
            problem = file.read()
    except FileNotFoundError:
        return print('Error: File not found!')
    food_count = problem.count('.')
    board = []
    for line in problem.split('\n'):
        if line:
            if line[-1] == " ":
                line = line[:-1]
            board_line = []
            for char in line:
                if char == ".":
                    board_line.append([char, 1])
                else:
                    board_line.append([char, 0])
            board.append(board_line)
    return seed, food_count, board

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')
