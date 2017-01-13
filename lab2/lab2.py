# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    list_of_path = [(start,)]
    if start == goal:
        return [start]
    while len(list_of_path) > 0:
        path_to_extend = list_of_path[0]
        list_of_path.pop(0)
        node_to_extend = path_to_extend[-1]
        new_nodes = graph.get_connected_nodes(node_to_extend)
        if len(path_to_extend) > 1:
            new_nodes = [node for node in new_nodes
                            if node not in path_to_extend]
        if goal in new_nodes:
            goal_path = path_to_extend + (goal,)
            return list(goal_path)
        new_path = [path_to_extend + (node,) for node in new_nodes]
        list_of_path.extend(new_path)

    return None


## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    list_of_path = [(start,)]
    if start == goal:
        return [start]
    while len(list_of_path) > 0:
        path_to_extend = list_of_path[-1]
        list_of_path.pop(-1)
        node_to_extend = path_to_extend[-1]
        new_nodes = graph.get_connected_nodes(node_to_extend)
        if len(path_to_extend) > 1:
            new_nodes = [node for node in new_nodes
                            if node not in path_to_extend]
        if goal in new_nodes:
            goal_path = path_to_extend + (goal,)
            return list(goal_path)
        new_path = [path_to_extend + (node,) for node in new_nodes]
        list_of_path.extend(new_path)
    return None



## Now we're going to add some heuristics into the search.
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    list_of_path  = [(start,)]
    if start == goal:
        return [start]
    while len(list_of_path) > 0:
        path_to_extend = list_of_path[-1]
        list_of_path.pop(-1)
        node_to_extend = path_to_extend[-1]
        new_nodes = graph.get_connected_nodes(node_to_extend)
        if len(path_to_extend) > 1:
            new_nodes = [node for node in new_nodes
                                if node not in path_to_extend]
        if goal in new_nodes:
            goal_path = path_to_extend + (goal,)
            return list(goal_path)
        heuristics_val = [graph.get_heuristic(node, goal) for node in new_nodes]
        sorted_heuristic_idx_list = sorted(range(len(heuristics_val)),
                                           key=lambda x:heuristics_val[x],
                                           reverse=True)
        sorted_new_nodes = [new_nodes[i] for i in sorted_heuristic_idx_list]
        new_path = [path_to_extend + (_node,) for _node in sorted_new_nodes]
        list_of_path.extend(new_path)
    return None

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    agenda = [(start,)]
    if start == goal:
        return [start]
    while len(agenda) > 0:
        path_to_extend = agenda[0]
        popped = agenda.pop(0)
        node_to_extend = path_to_extend[-1]
        new_nodes = graph.get_connected_nodes(node_to_extend)
        if len(path_to_extend) > 1:
            new_nodes = [node for node in new_nodes
                            if node not in path_to_extend]
        if goal in new_nodes:
            goal_path = path_to_extend + (goal,)
            return list(goal_path)
        heuristics_val = [graph.get_heuristic(node, goal) for node in new_nodes]
        sorted_heuristic_idx_list = sorted(range(len(heuristics_val)),
                                           key=lambda x:heuristics_val[x])
        sorted_new_nodes = [new_nodes[i] for i in sorted_heuristic_idx_list]
        new_path = [path_to_extend + (node,) for node in
                        sorted_new_nodes[:abs(len(agenda) - beam_width)]]
        agenda.extend(new_path)
    return []

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.
## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.

def path_length(graph, node_names):
    if len(node_names) == 0:
        return 0
    total_nodes = len(node_names)
    length = 0
    for i in range(0, total_nodes):
        if i < total_nodes - 1:
            if graph.are_connected(node_names[i], node_names[i+1]):
                length += graph.get_edge(node_names[i], node_names[i+1]).length

    return length


def branch_and_bound(graph, start, goal):
    agenda = [(start, )]
    if start == goal:
        return [start]
    while len(agenda) > 0:
        path_to_extend = agenda[0]
        agenda.pop(0)
        node_to_extend = path_to_extend[-1]
        new_nodes = graph.get_connected_nodes(node_to_extend)
        if len(path_to_extend) > 1:
            new_nodes = [node for node in new_nodes
                            if node not in path_to_extend]
        if goal in new_nodes:
            goal_path = path_to_extend + (goal, )
            return list(goal_path)

        new_paths = [path_to_extend + (node, ) for node in new_nodes]
        path_lengths = [path_length(graph, path) for path in new_paths]

        sorted_path = [path for (path_lengths, path) in sorted(zip(path_lengths, new_paths))]
        agenda.extend(sorted_path)

    return None

def a_star(graph, start, goal):
    agenda = [(start,)]
    if start == goal:
        return [start]
    while len(agenda) > 0:
        path_to_extend = agenda[0]
        agenda.pop(0)
        node_to_extend = path_to_extend[-1]
        new_nodes = graph.get_connected_nodes(node_to_extend)
        if len(path_to_extend) > 1:
            new_nodes = [node for node in new_nodes
                            if node not in path_to_extend]
        if goal in new_nodes:
            goal_path = path_to_extend + (goal,)
            return list(goal_path)

        new_paths = [path_to_extend + (node,) for node in new_nodes]
        new_paths.extend(agenda)
        agenda = new_paths
        for path in agenda:
            if path[-1] in new_nodes:
                if path_length(graph, path_to_extend + (path[-1],)) < path_length(graph, path):
                    agenda.remove(path)

        hScore = []
        for path in agenda:
            _end_node = path[-1]
            hScore.append(graph.get_heuristic(_end_node, goal))

        gScore = [path_length(graph, path) for path in agenda]
        _fScore = [x + y for x,y in zip(hScore, gScore)]
        agenda = [path for (fscore, path) in sorted(zip(_fScore, agenda))]

    return []


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    """
    for all nodes x in Graph, h(x) <= c(n,g)
    """
    for node in graph.nodes:
        hScore = graph.get_heuristic(node, goal)
        goal_path = a_star(graph, node, goal)
        actual_cost = path_length(graph, goal_path)
        if hScore > actual_cost:
            return False
    return True

"""
h(m) - h(n) <= c(m,n)
You can verify consistency by checking each edge and see if difference between h
values on an edge <= the actual edge cost.
"""
def is_consistent(graph, goal):
    for edge in graph.edges:
        hm = graph.get_heuristic(edge.node1, goal)
        hn = graph.get_heuristic(edge.node2, goal)
        if abs(hm - hn) > edge.length:
            return False
    return True

HOW_MANY_HOURS_THIS_PSET_TOOK = '6.5'
WHAT_I_FOUND_INTERESTING = 'a_star'
WHAT_I_FOUND_BORING = 'nothing'
