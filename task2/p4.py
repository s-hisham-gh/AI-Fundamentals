import sys, parse
import time, os, copy
import random

EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1

def better_play_multiple_ghosts(problem):
    _, food_count, board_layout = problem
    pacman_position, ghost_positions = locate_players(board_layout)
    num_ghosts = len(ghost_positions)
    play_order = ['P', 'W', 'X', 'Y', 'Z'][:1 + num_ghosts]
    move_counter, total_score = 1, 0
    solution_log = f"{total_score}\n"
    solution_log += format_board(board_layout)
    player_position = None
    total_score = 0
    game_active = True
    while game_active:
        for player in play_order:
            if player == "P":
                player_position = pacman_position
            else:
                player_position = ghost_positions[play_order.index(player) - 1]
            if player == "P":
                possible_moves = find_moves(board_layout, player_position, barriers=['%'])
            elif player != 'P':
                possible_moves = find_moves(board_layout, player_position, barriers=['%', 'W', 'X', 'Y', 'Z'])
            else:
                raise ValueError("PacMan is stuck")
            if possible_moves and player != "P":
                move = random.choice(possible_moves)
            elif possible_moves and player == "P":
                move = get_good_move(board_layout, move_counter, player_position, ghost_positions)
            elif player != 'P':
                move = ''
            else:
                raise ValueError("PacMan is stuck")
            solution_log += f"{move_counter}: {player} moving {move}\n"
            food_eaten, new_position = execute_move(board_layout, player, player_position, move)
            if player == "P":
                pacman_position = new_position
            else:
                ghost_positions[play_order.index(player) - 1] = new_position
            food_count -= food_eaten
            if player == "P":
                total_score += (EAT_FOOD_SCORE * food_eaten) + PACMAN_MOVING_SCORE
            solution_log += format_board(board_layout)
            move_counter += 1
            if food_count == 0:
                total_score += PACMAN_WIN_SCORE
                solution_log += f"score: {total_score}\n"
                solution_log += "WIN: Pacman"
                winner = "Pacman"
                game_active = False
                break
            elif pacman_position in ghost_positions:
                total_score += PACMAN_EATEN_SCORE
                solution_log += f"score: {total_score}\n"
                solution_log += "WIN: Ghost"
                winner = "Ghost"
                game_active = False
                break
            solution_log += f"score: {total_score}\n"
    return solution_log, winner

def locate_players(board_layout):
    pacman_loc, ghost_loc = (0, 0), [(-1, -1)]*4
    ghost_map = {'W': 0, 'X': 1, 'Y': 2, 'Z': 3}
    for row_idx, row in enumerate(board_layout):
        for col_idx, cell in enumerate(row):
            if cell[0] == 'P':
                pacman_loc = (row_idx, col_idx)
            if cell[0] in ghost_map.keys():
                ghost_loc[ghost_map[cell[0]]] = (row_idx, col_idx)
    while (-1, -1) in ghost_loc:
        ghost_loc.remove((-1, -1))
    return pacman_loc, ghost_loc

def find_moves(board_layout, player_position, barriers=['%']):
    possible_moves = []
    if player_position[0] > 0 and board_layout[player_position[0]-1][player_position[1]][0] not in barriers:
        possible_moves.append('N')
    if player_position[0] < len(board_layout) - 1 and board_layout[player_position[0]+1][player_position[1]][0] not in barriers:
        possible_moves.append('S')
    if player_position[1] > 0 and board_layout[player_position[0]][player_position[1]-1][0] not in barriers:
        possible_moves.append('W')
    if player_position[1] < len(board_layout[0])-1 and board_layout[player_position[0]][player_position[1]+1][0] not in barriers:
        possible_moves.append('E')
    return possible_moves

def execute_move(board_layout, player, player_position, direction):
    if not direction:
        return 0, player_position
    direction_map = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    new_position, food_collected = (player_position[0]+direction_map[direction][0], player_position[1]+direction_map[direction][1]), 0
    if player == 'P' and (board_layout[new_position[0]][new_position[1]][0] == '.'):
        board_layout[new_position[0]][new_position[1]][1] = 0
        food_collected = 1
    if board_layout[new_position[0]][new_position[1]][0] not in ('W', 'X', 'Y', 'Z'):
        board_layout[new_position[0]][new_position[1]][0] = board_layout[player_position[0]][player_position[1]][0]
    if board_layout[player_position[0]][player_position[1]][1] > 0:
        board_layout[player_position[0]][player_position[1]][0] = '.'
    else:
        board_layout[player_position[0]][player_position[1]][0] = ' '
    return food_collected, (player_position[0] + direction_map[direction][0], player_position[1] + direction_map[direction][1])

def format_board(board_layout):
    board = ''
    for row in board_layout:
        for cell in row:
            board += cell[0]
        board += '\n'
    return board

def bfs(board_layout, start, target, cutoff=12):
    direction_map = {'E': (0, 1), 'N': (-1, 0), 'S': (1, 0), 'W': (0, -1)}
    queue, visited = [(start, 0)], set()
    while queue:
        position, distance = queue.pop(0)
        if position == target:
            return distance
        if distance > cutoff:
            return 1000
        visited.add(position)
        for move in find_moves(board_layout, position):
            new_position = (position[0]+direction_map[move][0], position[1]+direction_map[move][1])
            if new_position not in visited:
                queue.append((new_position, distance+1))
    return 1000

def get_good_move(board_layout, move_counter, pacman_position, ghost_positions):
    direction_map = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    possible_moves = find_moves(board_layout, pacman_position)
    nearest_food = (0, 0)
    min_distance = float('inf')
    for i in range(len(board_layout)):
        for j in range(len(board_layout[i])):
            if board_layout[i][j][0] == '.':
                distance = abs(i-pacman_position[0]) + abs(j-pacman_position[1])
                if distance < min_distance:
                    min_distance = distance
                    nearest_food = (i, j)
    scores = {}
    for move in possible_moves:
        new_pacman_position = (pacman_position[0]+direction_map[move][0], pacman_position[1]+direction_map[move][1])
        food_distance = bfs(board_layout, new_pacman_position, nearest_food)
        ghost_distances = []
        for ghost in ghost_positions:
            ghost_distances.append(bfs(board_layout, new_pacman_position, ghost))
        closest_ghost = ghost_distances.index(min(ghost_distances))
        ghost_dist_score = -500/(2*move_counter + ghost_distances.pop(closest_ghost))
        ghost_dist_score += sum([-2/(1+ghost_dist) for ghost_dist in ghost_distances])
        scores[move] = ghost_dist_score - (food_distance)
    good_moves = [move for move in possible_moves if scores[move] == max(scores.values())]
    return random.choice(good_moves)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 4
    file_name_problem = str(test_case_id) + '.prob'
    file_name_sol = str(test_case_id) + '.sol'
    path = os.path.join('test_cases', 'p' + str(problem_id))
    problem = parse.read_layout_problem(os.path.join(path, file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:', test_case_id)
    print('num_trials:', num_trials)
    print('verbose:', verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_multiple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print('time: ', end - start)
    print('win %', win_p)
