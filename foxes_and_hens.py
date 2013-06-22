## foxes_and_hens.py

import random
from collections import Counter

def foxes_and_hens(strategy, foxes=22, hens=30):
    """Play the game of foxes and hens."""
    # A state is a tuple of (score-so-far, number-of-hens-in-yard, 
    # deck-of-cards)
    deck = list('F'*foxes + 'H'*hens)
    #random.shuffle(deck)
    state = (score, yard, cards) = (0, 0, ''.join(deck))
    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard

def do(action, state):
    "Apply action to state, returning a new state."
    score, yard, cards = state
    up = cards[0]
    if action == 'gather':
        return (score+yard, 0, cards[1:])
    elif action == 'wait':
        return (score, yard+1, cards[1:]) if (up ==
            'H') else (score, 0, cards[1:])

def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 15:
        return 'wait'
    else:
        return 'gather'

def average_score(strategy, N=100):
    return sum(foxes_and_hens(strategy) for _ in range(N)) / float(N)

def superior(A, B=take5):
    """Does strategy A have a higher average score than B, by more than 1.5
    point?"""
    a, b = average_score(A), average_score(B)
    print a, b
    return a - b > 1.5

def strategy_pr(state):
    score, yard, cards = state
    c = Counter(cards)
    foxes, chickens = c['F'], c['H']

    return random.choice(
        list(['gather']*foxes + ['wait']*chickens))

def strategy_eq(state):
    score, yard, cards = state
    c = Counter(cards)
    foxes, chickens = c['F'], c['H']
    if foxes == 0: return 'wait'
    elif chickens == 0: return 'gather'
    else: return random.choice(['gather', 'wait'])

def strategy_gd(state):
    score, yard, cards = state
    c = Counter(cards)
    foxes, chickens = c['F'], c['H']

    # assume the distribution is geometric
    exp_num_chickens = (len(cards) / foxes
                        ) - 1 if foxes else yard + chickens
    return 'gather' if exp_num_chickens < yard / 2  else 'wait'

def test():
    gather = do('gather', (4, 5, 'F'*4 + 'H'*10))
    assert (gather == (9, 0, 'F'*3 + 'H'*10) or 
            gather == (9, 0, 'F'*4 + 'H'*9))
    
    wait = do('wait', (10, 3, 'FFHH'))
    assert (wait == (10, 4, 'FFH') or
            wait == (10, 0, 'FHH'))
    
    assert superior(strategy_gd)
    return 'tests pass'

if __name__ == "__main__":
    print test()   
