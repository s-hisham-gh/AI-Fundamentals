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
        row = []
        for j in range(8):
            row.append(0)
        board.append(row)

    for column in range(8):  
        for row in range(8): 
            queen = problem[:column]+[(row, column)]+problem[column+1:]
            board[row][column] = position_cost(queen)

    solution = ''
    for row in board:
        f_row = ''
        for val in row:
            f_row += '{:^3}'.format(val)
        solution += f_row.strip()+'\n'
    solution = solution.strip()
    return solution

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)
