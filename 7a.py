import numpy as np
import random
import json

def save_json(data):
    with open('data.json', 'w') as f:
        json.dump(data.__dict__, f)

class Menace:
    def __init__(self):
        self.boxes = {}
        self.wins = 0
        self.draws = 0
        self.losses = 0
    
    def save(self):
        save_json(self)

def valid_move(board, mv):
    return mv >= 0 and mv <= 8 and board[mv] == " "

def empty_spaces(state):
    return np.array([i for i in range(len(state)) if state[i] == ' '])

def print_board(b):
    print("\n 0 | 1 | 2     %s | %s | %s\n"
          "---+---+---   ---+---+---\n"
          " 3 | 4 | 5     %s | %s | %s\n"
          "---+---+---   ---+---+---\n"
          " 6 | 7 | 8     %s | %s | %s" % (b[0], b[1], b[2],
                                          b[3], b[4], b[5],
                                          b[6], b[7], b[8]))

def game_status(state):
    s = state.copy()
    for i in range(0, 7, 3):
        if s[i] == s[i+1] == s[i+2]:
            return 10 if s[i] == 'X' else -10 if s[i] == 'O' else -1
    for i in range(3):
        if s[i] == s[i+3] == s[i+6]:
            return 10 if s[i] == 'X' else -10 if s[i] == 'O' else -1
    if s[0] == s[4] == s[8] or s[2] == s[4] == s[6]:
        return 10 if s[4] == 'X' else -10 if s[4] == 'O' else -1
    return 0 if len(empty_spaces(s)) == 0 else -1

def get_move(board, player=None):
    if player:
        b_str = ''.join(board)
        if b_str not in player.boxes:
            beads = [i for i, v in enumerate(board) if v == ' ']
            player.boxes[b_str] = beads * ((len(beads) + 2) // 2)
        bead = random.choice(player.boxes[b_str]) if player.boxes[b_str] else -1
        player.moves.append((b_str, bead))
        return bead
    while True:
        mv = int(input("Enter move: "))
        if valid_move(board, mv):
            return mv
        else:
            print("Invalid move")

def update_menace(player, result):
    for b, bead in player.moves:
        if result == "win":
            player.boxes[b].extend([bead]*3)
            player.wins += 1
        elif result == "lose":
            player.boxes[b].remove(bead)
            player.losses += 1
        elif result == "draw":
            player.boxes[b].append(bead)
            player.draws += 1
    player.save()

def train_menace(p1, p2, rounds=1000):
    for _ in range(rounds):
        p1.moves, p2.moves = [], []
        board = [' '] * 9
        while game_status(board) == -1:
            board[get_move(board, p1)] = 'O'
            if game_status(board) != -1: break
            board[get_move(board, p2)] = 'X'
        res = game_status(board)
        if res == 10:
            update_menace(p1, "win")
        elif res == -10:
            update_menace(p1, "lose")
        else:
            update_menace(p1, "draw")

p1 = Menace()

try:
    with open('data.json') as f:
        saved = json.load(f)
        p1.boxes, p1.wins, p1.losses, p1.draws = saved['boxes'], saved['wins'], saved['losses'], saved['draws']
except:
    p2 = Menace()
    train_menace(p1, p2)
    print("No pre-existing game data.")

board = [' '] * 9
print_board(board)

if input("Go first? (Y/N): ").lower() in ['y', 'yes']:
    print("You are O")
    while game_status(board) == -1:
        board[get_move(board)] = 'O'
        print_board(board)
        if game_status(board) != -1: break
        board[get_move(board, p1)] = 'X'
        print_board(board)
else:
    print("You are X")
    while game_status(board) == -1:
        board[get_move(board, p1)] = 'O'
        print_board(board)
        if game_status(board) != -1: break
        board[get_move(board)] = 'X'
        print_board(board)

res = game_status(board)
if res == 10:
    update_menace(p1, "lose")
elif res == -10:
    update_menace(p1, "win")
else:
    update_menace(p1, "draw")
