from State import State
from Operator import Operator
from Nocca_AI import Nocca_AI
import stateTransition
import sys
import msvcrt
import random
BLACK = 0
WHITE = 1
HEIGHT = 6
WIDTH = 5


class NoccaNocca(object):

    def __init__(self):
        self.is_continuing = True # 終了条件
        self.turn = BLACK # BLACKが先攻
        self.target = None
        self.direction = None # 進もうとしている方向
        self.state = State()
        self.state.E_position = [0,1,2,3,4]
        self.state.P_position = [25,26,27,28,29]
        self.set_valid_ij_li()

    def set_valid_ij_li(self): # 有効な駒の座標のリスト: if 駒が置いてある & 一番上が自分の駒である
        p = [p for p in self.state.P_position if p < 100 if self.turn == BLACK]
        e = [e for e in self.state.E_position if e < 100 if self.turn == WHITE]
        self.valid_ij_li = p if p else e

    def set_valid_directions(self):
        # 'hjklyubn' キーボードの並びだと思われる
        self.valid_directions = '01235678'
        if   self.target >= 0 and self.target <= 4 and self.turn == WHITE: # 上端(0のみ)
            self.valid_directions = self.valid_directions.replace('0', '').replace('1', '').replace('2', '')
        elif self.target >= 25 and self.target <= 29 and self.turn == BLACK: # 下端(1のみ)
            self.valid_directions = self.valid_directions.replace('6', '').replace('7', '').replace('8', '')
        if   self.target % 5 == 0: # 左端
            self.valid_directions = self.valid_directions.replace('0', '').replace('3', '').replace('6', '')
        elif self.target % 5 == 4: # 右端
            self.valid_directions = self.valid_directions.replace('2', '').replace('5', '').replace('8', '')
        for direction, (_target) in {
            '0': (-6), '1': (-5), '2': (-4),
            '3': (-1),            '5': (1),
            '6': (4),  '7': (5),  '8': (6)
        }.items(): # すでに3つ駒がある方向も除外
            if direction in self.valid_directions and self.target + _target in [p % 100 for p in (self.state.P_position + self.state.E_position) if p >= 200] :
                self.valid_directions = self.valid_directions.replace(direction, '')

    def select_ij(self, target: int) -> bool:
        if (target) not in self.valid_ij_li:
            return False # if 指定したマスに有効な駒がない
        self.target = target
        self.set_valid_directions()
        return True

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


def input_direction(n: NoccaNocca) -> bool:
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
                             ((" " if i != 4 else "○") if direction != i else ("×" if i != 4 else "●"))))
                    
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
        elif key == b'\r' and str(direction) in status + "4": # ENTER
            print("\n\n\n")
            break
        elif key == b'\x03': # ctrl + c
            print("\n\n")
            sys.exit()
    if direction == 4:
        return True
    _j = {
    '0': (-6), '1': (-5), '2': (-4),
    '3': (-1),            '5': (1),
    '6': (4),  '7': (5),  '8': (6)
    }[str(direction)]
    n.direction = _j
    return False

def makeOperator(direction: int, target: int) -> Operator:
  op = Operator()
  op.target = target
  op.derection = direction
  return op

def main():
    n = NoccaNocca()
    auto = imput_mode()
    swich = BLACK
    if auto == 0:
        ai = Nocca_AI()
        swich = random.randint(BLACK,WHITE) 
        n.turn = WHITE if swich else BLACK

    while n.is_continuing:
        print('=' * 25)
        stateTransition.printState(n.state) # 状態表現でのプリント
        op = Operator()
        n.set_valid_ij_li() 
        if swich & (not auto):
            # print("AI:", n.valid_ij_li)
            print("AI's turn")
            op = ai.select_move(n.state)
            swich = False
        else:
            # print("PLAYER:", n.valid_ij_li)
            print("Player's turn")
            selection = True
            while selection:
                input_stone(n)
                selection = input_direction(n)
            op = makeOperator(n.direction, n.target)
            swich = True
        n.state = stateTransition.stateTransition(op, n.state)
        if n.state == None:
          break
        n.turn = WHITE if n.turn == BLACK else BLACK
    n.winner = n.turn
    print('=' * 32)
    winner={BLACK: 'Player',WHITE: 'AI'}[n.winner]
    print(f'{winner} won!'.format())
    sys.stdout.flush()
    key = msvcrt.getch()
    if key == b'\r' or key == b'\x03': pass # ENTER or ctrl + c

if __name__ == '__main__':
    main()