import array
class State:
    # クラス変数にするとインスタンスが複数定義できないので
    # コンストラクタ変数にしています
    # 外からもアクセスできます(getter,setter作ってもいいけど)
    def __init__(self):
        self.E_position = array.array("i",[])
        self.P_position = array.array("i",[])
