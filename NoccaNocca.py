import itertools
import sys
import msvcrt
BLACK = 0
WHITE = 1
HEIGHT = 6
WIDTH = 5


class NoccaNocca(object):

    def __init__(self):
        self.init_board()
        self.is_continuing = True # 終了条件
        self.turn = BLACK # BLACKが先攻
        self.i = None # 操作する駒の座標
        self.j = None
        self.direction = None # 進もうとしている方向
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
        self.valid_ij_li = [(i, j) for i, j in itertools.product(range(HEIGHT), range(WIDTH)) if len(self.board[i][j]) > 0 and self.board[i][j][-1] == self.turn]

    def set_valid_directions(self):
        # 'hjklyubn' キーボードの並びだと思われる
        self.valid_directions = '01235678'
        if   self.i == 0 and self.turn == BLACK: # 上端(0のみ)
            self.valid_directions = self.valid_directions.replace('0', '').replace('1', '').replace('2', '')
        elif self.i == HEIGHT-1 and self.turn == WHITE: # 下端(1のみ)
            self.valid_directions = self.valid_directions.replace('6', '').replace('7', '').replace('8', '')
        if   self.j == 0: # 左端
            self.valid_directions = self.valid_directions.replace('0', '').replace('3', '').replace('6', '')
        elif self.j == WIDTH-1: # 右端
            self.valid_directions = self.valid_directions.replace('2', '').replace('5', '').replace('8', '')
        for direction, (_i, _j) in {
            '0': (-1, -1), '1': (-1,  0), '2': (-1,  1),
            '3': ( 0, -1),                '5': ( 0,  1),
            '6': ( 1, -1), '7': ( 1,  0), '8': ( 1,  1)
        }.items(): # すでに3つ駒がある方向も除外
            if direction in self.valid_directions and len(self.board[self.i+_i][self.j+_j]) == 3:
                self.valid_directions = self.valid_directions.replace(direction, '')

    def select_ij(self, i: range(HEIGHT), j: range(WIDTH)) -> bool:
        if (i, j) not in self.valid_ij_li:
            return False # if 指定したマスに有効な駒がない
        self.i = i
        self.j = j
        self.set_valid_directions()
        return True

    def select_direction(self, direction: str) -> bool:
        if direction not in self.valid_directions:
            return False
        self.direction = direction
        return True

    def move(self) -> str:
        _i, _j = {
            '0': (-1, -1), '1': (-1,  0), '2': (-1,  1),
            '3': ( 0, -1),                '5': ( 0,  1),
            '6': ( 1, -1), '7': ( 1,  0), '8': ( 1,  1)
        }[self.direction]
        i_ = self.i + _i # 移動先
        j_ = self.j + _j

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


def input_stone(n: NoccaNocca) -> int:
    # 有効駒リスト[(i,j),…]のijの組み合わせごとにデータを(i j)に置き換えて羅列
    status = ', '.join(map(lambda ij: str(ij).replace(',', ''), n.valid_ij_li))
    print(f'which stone?  [(i j)∈ {status}]'.format())
    
    point = 0
    branch = len(n.valid_ij_li) - 1
    space = " " * 7

    while True :
        cursor = " " * 13 + space * point + "*" + space * (branch-point)
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

    return map(int,n.valid_ij_li[point])


def input_direction(n: NoccaNocca) -> str:
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

    return str(direction)


def main():
    n = NoccaNocca()
    while n.is_continuing:
        print('=' * 32)
        n.print_board()

        i, j = input_stone(n)
        n.select_ij(i, j)

        direction = input_direction(n)
        n.select_direction(direction)
        
        print(n.move())

    print('=' * 32)
    winner={BLACK: 'BLACK',WHITE: 'WHITE'}[n.winner]
    print(f'{winner} won!'.format())    

if __name__ == '__main__':
    main()