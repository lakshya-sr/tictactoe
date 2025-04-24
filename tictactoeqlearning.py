from tictactoe_gym.envs.tictactoe_env import TicTacToeEnv
import random, pickle

class QTable():
    def __init__(self):
        self.table = {}
    
    def make_hashable(self, key):
        return tuple(key[0].tobytes()), key[1]
        
    def __getitem__(self, key):
        if (self.make_hashable(key)) in self.table.keys():
            return self.table[self.make_hashable(key)]
        else: 
            return 0
    
    
    def __setitem__(self, key, value):
        self.table[self.make_hashable(key)] = value
    
    
class QLearning():
    alpha = 0.3
    gamma = 0.9
    
    def __init__(self, env):
        self.table = QTable()
        self.env = env
    
    def episode(self, player):
        self.env.reset()
        terminal = False
        while not terminal:
            state = self.env.get_observation(player)
            actions = self.env.get_actions()
            max_score = max([self.table[state, action] for action in actions])
            best_action = random.choice([action for action in actions if self.table[state, action] == max_score])
            next_state, winner, terminal, _, info = self.env.step(best_action)
            if terminal:
                self.table[state, best_action] =  self.q_score(self.env.get_result(player), self.table[state, best_action], self.env.get_result(player))
            else:
                self.table[state, best_action] =  self.q_score(self.env.get_result(player), self.table[state, best_action], self.max_return(next_state))
            state = next_state
        
        
        
    
    def q_score(self, reward, Q_current, max_expected_Q):
        return (1 - self.alpha)*Q_current + self.alpha*(reward + self.gamma*max_expected_Q)
    
    def max_return(self, state):
        return max([self.table[state, action] for action in self.env.get_actions()])
    
    def best_move(self, state):
        self.env.reset()
        max_score = max([self.table[state, action] for action in self.env.get_actions()])
        best_action = random.choice([action for action in self.env.get_actions() if self.table[state, action] == max_score])
        return best_action
        
def train():
    env = TicTacToeEnv()
    env.reset()
    initial_state = env.get_observation(1)
    q = QLearning(env)
    for i in range(10000):
        q.episode(1)
    print(q.best_move(initial_state))
    with open("QTable.bin", "wb") as f:
        pickle.dump(q.table, f)

def predict():
    env = TicTacToeEnv()
    q = QLearning(env)
    env.reset()
    initial_state = env.get_observation(1)
    with open("QTable.bin", "rb") as f:
        q.table = pickle.load(f)
    print(q.best_move(initial_state))
     
def test():
    env = TicTacToeEnv()
    env.reset()
    print(env.get_actions())
    print(env.get_observation(1))
    q = QLearning(env)
    env.reset()
    initial_state = env.get_observation(1)
    with open("QTable.bin", "rb") as f:
        q.table = pickle.load(f)
    for action in env.get_actions():
        print(q.table[initial_state, action])
    terminal_state = None
    terminal = False
    while not terminal:
        terminal_state, winner, terminal, _, info = env.step(random.choice(env.get_actions()))
    print(q.q_score(env.get_result(1), q.table[terminal_state, None], env.get_result(1)))

        
    
# train()
# predict()
test()