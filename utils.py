import random
from copy import deepcopy

def is_consistent(graph:dict, variable_value_pairs):
    """
        returns True if the variables that have been assigned a value so far are consistent with the constraints, 
        and False otherwise.
        
        variable_value_pairs can be used to access any value of any variable from the variable as a key
        you can use variable_value_pairs.items() to traverse it as (state, color) pairs
                    variable_value_pairs.keys() to get all the variables,         
                and variable_value_pairs.values() to get all the values
    """
    "*** YOUR CODE HERE ***"
    for node, value in variable_value_pairs.items():
        if value is not None:
            for adj in graph[node]:
                if variable_value_pairs[node] == variable_value_pairs[adj]:
                    return False
            
    return True

    

def is_solved(graph:dict, variable_value_pairs):
    for node in graph.keys():
        for adj in graph[node]:
            if variable_value_pairs[node] == variable_value_pairs[adj] or ( variable_value_pairs[node] == None):
                return False
            
    return True

def get_next_variable(variable_value_pairs:dict, domains):
    """
        returns the index of the next variable from the default order of the unassinged variables
    """
    "*** YOUR CODE HERE ***"

    for i, value in variable_value_pairs.items():
        if value is None:
            return i
    

def get_chosen_variable(graph:dict, variable_value_pairs, domains):
    """
        returns the next variable that is deemed the best choice by the proper heuristic
        use a second heuristic for breaking ties from the first heuristic
    """
    "*** YOUR CODE HERE ***"
    "MRV & degree heuristic"
    
    min = 6
    dict_of_possible_nodes:dict = None

    for i in range(domains):
        if len(domains[i]) <= min and variable_value_pairs[i] == None:
            min = len(domains[i])
            dict_of_possible_nodes[''.join(i)] = domains[i]
    
    if len(dict_of_possible_nodes) == 1:
        return dict_of_possible_nodes[0]
    
    max = 0
    target_node = None
    for index in dict_of_possible_nodes:
        if len(graph[index]) > max:
            max = len(graph[index])
            target_node = index

    return target_node
    
def get_ordered_domain(graph, domains, variable):
    """
        returns the domain of the varibale after ordering its values by the proper heuristic
        (you may use imports here)
    """
    "*** YOUR CODE HERE ***"
    domain_order = []
    for color in domains[variable]:
        counter = 0
        for node in graph[variable]:
            if color in domains[node]:
                counter += 1
        domain_order.append((color, counter))
    sorted(domain_order, key=lambda n: n[1])
    return [n[0] for n in domain_order]
    

def forward_check(graph:dict, variable_value_pairs, domains:list[list[int]], variable, value):
    """
        removes the value assigned to the current variable from its neighbors
        returns True if backtracking is necessary, and False otherwise
    """
    "*** YOUR CODE HERE ***"

    print('*** first loop ***')
    for neighbor in graph[variable]:
        print('neighbor: ', neighbor, 'in graph[', variable, ']')
        print('variable-value-pairs of neighbor: ', neighbor, 'is: ', variable_value_pairs[neighbor], 'and value is: ', value, 'copy of domain[neighbor] is: ',domains[neighbor])
        if variable_value_pairs[neighbor] == None and value in domains[neighbor]:
            domains[neighbor].remove(value)
            print('from domain of neighbor ', neighbor, 'value :', value, 'removed')

    print('*** second loop ***')
    for domain in domains:
        print('domain in domains: ', domain)
        if len(domain) == 0:
            print('domain: ', domain, 'removed because has 0 length')
            
            for neighbor in graph[variable]:
                domains[neighbor].append(value)
            return True
        
    return False
    
def ac3(graph:dict, variable_value_pairs, domains:list[list[int]]):
    """
        maintains arc-consistency
        returns True if backtracking is necessary, and False otherwise
    """
    "*** YOUR CODE HERE ***"
    queue = []
    for node in graph:
        for neighbor in graph[node]:
            queue.append([node, neighbor])

    copy_of_domains = deepcopy(domains)
    while len(queue) != 0:
        arc = queue.pop(0)

        print('first arc is: ', arc)
        removed = False
        if variable_value_pairs[arc[0]] != None and variable_value_pairs[arc[1]] == variable_value_pairs[arc[0]]:
            return True            

        
        print('domain of tail: ', domains[arc[0]], 'domain of head: ', domains[arc[1]])
        for color in copy_of_domains[arc[0]]:
            if color in copy_of_domains[arc[1]] and len(copy_of_domains[arc[1]]) == 1:
                copy_of_domains[arc[0]].remove(color)
                removed = True
                print('from domain of tail color: ', color, 'removed')
        
        if removed:
            for node in graph[arc[0]]:
                queue.append([arc[0], node])

        print('now checking in reverse | domain of head: ', domains[arc[1]], 'domain of tail: ', domains[arc[0]])
        for color in copy_of_domains[arc[1]]:
            if color in copy_of_domains[arc[0]] and len(copy_of_domains[arc[0]]) == 1:
                copy_of_domains[arc[1]].remove(color)
                removed = True
                print('now checking in reverse | from domain of head color: ', color, 'removed')
        
        if removed:
            for node in graph[arc[1]]:
                queue.append([arc[1], node])
    
    for domain in copy_of_domains:
        print('domain: ', domain)
        if len(domain) == 0:
            print('domain with 0 len founded. backtrack is necceseery')
            return True
        
    return False


def random_choose_conflicted_var(graph:dict, variable_value_pairs):
    """
        returns a random variable that is conflicting with a constrtaint
    """
    "*** YOUR CODE HERE ***"
    conflicting_variables = []
    for node in graph.keys():
        for anotherNode in graph[node]:
            if variable_value_pairs[node] == variable_value_pairs[anotherNode]:
                conflicting_variables.append(node)

    return conflicting_variables[random.randint(0, len(conflicting_variables) - 1)]
    
def get_chosen_value(graph:dict, variable_value_pairs:dict, domains, variable):
    """
        returns the value by using the proper heuristic
        NOTE: handle tie-breaking by random
    """
    "*** YOUR CODE HERE ***"
    colors_and_their_number_of_conflicts = [None, None, None, None]
    for color in domains[variable]:
        conflict_counter  = 0
        for neighbor in graph[variable]:
            if variable_value_pairs[variable] == variable_value_pairs[neighbor]:
                conflict_counter += 1
            colors_and_their_number_of_conflicts[color] = conflict_counter
    
    min_conflict = 100
    for color in domains[variable]:
        if colors_and_their_number_of_conflicts[color] < min_conflict:
            min_conflict = colors_and_their_number_of_conflicts[color]

    list_of_colors = []
    for color in domains[variable]:
        if colors_and_their_number_of_conflicts[color] > min_conflict:
            colors_and_their_number_of_conflicts.remove(color)
        else:
            list_of_colors.append(color)

    random_value = list_of_colors[random.randint(0, len(list_of_colors) - 1)]
    print('Giving color: ', random_value, 'to node: ', variable)
    return random_value