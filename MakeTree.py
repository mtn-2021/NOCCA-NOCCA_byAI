import array
from State import State
from StateNode import StateNode
#先行後攻で陣地が変わるのであれば修正が必要
#state = State()
#state.P_position.extend([1,2,3,4,5])
#state.E_position.extend([26,27,28,29,30])
#MakeTree.makeTree(state,3)


def makeTree(state : State, depth : int) -> list[StateNode]:
    node = StateNode(state) # 初期状態
    tree = [node] 
    for treeInx,n in enumerate(tree): # treeの中を順に読み込む（親になるnodeを選択）
        if _checkEnd(n.state): # 現在のノード時点でゲームが終わっているならそのノードの子供を作らない
            continue
        elif n.depth >= depth: # 指定した深さを超えていれば終了
            break

        ban = _checkBan(n.state) # 駒が3つ積もっている地点を取得
        turn = (n.depth % 2 == 0) # 現在のノードが誰のターンか取得
        stones = (n.state.E_position if turn else n.state.P_position) # 現在ノードのターンプレイヤーの駒一覧を取得
        # print("aaa",stones)
        
        for posInx,position in enumerate(stones): # ターンプレイヤーの駒一つ一つに処理を行う
            move = _checkCanMove(position,ban,turn) # 参照している駒の動ける方向を取得
            for m in move:
                tree.append(_getNextNode(n,m,treeInx,posInx,turn)) # 各方向に動いた場合のノードを作成、treeに追加
            n.childNum += len(move) # 追加したノードの分だけ現在ノードのchildNumを増やす
    return tree
        

def _checkEnd(state : State) -> bool:
    end = False
    if (([i for i in state.E_position if i%100 > 29]) or # 味方が敵陣に入っていれば or
        ([i for i in state.P_position if i%100 < 0]) or # 敵が自陣に入っていれば or
        (not [i for i in state.P_position if i < 100]) or # 味方が一人も動けなければ or
        (not [i for i in state.E_position if i < 100])): # 敵が一人も動けなければ
        end = True # ゲームは終わっている
    return end

def _getNextNode(n : StateNode, m : int, treeInx : int,posInx : int,turn : bool) -> StateNode:
    pList = [i + 100 if i % 100 == m else i for i in n.state.P_position] # 移動先の座標に既にある駒を沈下
    eList = [i + 100 if i % 100 == m else i for i in n.state.E_position]
    turnList = eList if turn else pList
    tmp = turnList[posInx] # 駒を移動
    turnList[posInx] = m
    pList = [i - 100 if i % 100 == tmp else i for i in pList] # 移動前の座標にある駒を浮上
    eList = [i - 100 if i % 100 == tmp else i for i in eList]    
    
    nextState = State() # 操作後の状態表現
    nextState.P_position = pList
    nextState.E_position = eList
    nextNode = StateNode(nextState) # 操作後のノード
    nextNode.parent = treeInx # 親のtree上のアドレス
    nextNode.depth = n.depth + 1 # 親より一つ深い
    return nextNode

def _checkCanMove(p : int, tripleZone : array.array("i",[]), turn : bool) -> array.array("i",[]):
    xy_p = p % 100
    ban = array.array("i",[])
    if  p // 100 != 0: # 上に駒が乗ってたら動けない
        return ban
    if xy_p % 5 == 0: # 駒が左端にあるなら左方向には動けない
        ban.extend([p-6,p-1,p+4])
    elif xy_p % 5 == 4: # 駒が右端にあるなら右方向には動けない
        ban.extend([p-4,p+1,p+6])
    ((ban.extend([p-6,p-5,p-4]) if xy_p < 5 else None ) # AIの駒で尚且つ上端なら上方向には動けない
     if turn else 
     (ban.extend([p+6,p+5,p+4]) if 30 > xy_p > 24 else None)) # ユーザーの駒で尚且つ下端なら下方向には動けない
    
    
    ban.extend(tripleZone) # 三つ積もっているところには動けない

    canMoveTo = {p-6, p-1, p+4, # 動ける方向
                 p-5,      p+5,
                 p-4, p+1, p+6}

    for i in set(ban): # 動ける方向から動けない方向を除外
        canMoveTo.discard(i)

    return array.array("i",canMoveTo)


def _checkBan(state : State) -> array.array("i",[]):
    banList = [i - 200 for i in 
               (state.E_position + state.P_position) 
                if i > 200] # 全ての駒から深さ200以上の駒の(つまり駒が3つ積もっている)座標を取得
    return banList
