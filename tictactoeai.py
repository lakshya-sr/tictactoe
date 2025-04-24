import random, math, copy

def print_state(state):
    for y in range(3):
        for x in range(3):
            print(f"{state[0][y*3 + x]} ", end="")
        print()
    print(f"{state[1]}'s turn")
    
def is_terminal(state):
    return len(get_legal_moves(state)) == 0

def get_legal_moves(state):
    if winner(state) != 0: return []
    empty_cells = []
    for i, v in enumerate(state[0]):
        if v == 0:
            empty_cells.append(i)
    return empty_cells

def make_move(state, action):
    if state[0][action] == 0:
        state[0][action] = state[1]
        state[1] = -state[1]
        return state
    else:
        return False
  
def winner(state):
    win_states = [[0, 1, 2],
                  [3, 4, 5],
                  [6, 7, 8],
                  [0, 3, 6],
                  [1, 4, 7],
                  [2, 5, 8],
                  [0, 4, 8],
                  [2, 4, 6]]
    for i in win_states:
        if state[0][i[0]] == state[0][i[1]] == state[0][i[2]] != 0:
            return state[0][i[0]]
    return 0

def clone(state):
    return copy.deepcopy(state)
    
def log(obj):
    f.write(f"{obj}\n")

def start_state():
    state = [[0] * 9, 1]
    return state
    
def generate_example(state):
    history = []
    while not is_terminal(state):
        actions = get_legal_moves(state)
        action = random.choice(actions)
        make_move(state, action)
        history.append(copy.deepcopy(state))
        # print(state, actions)
    # log(f"{winner(history[-1])} {history}")
    return history
    
def average_score(state, iterations):
    wins, losses = 0, 0
    if is_terminal(state): 
        if winner(state) == 0: return 0
        else: return winner(state)*math.inf
        
    for i in range(iterations):
        example = generate_example(clone(state))
        if winner(example[-1]) == state[1]: wins += 1
        elif winner(example[-1]) == -state[1]: losses += 1
    # log(f"{state} {wins} {losses}")
    if losses == 0: return math.inf
    else: return wins/losses
    
def num_wins(state, iterations):
    wins = 0
    if is_terminal(state):
        if winner(state) == state[1]: return 1
        else: return 0
    for i in range(iterations):
        example = generate_example(clone(state))
        if winner(example[-1]) == state[1]: wins += 1
    return wins

def num_losses(state, iterations):
    losses = 0
    if is_terminal(state):
        if winner(state) == -state[1]: return 1
        else: return 0
    for i in range(iterations):
        example = generate_example(clone(state))
        if winner(example[-1]) == -state[1]: losses += 1
    return losses
    
def choose_move(state, iterations):
    average_scores = {}
    if is_terminal(state): return -1
    for action in get_legal_moves(state):
        new_state = make_move(clone(state), action)
        average_scores[action] = average_score(new_state, iterations)
        # log(f"{state} {action} {average_scores[action]}")
    # print(average_scores)
    max_score = max(average_scores.values())
    return random.choice([action for action, score in average_scores.items() if score == max_score])

# f = open("log.txt", "w")
# wins, losses, draws = 0,0,0
# player = -1
# for i in range(10): 
    # state = start_state()
    # while not is_terminal(state):
        # print_state(state)
        # if state[1] == player: action = int(input("Enter move : "))
        # else: action = choose_move(state, 100)
        # make_move(state, action)
        # if winner(state) == player: wins += 1
        # elif winner(state) == -player: losses += 1
        # else: draws += 1
        # if wins > 10: print("win")
        # else: print("loss")
# print(wins, losses, draws)
# f.close()

print(min([(num_losses(make_move(start_state(), a), 1000), a) for a in get_legal_moves(start_state())]))
# for a in get_legal_moves(start_state()):
    # print(a, num_wins(make_move(start_state(), a), 1000))