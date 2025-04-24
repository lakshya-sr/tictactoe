import random, math, copy

class Node:
    def __init__(self, data, children=None):
        self.data = data
        if children is None:
            self.children = []
        else:
            self.children = children
    
    def __repr__(self):
        return f"{self.data}"
    
class Tree:
    def __init__(self, root=None):
        self.root = root
    
    def add_node(self, node, parent=None):
        if parent is None:
            if self.root is None:
                self.root = node
            else:
                self.log("Cannot have more than one root")
        else:
            parent.children.append(node)
            node.parent = parent
        if parent == self.root: self.log("root")
        return node
    
    def remove_node(self, node):
        if node is Node:
            if node.parent is None:
                self.root = None
            else:
                node.parent.children.remove(node)
        return node
   
    def log(self, message):
        pass 
        # print(message)

    def depth_first_search(self, node, f):
        if node is None: node = self.root
        stack = [node]
        while len(stack) > 0:
            current = stack.pop()
            f(current)
            for child in current.children:
                stack.append(child)
    
    def breadth_first_search(self, node, f):
        if node is None: node = self.root
        queue = [node]
        while len(queue) > 0:
            current = queue[0]
            queue.remove(current)
            f(current)
            for child in current.children:
                queue.append(child)
    
    def post_order_traversal(self, node, f):
        if node is None: node = self.root
        for child in node.children:
            post_order_traversal(child, f)
            
        f(node)
    
    

class MCTSNode(Node):
    def __init__(self, data, parent=None):
        Node.__init__(self, data)
        self.N = 1
        self.Q = 0
        self.parent = parent
        self.actions = []
    
    def __repr__(self):
        return f"{Node.__str__(self)} \n N = {self.N} \n Q = {self.Q}"

class MCTSTree(Tree): 
    def __init__(self, game, root, score_fn):
        Tree.__init__(self, root)
        self.game = game
        self.root.actions = self.game.get_legal_moves(self.root.data)
        self.score_fn = score_fn

    def iteration(self, node):
        selected_node = self.select(node)
        expanded_node = self.expand(selected_node)
        simulated_node = self.simulate(expanded_node)
        self.backpropagate(simulated_node, node)
        
    def select(self, node):
        if len(node.actions) > 0:
            return node
            
        while len(node.actions) == 0 and not self.game.is_terminal(node.data):
            max_score = max([self.score(child) for child in node.children])
            max_score_nodes = [child for child in node.children if self.score(child) == max_score]
            node = random.choice(max_score_nodes)
            # node = random.choice(node.children)
        return node
            
    def expand(self, node):
        if self.game.is_terminal(node.data) or len(node.actions) == 0:
            return node
        new_node = self.add_node(MCTSNode(self.game.make_move(node.data, node.actions.pop())), node)
        new_node.actions = self.game.get_legal_moves(new_node.data)
        # self.log(new_node)
        return new_node
    
    def simulate(self, node):
        if self.game.is_terminal(node.data): return node
        while not self.game.is_terminal(node.data):
            available_moves = self.game.get_legal_moves(node.data)
            # self.log(f"available_moves : {available_moves}")
            move = random.choice(available_moves)
            # self.log(f"move : {move}")
            new_state = self.game.make_move(node.data, move)
            # self.log(f"new_state : {new_state}")
            node = MCTSNode(new_state, node)
            # self.log(f"node : {node}")
        # self.log(f"final_node : {node}")
        return node
    
    def backpropagate(self, node, root):
        score = self.game.score(node.data)
        while not node == root:
            node = node.parent
            score = -score
            # self.log(node.parent)
            node.Q += score
            node.N += 1
        
    def best_move(self, node, player):
            max_score = max([child.Q for child in node.children])
            max_score_nodes = [child for child in node.children if child.Q == max_score]
            return random.choice(max_score_nodes)
            # min_score = min([child.Q for child in node.children])
            # min_score_nodes = [child for child in node.children if child.Q == min_score]
            # return random.choice(min_score_nodes)
        
    def score(self, node):
        return self.score_fn(node)


class TicTacToeState:
    def __init__(self, board, player):
        self.board = [[j for j in i] for i in board]
        self.player = player
    
    def __str__(self):
        return f"{self.board[0]} \n{self.board[1]} \n{self.board[2]}\n {self.player}"
        # return f"{self.player}"

class TicTacToeAction:
    def __init__(self, move, player):
        self.move = move
        self.player = player
    
    def __repr__(self):
        return f"move : {self.move} player : {self.player}"

class TicTacToe:
    def __init__(self):
        self.player1 = 1
        self.player2 = -1
    
    def is_terminal(self, state):
        return len(self.get_legal_moves(state)) == 0
    
    def wins(self, state, player):
        board = state.board
        win_state = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False
    
    def score(self, state):
        if self.is_terminal(state):
            if self.wins(state, self.player1): return self.player1
            elif self.wins(state, self.player2): return self.player2
            else: return 0
        return 0
        
    def get_legal_moves(self, state):
        if self.wins(state, self.player1) or self.wins(state, self.player2): return []
        empty_cells = []
        for x, row in enumerate(state.board):
            for y, cell in enumerate(row):
                if cell == 0:
                    empty_cells.append([x, y])
        
        return [TicTacToeAction(move, state.player) for move in empty_cells]
    
    def make_move(self, state, action):
        new_state = TicTacToeState(state.board, -state.player)
        new_state.board[action.move[0]][action.move[1]] = state.player
        return new_state
    
    
 
board = [[0,0,0],
         [0,0,0],
         [0,0,0]]
# game = TicTacToe()
# c = 1.1
# mcts = MCTSTree(game, MCTSNode(TicTacToeState(board, 1)), lambda node : (node.Q/node.N)*c*math.sqrt(math.log(node.N)/node.N))
# print(len(mcts.root.actions))

# node = mcts.root
# while not game.is_terminal(node.data):
    # for i in range(1000):
        # mcts.iteration(node)
        # mcts.log(f"iteration : {i}")
    # node = mcts.best_move(node, node.data.player)
    # print(node)
    
# print(len(mcts.root.children))


# print(mcts.root.children)

# print(game.get_legal_moves(TicTacToeState([[0,0,0],
                                           # [0,1,-1],
                                           # [-1,1,1]], -1)))
# t = Tree(Node(1))
# n2 = t.add_node(Node(2), t.root)
# n3 = t.add_node(Node(3), t.root)
# n4 = t.add_node(Node(4), t.root)
# t.add_node(Node(5), n2)
# t.add_node(Node(6), n2)

# import tree_drawing as td
# td.draw_tree(mcts, 500)



# tree = Tree(Node(1))
# tree.add_node(Node(2), tree.root)
# tree.add_node(Node(3), tree.root.children[0])
# print(len(tree.root.children), len(tree.root.children[0].children))


t = Tree(Node(TicTacToeState(board, 1)))
game = TicTacToe()
count = 0

def add_next_states(node):
    global count
    if game.is_terminal(node.data): 
        # print("terminal\n", node.data)
        return
    count += 1
    print(count)
    actions = game.get_legal_moves(node.data)
    for a in actions:
        t.add_node(Node(game.make_move(node.data, a)), node)
    
    
    

add_next_states(t.root)
# add_next_states(t.root.children[0])
# add_next_states(t.root.children[0].children[0])
# add_next_states(t.root.children[0].children[0].children[0])
# add_next_states(t.root.children[0].children[0].children[0].children[0])
# add_next_states(t.root.children[0].children[0].children[0].children[0].children[0])
# add_next_states(t.root.children[0].children[0].children[0].children[0].children[0].children[0])
# add_next_states(t.root.children[0].children[0].children[0].children[0].children[0].children[0].children[0])
# print(len(game.get_legal_moves(t.root.children[0].children[0].children[0].children[0].children[0].children[0].children[0].data)))

for child in t.root.children:
    add_next_states(child)

for child in t.root.children:
    for child1 in child.children:
        add_next_states(child1)

for child in t.root.children:
    for child1 in child.children:
        for child2 in child1.children:
            add_next_states(child2)
                
for child in t.root.children:
    for child1 in child.children:
        for child2 in child1.children:
            for child3 in child2.children: 
                add_next_states(child3)
                
# for child in t.root.children:
    # for child1 in child.children:
        # for child2 in child1.children:
            # for child3 in child2.children:
                # for child4 in child3.children:
                    # add_next_states(child4)
                
# for child in t.root.children:
    # for child1 in child.children:
        # for child2 in child1.children:
            # for child3 in child2.children:
                # for child4 in child3.children:
                    # for child5 in child4.children:
                        # add_next_states(child1)
                
# for child in t.root.children:
    # for child1 in child.children:
        # for child2 in child1.children:
            # for child3 in child2.children:
                # for child4 in child3.children:
                    # for child5 in child4.children:
                        # for child6 in child5.children:
                            # add_next_states(child1)
                
# for child in t.root.children:
    # for child1 in child.children:
        # for child2 in child1.children:
            # for child3 in child2.children:
                # for child4 in child3.children:
                    # for child5 in child4.children:
                        # for child6 in child5.children:
                            # for child7 in child6.children:
                                # add_next_states(child1)
                
             
print(count)
# print(game.get_legal_moves(TicTacToeState([[1,1,1],[1,1,1],[1,1,1]], 1)))
# t.depth_first_search(None, add_next_states)




