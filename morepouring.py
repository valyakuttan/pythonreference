## morepouring.py
##
##

def more_pour_problem(capacities, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number."""
    def is_goal(state):
        return goal in state
    
    def successor_states(state):
        return successors(state, capacities)

    start = start if start else tuple(0 for _ in range(len(capacities)))
    
    return shortest_path_search(start,
                                successor_states,
                                is_goal)

def successors(state, capacities):
    """Return a dictionary of {state:action} pairs describing what can be
    reached from the state and how. state is a tuple (x,y,z,...) describing
    the current water level of glasses and capacities is a tuple represents
    the maximum capacities of glasses.""" 
    
    successor_dict = {}
    for i in range(len(state)):
        X = capacities[i]
        
        #fill i
        s = state[:i]+(X,) +state[i+1:]
        if (s != state) and (s not in successor_dict):
            successor_dict[s] = ('fill', i)

        #empty i
        s = state[:i]+(0,) +state[i+1:]
        if (s != state) and (s not in successor_dict):
            successor_dict[s] = ('empty', i)
            
    for i in range(len(state)):
        for j in range(i+1, len(state)):
            # pour i -> j
            s, a = pour_from_i2j(i, j, state, capacities)
            if (s != state) and (s not in successor_dict):
                successor_dict[s] = a
            
            # pour j -> i
            s, a = pour_from_j2i(i, j, state, capacities)
            if (s != state) and (s not in successor_dict):
                successor_dict[s] = a
    
    return successor_dict

def pour_from_i2j(i, j, state, capacities):
    "Return (state, action) pair corresponding to pouring from i -> j"
    x, y, X, Y = state[i], state[j], capacities[i], capacities[j]
    if x + y <= Y:
        s = (state[:i] + (0,) +
                state[i+1:j] + (x+y,) +
                state[j+1:])
    else:
        s = (state[:i] + (x-(Y-y),) +
                state[i+1:j] + (y+(Y-y),) +
                state[j+1:])

    return s, ('pour', i, j)    


def pour_from_j2i(i, j, state, capacities):
    "Return (state, action) pair corresponding to pouring from j -> i"
    x, y, X, Y = state[i], state[j], capacities[i], capacities[j]
    if x + y <= X:
        s = (state[:i] + (x+y,) +
                state[i+1:j] + (0,) +
                state[j+1:])
    else:
        s = (state[:i] + (x+(X-x),) +
                state[i+1:j] + (y-(X-x),) +
                state[j+1:])

    return s, ('pour', j, i)


def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set()
    frontier = [ [start] ] 
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []
    
def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)] 
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

if __name__ == "__main__":
    print test_more_pour()

