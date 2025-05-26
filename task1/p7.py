import sys, parse, grader

def position_cost(nqueens):
    cost = 0
    for i in range(len(nqueens)):
        for j in range(i+1, len(nqueens)):
            if (nqueens[i][0] == nqueens[j][0] or nqueens[i][1] == nqueens[j][1] or  
                abs(nqueens[i][0]-nqueens[j][0]) == abs(nqueens[i][1]-nqueens[j][1])): 
                cost += 1 
    return cost
    
def number_of_attacks(problem):
    board = []
    for i in range(8):
        rows = []
        for j in range(8):
            rows.append(0)
        board.append(rows) 

    for x in range(0, 8, 1):      
        for y in range(0, 8, 1):          
            board[y][x] = position_cost(problem[:x]+[(y, x)]+problem[x+1:])           
    return board
    
def better_board(problem):
    board_attacks = number_of_attacks(problem)
    min_attacks = float('inf')
    best_position = None

    for i in range(8):   
        for j in range(8):
            if board_attacks[j][i] < min_attacks:
                min_attacks = board_attacks[j][i]
                best_position = (j, i)
    if best_position:
        j, i = best_position
        problem = problem[:i]+[(j, i)]+problem[i+1:]
        solution = []
        for row in range(8):
            current_row = []
            for col in range(8):
                if (row, col) in problem:
                    current_row.append('q')
                else:
                    current_row.append('.')
            solution.append(current_row)

        output = ''
        for row in solution:
            output += ' '.join(row)+'\n'
        return output.strip()

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)