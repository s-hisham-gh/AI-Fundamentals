import sys, parse, grader
from heapq import heappush, heappop

def ucs_search(problem):
    startState, goalState, stateSpaceGraph, heuristic = problem
    frontier = []
    heappush(frontier, (0, [startState]))
    elist = []
    exploredSet = set()

    while frontier:   
        path = heappop(frontier)   
        for i in goalState:       
            if (path[1][-1] == i):           
                return  ' '.join(elist)+'\n'+' '.join(path[1])           
        if path[1][-1] not in exploredSet:       
            elist.append(path[1][-1])      
            exploredSet.add(path[1][-1])      
            if path[1][-1] in stateSpaceGraph:         
                for child in stateSpaceGraph[path[1][-1]]:              
                    heappush(frontier, (path[0]+child[0], path[1]+[child[1]]))

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)