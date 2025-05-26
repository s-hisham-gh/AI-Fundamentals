import sys, grader, parse, collections

def bfs_search(problem):
    startState, goalState, stateSpaceGraph, heuristic = problem
    frontier = collections.deque([[startState]])
    elist = []
    exploredSet = set()

    while frontier:  
        path = frontier.popleft()       
        for i in goalState:            
            if (path[-1] == i):  
                return  ' '.join(elist)+'\n'+' '.join(path)      
        if path[-1] not in exploredSet:   
            elist.append(path[-1]) 
            exploredSet.add(path[-1])          
            if path[-1] in stateSpaceGraph:          
                for child in stateSpaceGraph[path[-1]]:              
                    frontier.append(path+[child[1]])

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)