import itertools

BLACK = 0
WHITE = 1
#盤の高さ
HEIGHT=5
#盤の幅
WIDTH=6


class NoccaNocca(object):

    def __init__(self):

        self.init_board()       #盤を表示する
        self.is_continuing=True #ゲームが終了していないか
        self.turn=BLACK         #どっちのターンか
        self.i=None             #x座標の値
        self.j=None             #y座標の値
        self.winner=None
        self.direction=None
        #この場所に駒を置けるかを精査する
        self.set_valid_ij_li()


    #盤を用意して駒を初期に置く
    def init_board(self):
        #サイズ5×6野に次元配列を用意する
        self.board = [[[] for _ in range(WIDTH+1)] for _ in range(HEIGHT)]

        #0列と5列にそれぞれ駒を配置
        for j in range(HEIGHT):
            self.board[j][0].append(BLACK)
            self.board[j][WIDTH-1].append(WHITE)


    #自分の駒がある座標を返す
    def select_ij(self, i: range(HEIGHT), j: range(WIDTH)) -> bool:
        if (i, j) not in self.valid_ij_li:
            return False

        self.i = i
        self.j = j

        self.set_valid_directions()

        return True

    #駒を動かす方向を指定する
    def select_direction(self,direction: str) -> bool:
        #駒を動かす方向が有効ではなかったらFalseを返す
        if direction not in self.valid_directions:
            return False

        #有効だったら代入
        self.direction=direction
        return True

    def move(self) -> str:
        _i, _j = {
            'y': (-1, -1), 'k': (-1,  0), 'u': (-1,  1),
            'h': ( 0, -1),                'l': ( 0,  1),
            'b': ( 1, -1), 'j': ( 1,  0), 'n': ( 1,  1)
        }[self.direction]

        #次に打たれるマス目の座標
        i_=self.i+_i
        j_=self.j+_j

        #勝利しているかを判定する
        if(self.turn==BLACK and j_==WIDTH) or (self.turn==WHITE and j_== -1):
            #ゲーム中断
            self.is_continuing = False
            self.winner = self.turn

            return 'Won'

        self.board[i_][j_].append(self.board[self.i][self.j].pop())
        self.turn=BLACK if self.turn == WHITE else WHITE
        self.set_valid_ij_li()

        #valid_ij_liの大きさがゼロつまり駒が動けないとき
        if len(self.valid_ij_li)==0:
            #ゲーム中止
            self.is_continuing=False
            #勝者ブラック、ホワイトのターンの時は勝者ホワイト
            self.winner=BLACK if self.turn==WHITE else WHITE

        return 'Moved'


    #自分の駒があるところを探索
    def set_valid_ij_li(self):
        self.valid_ij_li = [(i, j) for i, j in itertools.product(range(HEIGHT), range(WIDTH)) if len(self.board[i][j]) > 0 and self.board[i][j][-1] == self.turn]


    #どの方向に動かすことができるか精査する
    def set_valid_directions(self):
        #とりあえず全方向動けると考える
        self.valid_directions='hjklyubn'
        #左端(0列)にいて、BLACKのとき左に行けないようにする
        if self.j==0 and self.turn ==BLACK:
            self.valid_directions=self.valid_directions.replace('y','').replace('h','').replace('b','')

        #右端(5列)にいて、WHITEのとき右にいけないようにする
        elif self.j==WIDTH-1 and self.turn==WHITE:
            self.valid_directions=self.valid_directions.replace('u','').replace('l','').replace('n','')

        #上端（0行）にいるとき上に行けないようにする
        if self.i==0:
            self.valid_directions=self.valid_directions.replace('y','').replace('k','').replace('u','')

        #下端（4列）にいるとき下に行けないようにする
        elif self.i==HEIGHT-1:
            self.valid_directions=self.valid_directions.replace('b','').replace('j','').replace('n','')

        #方向を規定する
        for direction,(_i,_j) in {
            'y': (-1, -1), 'k': (-1,  0), 'u': (-1,  1),
            'h': ( 0, -1),                'l': ( 0,  1),
            'b': ( 1, -1), 'j': ( 1,  0), 'n': ( 1,  1)
        }.items():
            if direction in self.valid_directions and len(self.board[self.i+_i][self.j+_j])==3:
                self.valid_directions=self.valid_directions.replace(direction,'')

    #盤を表示する
    def print_board(self):
        #駒を動かす方向を表示
        print(r'direction:')
        print(r'y   k   u')
        print(r'  \ | /  ')
        print(r'h - * - l')
        print(r'  / | \  ')
        print(r'b   j   n')
        print('-' * 32)

        #BLACKとWHITEのどちらのターンかを表示する
        #例）BLACK's turn.
        print('{turn}\'s turn.'.format(
        turn={
        BLACK: 'BLACK',
        WHITE: 'WHITE'
        }[self.turn]
        ))

        #盤を表示していく
        #ここらへんは盤の上らへんのところを表示する
        print('i\j|', end='')
        print('   '.join(map(str, range(6))))
        print('---+', end='')
        print('-' * 4 * WIDTH)

        #ここらへんは盤そのものを表示していく
        for i in range(HEIGHT):
            print('{i}  |'.format(
            i=i
            ), end='')
            print(' '.join(map(lambda j: ''.join(map(str, self.board[i][j])) + '_' * (3-len(self.board[i][j])), range(WIDTH))))



def main():

    n = NoccaNocca()

    #ゲームが続いているとき
    while n.is_continuing:
        #'='を32個表示
        print('=' * 32)
        n.print_board()
        #動かす駒を表示する
        while True:
            i, j = map(int, input('which stone?    [(i j)∈{status}]: '.format(
                status=', '.join(map(lambda ij: str(ij).replace(',', ' '), n.valid_ij_li))
            )).split(' '))
            if n.select_ij(i, j):
                break

        #動かせる駒を表示する
        while True:
            direction = input('which direction?[{status}]: '.format(
                status = n.valid_directions
            ))
            if n.select_direction(direction):
                break

        #駒を動かす
        n.move()

    #'='を32個表示
    print('='*32)

    #勝者を表示
    print('{winner} won!'.format(
        winner={
            BLACK: 'BLACK',
            WHITE: 'WHITE'
        }[n.winner]
    ))


if __name__ == '__main__':

    main()
