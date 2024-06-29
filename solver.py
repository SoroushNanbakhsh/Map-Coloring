import sys
import cv2
import random
from map import Map
import utils
from copy import deepcopy

ESCAPE_KEY_CHARACTER = 27
SLEEP_TIME_IN_MILLISECONDS = 500

GRAPH = {}
COLORED_STATES = {}
N_COLORS = 4
COLORING_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
NONE_COLOR = (0, 0, 0)
BACKTRACK_COUNT = 0

MAP = None
FILTERING_MODE = None
USE_VARIABLE_ORDERING = None
USE_VALUE_ORDERING = None


def colorize_map(manual = False):
    for i in range(len(MAP.nodes)):
        if (COLORED_STATES[i] == None):
            MAP.change_region_color(MAP.nodes[i], NONE_COLOR)
        else:
            MAP.change_region_color(MAP.nodes[i], COLORING_COLORS[COLORED_STATES[i]])
    cv2.imshow('Colorized Map', MAP.image)
    if not manual:
        key = cv2.waitKey(SLEEP_TIME_IN_MILLISECONDS)
    else:
        key = cv2.waitKey()
    if key == ESCAPE_KEY_CHARACTER:
        cv2.destroyAllWindows()
        exit()

'''BACKTRACKING CSP SOLVER'''
def backtrack_solve(domains, ind):
    colorize_map(True)

    
    global BACKTRACK_COUNT
    if utils.is_solved(GRAPH, COLORED_STATES):
        print("solved")
        print(f"backtrack count: {BACKTRACK_COUNT}")
        exit(0)
    elif not utils.is_consistent(GRAPH, COLORED_STATES):
        BACKTRACK_COUNT += 1
        COLORED_STATES[ind] = None
        return
    elif FILTERING_MODE == '-fc':
        if utils.forward_check(GRAPH, COLORED_STATES, domains, ind, COLORED_STATES[ind]):
            BACKTRACK_COUNT += 1
            COLORED_STATES[ind] = None
            return
    elif FILTERING_MODE == '-ac':
        if utils.ac3(GRAPH, COLORED_STATES, domains):
            BACKTRACK_COUNT += 1
            COLORED_STATES[ind] = None
            return
    "*** YOUR CODE HERE ***"
    index = utils.get_next_variable(COLORED_STATES, domains)

    # if FILTERING_MODE == '-n':
    #     pass

    # elif FILTERING_MODE == '-fc':
    #     if utils.forward_check(GRAPH, COLORED_STATES, domains, ind, COLORED_STATES[ind]):
    #         BACKTRACK_COUNT += 1
    #         COLORED_STATES[ind] = None
    #         return
        
    # elif FILTERING_MODE == '-ac':
    #     if utils.ac3(GRAPH, COLORED_STATES, domains):
    #         BACKTRACK_COUNT += 1
    #         COLORED_STATES[ind] = None
    #         return

    for color in domains[index]:
        COLORED_STATES[index] = color
        backtrack_solve(domains, index)

    BACKTRACK_COUNT+=1
    COLORED_STATES[index] = None


'''ITERATIVE IMPROVEMENT SOLVER'''
def iterative_improvement_solve(domains:list[list[int]], max_steps=100):
    """
        you will need to use the global variables GRAPH and COLORED_STATES, refer to preprocess() and try to see what they represent
        don't forget to call colorize_map()
        1. initialize all the variables randomly,
        2. then change the conficting values until solved, use max_steps to avoid infinite loops
    """
    "*** YOUR CODE HERE ***"

    for index in range(len(COLORED_STATES)):
        COLORED_STATES[index] = random.randint(0, 3)
        colorize_map(True)

    steps = 1
    while not utils.is_solved(GRAPH, COLORED_STATES) and steps < max_steps:
        next_node_index = utils.random_choose_conflicted_var(GRAPH, COLORED_STATES)
        print('Choosing node: ', next_node_index, 'as conflicting node', 'with color: ', COLORED_STATES[next_node_index])

        COLORED_STATES[next_node_index] = utils.get_chosen_value(graph=GRAPH, variable_value_pairs=COLORED_STATES, domains=domains, variable=next_node_index)
        colorize_map(True)
        steps += 1

    "*** YOUR CODE ENDS HERE ***" 
    print(COLORED_STATES)
    print("solved")
    colorize_map(True)
            
            
def preprocess():
    MAP.initial_preprocessing()
    for vertex in range(len(MAP.nodes)):
       GRAPH[vertex], COLORED_STATES[vertex] = set(), None
    for v in MAP.nodes:
        for adj in v.adj:
            GRAPH[v.id].add(adj)
            GRAPH[adj].add(v.id)

def assign_boolean_value(argument):
    if argument == "-t":
        return True
    elif argument == "-f":
        return False
    else:
        return None


if __name__ == "__main__":
    try:
        MAP_IMAGE_PATH = sys.argv[1]
        FILTERING_MODE = sys.argv[2]
        is_ii_mode = FILTERING_MODE == "-ii"
        if not is_ii_mode:
            USE_VARIABLE_ORDERING = assign_boolean_value(sys.argv[3])
            USE_VALUE_ORDERING = assign_boolean_value(sys.argv[4])
            if USE_VARIABLE_ORDERING == None or USE_VALUE_ORDERING == None:
                print("invalid ordering flags")
                exit(1)
    except IndexError:
        print("Error: invalid arguments.")
        exit(1)
        
    try:
        MAP = Map(cv2.imread(MAP_IMAGE_PATH, cv2.IMREAD_COLOR))
    except Exception as e:
        print("Could not read the specified image")
        exit(1)
    
    preprocess()
    domains = [list(range(N_COLORS)) for _ in range(len(GRAPH.keys()))]
    if not is_ii_mode:
        print(f"filtering mode: {FILTERING_MODE}, use variable ordering: {USE_VARIABLE_ORDERING}, use value ordering: {USE_VALUE_ORDERING}")
        backtrack_solve(domains, 0)
    else:
        iterative_improvement_solve(domains)
    