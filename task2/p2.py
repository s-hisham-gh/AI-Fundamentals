import sys, parse
import time, os, copy
import random

EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1

def better_play_single_ghosts(problem):
    _, food_count, board = problem
    position_pacman, position_ghost = locate_players(board)
    move_count, score = 1, 0
    solution = f"{score}\n"
    solution += format_board(board)
    player_position = None
    score = 0
    game_active = True
    winner = None
    while game_active:
        for player in ("P", "W"):
            if player == "P": 
                player_position = position_pacman
            else: 
                player_position = position_ghost
            possible_moves = find_moves(board, player_position)
            if not possible_moves: 
                continue
            if player == "P":
                move = good_move(board, player_position, position_ghost, possible_moves)
            else:
                move = random.choice(possible_moves)
            solution += f"{move_count}: {player} moving {move}\n"
            eatCount, newplayer_position = execute_move(board, player, player_position, move)
            food_count -= eatCount
            if player == "P": 
                position_pacman = newplayer_position
            else: 
                position_ghost = newplayer_position
            if player == "P":
                score += (EAT_FOOD_SCORE * eatCount) + PACMAN_MOVING_SCORE
            solution += format_board(board)
            move_count += 1
            if food_count == 0:
                score += PACMAN_WIN_SCORE
                solution += f"score: {score}\n"
                solution += "WIN: Pacman"
                winner = "Pacman"
                game_active = False
                break
            elif position_pacman == position_ghost:
                score += PACMAN_EATEN_SCORE
                solution += f"score: {score}\n"
                solution += "WIN: Ghost"
                winner = "Ghost"
                game_active = False
                break
            solution += f"score: {score}\n"
    return solution, winner

def locate_players(board_layout):
    pacman_loc, ghost_loc = (0, 0), (0, 0)
    for row_idx, row in enumerate(board_layout):
        for col_idx, cell in enumerate(row):
            if cell[0] == 'P':
                pacman_loc = (row_idx, col_idx)
            if cell[0] == 'W':
                ghost_loc = (row_idx, col_idx)
    return pacman_loc, ghost_loc

def find_moves(board_layout, player_pos, barriers=['%']):
    possible_moves = []
    if (player_pos[1] < len(board_layout[0])-1) and (board_layout[player_pos[0]][player_pos[1]+1][0]) not in barriers:
        possible_moves.append('E')
    if (player_pos[0] > 0) and (board_layout[player_pos[0]-1][player_pos[1]][0]) not in barriers:
        possible_moves.append('N')
    if (player_pos[0] < len(board_layout)-1) and (board_layout[player_pos[0]+1][player_pos[1]][0]) not in barriers:
        possible_moves.append('S')
    if (player_pos[1] > 0) and (board_layout[player_pos[0]][player_pos[1]-1][0]) not in barriers:
        possible_moves.append('W')  
    return possible_moves

def execute_move(board_layout, player, player_loc, direction):
    direction_map = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    new_location = (player_loc[0]+direction_map[direction][0], player_loc[1]+direction_map[direction][1])
    food_collected = 0
    
    if player == 'P' and board_layout[new_location[0]][new_location[1]][0] == '.':
        board_layout[new_location[0]][new_location[1]][1] = 0
        food_collected = 1
    if board_layout[new_location[0]][new_location[1]][0] != 'W':
        board_layout[new_location[0]][new_location[1]][0] = board_layout[player_loc[0]][player_loc[1]][0]  
    if board_layout[player_loc[0]][player_loc[1]][1] > 0:
        board_layout[player_loc[0]][player_loc[1]][0] = '.'
    else:
        board_layout[player_loc[0]][player_loc[1]][0] = ' '
    
    return food_collected, new_location

def format_board(board_layout):
    board = ''
    for row in board_layout:
        for cell in row:
            board += cell[0]
        board += '\n'
    return board

def good_move(board, position_pacman, position_ghost, possible_moves):
    dirVecMap = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    nearest_food = (0, 0)
    minimum_distance = float('inf')
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j][0] == '.':
                distance = abs(i - position_pacman[0]) + abs(j - position_pacman[1])
                if distance < minimum_distance:
                    minimum_distance = distance
                    nearest_food = (i, j)
    food_distance = abs(nearest_food[0] - position_pacman[0]) + abs(nearest_food[1] - position_pacman[1])
    Scores = {}
    for move in possible_moves:
        newposition_pacman = (position_pacman[0] + dirVecMap[move][0], position_pacman[1] + dirVecMap[move][1])
        distance = abs(newposition_pacman[0] - position_ghost[0]) + abs(newposition_pacman[1] - position_ghost[1])
        Scores[move] = - 1 / (1 + distance) - 2 * food_distance + random.random() * 0.1
    good_moves = []
    for move in possible_moves:
        if Scores[move] == max(Scores.values()):
            good_moves.append(move)
    return random.choice(good_moves)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 2
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_single_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)
