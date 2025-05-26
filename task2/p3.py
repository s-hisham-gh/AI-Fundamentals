import sys, grader, parse, random

EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1

def random_play_multiple_ghosts(problem):
    seed_str, food_count, board_layout = problem
    solution_log = initialize_seed(seed_str)
    pacman_position, ghost_positions = locate_players(board_layout)
    num_ghosts = len(ghost_positions)
    play_order = ['P', 'W', 'X', 'Y', 'Z'][:num_ghosts+1]
    move_counter, score = 1, 0
    solution_log += f"{score}\n"
    solution_log += format_board(board_layout)
    player_position = None
    score = 0
    game_active = True
    while game_active:
        for player in play_order:
            if player == "P":
                player_position = pacman_position
            else:
                player_position = ghost_positions[play_order.index(player)-1]
            if player == "P":
                possible_moves = find_moves(board_layout, player_position, barriers=['%'])
            else:
                possible_moves = find_moves(board_layout, player_position, barriers=['%', 'W', 'X', 'Y', 'Z'])
            if possible_moves:
                move = random.choice(possible_moves)
            else:
                move = ''
            solution_log += f"{move_counter}: {player} moving {move}\n"
            food_eaten, new_position = execute_move(board_layout, player, player_position, move)
            if player == "P":
                pacman_position = new_position
            else:
                ghost_positions[play_order.index(player)-1] = new_position
            food_count -= food_eaten
            if player == "P":
                score += (EAT_FOOD_SCORE*food_eaten)+PACMAN_MOVING_SCORE
            solution_log += format_board(board_layout)
            move_counter += 1
            if food_count == 0:
                score += PACMAN_WIN_SCORE
                solution_log += f"score: {score}\n"
                solution_log += "WIN: Pacman"
                game_active = False
                break
            elif pacman_position in ghost_positions:
                score += PACMAN_EATEN_SCORE
                solution_log += f"score: {score}\n"
                solution_log += "WIN: Ghost"
                game_active = False
                break
            solution_log += f"score: {score}\n"
    return solution_log

def initialize_seed(seedStr:str):
    seedVal = seedStr.split()[1]
    try:
        seed = int(seedVal)
    except ValueError:
        print('Seed is not a number.')
        seed = seedVal
    finally:
        random.seed(seed, version=2)
        return f"seed: {seed}\n"

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

def find_moves(board_layout, player_pos, barriers=['%']):
    possible_moves = []
    if player_pos[1] < len(board_layout[0])-1 and board_layout[player_pos[0]][player_pos[1]+1][0] not in barriers:
        possible_moves.append('E')
    if player_pos[0] > 0 and board_layout[player_pos[0]-1][player_pos[1]][0] not in barriers:
        possible_moves.append('N')
    if player_pos[0] < len(board_layout)-1 and board_layout[player_pos[0]+1][player_pos[1]][0] not in barriers:
        possible_moves.append('S')
    if player_pos[1] > 0 and board_layout[player_pos[0]][player_pos[1]-1][0] not in barriers:
        possible_moves.append('W')
    return possible_moves

def execute_move(board_layout, player, player_loc, direction):
    if not direction:
        return 0, player_loc
    direction_map = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}
    new_location, food_collected = (player_loc[0]+direction_map[direction][0], player_loc[1]+direction_map[direction][1]), 0
    if player == 'P' and (board_layout[new_location[0]][new_location[1]][0] == '.'):
        board_layout[new_location[0]][new_location[1]][1] = 0
        food_collected = 1
    if board_layout[new_location[0]][new_location[1]][0] not in ('W', 'X', 'Y', 'Z'):
        board_layout[new_location[0]][new_location[1]][0] = board_layout[player_loc[0]][player_loc[1]][0]
    if board_layout[player_loc[0]][player_loc[1]][1] > 0:
        board_layout[player_loc[0]][player_loc[1]][0] = '.'
    else:
        board_layout[player_loc[0]][player_loc[1]][0] = ' '
    return food_collected, (player_loc[0]+direction_map[direction][0], player_loc[1]+direction_map[direction][1])

def format_board(board_layout):
    board = ''
    for row in board_layout:
        for cell in row:
            board += cell[0]
        board += '\n'
    return board

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)
