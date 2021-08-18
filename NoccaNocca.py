import MakeTree
from State import State
from Operator import Operator
from Nocca_AI import Nocca_AI
import stateTransition
import itertools
import sys
import msvcrt
import random
import NOCCA_slecteval
BLACK = 0
WHITE = 1
HEIGHT = 6
WIDTH = 5


class NoccaNocca(object):

    def __init__(self):
        self.init_board()
        self.is_continuing = True # 終了条件
        self.turn = BLACK # BLACKが先攻
        self.target = None
        self.direction = None # 進もうとしている方向
        self.state = State()
        self.state.E_position = [0,1,2,3,4]
        self.state.P_position = [25,26,27,28,29]
        self.set_valid_ij_li()


    def init_board(self):
        self.board = [[[] for _ in range(WIDTH)] for _ in range(HEIGHT)]
        for j in range(WIDTH):
            self.board[0][j].append(BLACK)
            self.board[HEIGHT-1][j].append(WHITE)

    def print_board(self):
        # self.turn が BLACK(=0) なら turn は 'BLACK'
        turn={BLACK: 'BLACK',WHITE: 'WHITE'}[self.turn]
        print(f'{turn}\'s turn.'.format())
        print('i\j|', end='')
        print('   '.join(map(str, range(WIDTH))))
        print('---+', end='')
        print('-' * WIDTH * 4)

        for i in range(HEIGHT):
            print('{i}  |'.format(
                i=i
            ), end='')
            # ' '毎にマスの駒要素(0|1)＋空要素(_)をプリント(計3要素) これをWIDTH列(j)分
            print(' '.join(map(lambda j: ''.join(map(str, self.board[i][j])) + '_' * (3-len(self.board[i][j])), range(WIDTH))))

    def set_valid_ij_li(self): # 有効な駒の座標のリスト: if 駒が置いてある & 一番上が自分の駒である
        # print([p for p in self.state.P_position if p < 100])
        # print(p for p in self.state.P_position if p < 100) if self.turn == WHITE else (e for e in self.state.E_position if e < 100)
        p = [p for p in self.state.P_position if p < 100 if self.turn == BLACK]
        e = [e for e in self.state.E_position if e < 100 if self.turn == WHITE]
        print(self.turn)
        self.valid_ij_li = p if p else e
        # [(i, j) for i, j in itertools.product(range(HEIGHT), range(WIDTH)) if len(self.board[i][j]) > 0 and self.board[i][j][-1] == self.turn]

    def set_valid_directions(self):
        # 'hjklyubn' キーボードの並びだと思われる
        self.valid_directions = '01235678'
        if   self.target >= 0 and self.target <= 4 and self.turn == BLACK: # 上端(0のみ)
            self.valid_directions = self.valid_directions.replace('0', '').replace('1', '').replace('2', '')
        elif self.target >= 25 and self.target <= 29 and self.turn == WHITE: # 下端(1のみ)
            self.valid_directions = self.valid_directions.replace('6', '').replace('7', '').replace('8', '')
        if   self.target % 5 == 0: # 左端
            self.valid_directions = self.valid_directions.replace('0', '').replace('3', '').replace('6', '')
        elif self.target % 5 == 4: # 右端
            self.valid_directions = self.valid_directions.replace('2', '').replace('5', '').replace('8', '')
        for direction, (_target) in {
            '0': (-6), '1': (-5), '2': (-4),
            '3': (-1),                '5': (1),
            '6': (4), '7': (5), '8': (6)
        }.items(): # すでに3つ駒がある方向も除外
            if direction in self.valid_directions and self.target + _target in [p % 100 for p in (self.state.P_position + self.state.E_position) if p >= 200] :
                self.valid_directions = self.valid_directions.replace(direction, '')

    def select_ij(self, target: int) -> bool:
        if (target) not in self.valid_ij_li:
            return False # if 指定したマスに有効な駒がない
        self.target = target
        self.set_valid_directions()
        return True

    def select_direction(self, direction: int) -> bool:
        if direction not in self.valid_directions:
            return False
        self.direction = direction
        return True

    def move(self) -> str:
        _i, _j = {
            '0': (-6), '1': (-5), '2': (-4),
            '3': (-1),                '5': (1),
            '6': (4), '7': (5), '8': (6)
        }[self.direction]
        i_ = self.target + _i # 移動先
        j_ = self.target + _j

        if (self.turn == BLACK and i_ > HEIGHT) or (self.turn == WHITE and i_ < 0):
            self.is_continuing = False
            self.winner = self.turn
            turn = {BLACK: 'BLACK',WHITE: 'WHITE'}[self.winner]
            return f'{turn} reached the goal!!'.format()
        # pop: 最後尾を取得(元の配列からは消える)
        self.board[i_][j_].append(self.board[self.i][self.j].pop())
        # ターン交代
        self.turn = BLACK if self.turn == WHITE else WHITE
        self.set_valid_ij_li() 
        # 動かせる駒がなければ直前のターンプレイヤーの勝利
        if len(self.valid_ij_li) == 0: 
            self.is_continuing = False
            self.winner = BLACK if self.turn == WHITE else WHITE
            turn = {BLACK: 'BLACK',WHITE: 'WHITE'}[self.winner]
            return f'{turn} conquered the board!!'.format()
        return f'{self.turn} Moved' 

def imput_mode() -> int:
    modes = ["vs AI","vs Human"]
    status = ', '.join(map(lambda mode: "[" + mode + "]", modes))
    print(f'which mode?  {status}'.format())
    point = 0
    branch = len(modes)-1
    space = [" " * (len(mode)+4) for mode in modes]

    while True :
        cursor = " " * (len(space[point])//2) + "".join(space[:point]) + "*" + "".join(space[point:])
        sys.stdout.write(f"\r← ENTER → :{cursor}".format())
        sys.stdout.flush()
        key = msvcrt.getch()
        if key == b'K' and point > 0 : # 左
            point -= 1
        elif key ==b'M' and point < branch : # 右
            point += 1
        elif key == b'\r': # ENTER
            print()
            break
        elif key == b'\x03': # ctrl + c
            sys.exit()
    
    return point

def input_stone(n: NoccaNocca) -> int:
    # 有効駒リスト[(i,j),…]のijの組み合わせごとにデータを(i j)に置き換えて羅列
    print(n.valid_ij_li)
    status = ', '.join(map(lambda i: str(i), n.valid_ij_li))
    print(f'which stone?  [(i j)∈ {status}]'.format())
    
    point = 0
    branch = len(n.valid_ij_li) - 1
    space = " " * 4

    while True :
        cursor = " " * 12 + space * point + "*" + space * (branch-point)
        sys.stdout.write(f"\r← ENTER → :{cursor}".format())
        sys.stdout.flush()
        key = msvcrt.getch()
        if key == b'K' and point > 0 : # 左
            point -= 1
        elif key ==b'M' and point < branch : # 右
            point += 1
        elif key == b'\r': # ENTER
            print()
            break
        elif key == b'\x03': # ctrl + c
            sys.exit()
    n.select_ij(n.valid_ij_li[point])


def input_direction(n: NoccaNocca):
    status = n.valid_directions
    direction = int(status[0])
    print("which direction?")
    while True :
        d_map = ["     ↑     :",
                 " ← ENTER → :",
                 "     ↓     :"]
        for i in range(9):
            d_map[i // 3] += ("%s   " % (
                             ("□" if direction != i else "■") 
                            if str(i) in status else 
                             ((" " if i != 4 else "○") if direction != i else "×")))
                    
        write_map = "".join(map(lambda row : row + "\n", d_map))
        sys.stdout.write(f"{write_map}\033[3A".format())
        sys.stdout.flush()
        key = msvcrt.getch()
        if key == b'K' and (direction % 3) != 0 : # 左
            direction -= 1
        elif key == b'M' and (direction % 3) != 2 : # 右
            direction += 1
        elif key == b'H' and (direction - 3) >= 0 : # 上
            direction -= 3
        elif key == b'P' and (direction + 3) <= 8 : # 下
            direction += 3
        elif key == b'\r' and str(direction) in status: # ENTER
            print("\n\n\n")
            break
        elif key == b'\x03': # ctrl + c
            print("\n\n")
            sys.exit()
    _j = {
    '0': (-6), '1': (-5), '2': (-4),
    '3': (-1),                '5': (1),
    '6': (4), '7': (5), '8': (6)
    }[str(direction)]
    # print(_j)
    n.direction = _j

def makeOperator(direction: int, target: int) -> Operator:
  op = Operator()
  op.target = target
  op.derection = direction
  return op

def main():
    n = NoccaNocca()
    list = NOCCA_slecteval.make_dummy()
    NOCCA_slecteval.SelectEval(list)
    auto = imput_mode()
    swich = BLACK
    if auto == 0:
        ai = Nocca_AI()
        swich = random.randint(BLACK,WHITE) 
        n.turn = WHITE if swich else BLACK

    while n.is_continuing:
        print('=' * 32)
        stateTransition.printState(n.state) # 状態表現でのプリント
        op = Operator()
        n.set_valid_ij_li() 
        if swich & (not auto):
            print("AI:", n.valid_ij_li)
            op.target = n.valid_ij_li[0]
            op.derection = 6
            # target = ai.select_stone(n.board, n.valid_ij_li)
            # n.select_ij(i, j) ##ここで有効方向を決めているのでこの処理はくくりだせません
            # direction = ai.select_direction(n.valid_directions)
            swich = False
        else:
            print("PLAYER:", n.valid_ij_li)
            input_stone(n)
            # n.select_ij(i, j)
            input_direction(n)
            # print(n.direction)
            # n.select_direction(n.direction)
            op = makeOperator(n.direction, n.target)
            swich = True
        n.turn = WHITE if swich else BLACK
        # print(op.target)
        # print(op.derection)
        n.state = stateTransition.stateTransition(op, n.state)
        # print(n.move())

    print('=' * 32)
    winner={BLACK: 'BLACK',WHITE: 'WHITE'}[n.winner]
    print(f'{winner} won!'.format())    

if __name__ == '__main__':
    main()