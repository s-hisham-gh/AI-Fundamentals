import sys, random, grader, parse

EAT_FOOD_SCORE = 10
PACMAN_EATEN_SCORE = -500
PACMAN_WIN_SCORE = 500
PACMAN_MOVING_SCORE = -1

def random_play_single_ghost(problem):
    seed_str, food_count, game_board = problem
    solution_log = initialize_seed(seed_str) 
    pacman_position, ghost_position = locate_players(game_board)
    move_counter, total_score = 1, 0
    solution_log += f"{total_score}\n"
    solution_log += format_board(game_board)   
    player_position = None
    game_active = True
    
    while game_active:
        for player_type in ("P", "W"):
            player_position = pacman_position if player_type == "P" else ghost_position
            available_moves = find_moves(game_board, player_position)
            if not available_moves:
                continue
            chosen_move = random.choice(available_moves)
            solution_log += f"{move_counter}: {player_type} moving {chosen_move}\n"
            
            food_eaten, new_position = execute_move(game_board, player_type, player_position, chosen_move)
            if player_type == "P": 
                pacman_position = new_position
            else: 
                ghost_position = new_position
            food_count -= food_eaten
            
            if player_type == "P":
                total_score += (EAT_FOOD_SCORE * food_eaten) + PACMAN_MOVING_SCORE    
            solution_log += format_board(game_board)
            move_counter += 1

            if food_count == 0:
                total_score += PACMAN_WIN_SCORE
                solution_log += f"score: {total_score}\nWIN: Pacman"
                game_active = False
                break
            elif pacman_position == ghost_position:
                total_score += PACMAN_EATEN_SCORE
                solution_log += f"score: {total_score}\nWIN: Ghost"
                game_active = False
                break     
            solution_log += f"score: {total_score}\n"
    return solution_log

def locate_players(board_layout):
    pacman_loc, ghost_loc = (0, 0), (0, 0)
    for row_idx, row in enumerate(board_layout):
        for col_idx, cell in enumerate(row):
            if cell[0] == 'P':
                pacman_loc = (row_idx, col_idx)
            if cell[0] == 'W':
                ghost_loc = (row_idx, col_idx)   
    return pacman_loc, ghost_loc

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

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)
