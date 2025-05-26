import sys, parse
import time, os, copy
import random

EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1

def min_max_multiple_ghosts(problem, k):
    _, food_count, board_layout = problem
    pacman_position, ghost_positions = locate_players(board_layout)
    num_ghosts = len(ghost_positions)
    play_order = ['P', 'W', 'X', 'Y', 'Z'][:1 + num_ghosts]
    move_counter, total_score = 1, 0
    solution_log = f"{total_score}\n"
    solution_log += format_board(board_layout)
    game_active = True
    while game_active:
        for player in play_order:
            player_position = pacman_position if player == "P" else ghost_positions[play_order.index(player) - 1]
            possible_moves = (
                find_moves(board_layout, player_position, barriers=['%']) 
                if player == "P" else 
                find_moves(board_layout, player_position, barriers=['%', 'W', 'X', 'Y', 'Z'])
            )
            move = ""
            if possible_moves:
                move = (
                    get_minimax_move(board_layout, move_counter, food_count, player_position, ghost_positions, k, True)
                    if player == "P" else
                    get_minimax_move(board_layout, move_counter, food_count, player_position, ghost_positions, k, False)
                )
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
                solution_log += f"score: {total_score}\nWIN: Pacman"
                game_active = False
                winner = "Pacman"
                break
            elif pacman_position in ghost_positions:
                total_score += PACMAN_EATEN_SCORE
                solution_log += f"score: {total_score}\nWIN: Ghost"
                game_active = False
                winner = "Ghost"
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
    if player_position[1] < len(board_layout[0])-1 and board_layout[player_position[0]][player_position[1]+1][0] not in barriers:
        possible_moves.append('E')
    if player_position[0] > 0 and board_layout[player_position[0]-1][player_position[1]][0] not in barriers:
        possible_moves.append('N')
    if player_position[0] < len(board_layout)-1 and board_layout[player_position[0]+1][player_position[1]][0] not in barriers:
        possible_moves.append('S')
    if player_position[1] > 0 and board_layout[player_position[0]][player_position[1]-1][0] not in barriers:
        possible_moves.append('W')
    return possible_moves

def execute_move(board_layout, player, player_position, direction):
    if not direction:
        return 0, player_position
    direction_map = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    new_position, food_collected = (player_position[0] + direction_map[direction][0], player_position[1] + direction_map[direction][1]), 0
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
    direction_map = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    queue, visited = [(start, 0)], set()
    while queue:
        position, distance = queue.pop(0)
        if position == target:
            return distance
        if distance > cutoff:
            return 1000
        visited.add(position)
        for move in find_moves(board_layout, position):
            new_position = (position[0] + direction_map[move][0], position[1]+direction_map[move][1])
            if new_position not in visited:
                queue.append((new_position, distance+1))
    return 1000

def test_terminated(food_count, pacman_position, ghost_position):
    if food_count == 0:
        return True, 'Pacman'
    if pacman_position in ghost_position:
        return True, 'Ghost'
    return False, None

def evaluation_function(board_layout, move_counter, food_count, pacman_position, ghost_position):
    nearest_food = (-1, -1)
    min_distance, sec_distance = float('inf'), float('inf')
    for i in range(len(board_layout)):
        for j in range(len(board_layout[i])):
            if board_layout[i][j][0] == '.':
                distance = abs(i-pacman_position[0]) + abs(j-pacman_position[1])
                if distance < min_distance:
                    sec_distance = min_distance
                    min_distance = distance
                    nearest_food = (i, j)
    min_food_distance = abs(nearest_food[0]-pacman_position[0])+abs(nearest_food[1]-pacman_position[1])
    ghost_distances = []
    for ghost in ghost_position:
        ghost_distances.append(bfs(board_layout, pacman_position, ghost, cutoff=5))
    closest_ghost = ghost_distances.index(min(ghost_distances))
    ghost_dist_score = -1/(2*move_counter + ghost_distances.pop(closest_ghost))
    ghost_dist_score += sum([-1/(move_counter+ghost_dist) for ghost_dist in ghost_distances])
    return -(0.1) ** move_counter * ghost_dist_score - 1/(min_food_distance) - 1/(1 + sec_distance)+(move_counter % 50) *random.random()

def utility(board_layout, move_counter, food_count, terminated, winner, pacman_position, ghost_position):
    if terminated and winner == 'Pacman':
        return PACMAN_WIN_SCORE
    elif terminated and winner == 'Ghost':
        return PACMAN_EATEN_SCORE
    else:
        return evaluation_function(board_layout, move_counter, food_count, pacman_position, ghost_position)

def minimax(board_layout, move_counter, food_count, pacman_position, ghost_position, num_ghost=-1, depth=5, is_maximizing=True):
    terminated, winner = test_terminated(food_count, pacman_position, ghost_position)
    if depth == 0 or terminated:
        return utility(board_layout, move_counter, food_count, terminated, winner, pacman_position, ghost_position)
    if is_maximizing:
        max_util = float('-inf')
        for move in find_moves(board_layout, pacman_position):
            util = minimax(board_layout, move_counter, food_count, pacman_position, ghost_position, depth=depth-1, is_maximizing=False)
            max_util = max(max_util, util)
        return max_util
    else:
        min_util = float('inf')
        for move in find_moves(board_layout, ghost_position[num_ghost], barriers=['%', 'W', 'X', 'Y', 'Z']):
            util = minimax(board_layout, move_counter, food_count, pacman_position, ghost_position, num_ghost, depth - 1, True)
            min_util = min(min_util, util)
        return min_util

def get_minimax_move(board_layout, move_counter, food_count, player_position, ghost_position, depth, is_maximizing):
    best_move = ''
    best_util = float('-inf') if is_maximizing else float('inf')
    for move in find_moves(board_layout, player_position):
        util = minimax(board_layout, move_counter, food_count, player_position, ghost_position, depth=depth, is_maximizing=is_maximizing)
        if is_maximizing and util > best_util:
            best_util = util
            best_move = move
        elif not is_maximizing and util < best_util:
            best_util = util
            best_move = move
    return best_move

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 5
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = min_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)
