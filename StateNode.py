from State import State


class StateNode:

    def __init__(self,state : State):
        self.state = state
        self.eval = None
        self.parent = None # StateNode() 入れ子にできないっぽいのでここはアドレスとします
        self.childNum = 0
        self.depth = 0 # 実装が楽になるので追加しました