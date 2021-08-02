import array
import copy
from State import State
from StateNode import StateNode
#先行後攻で陣地が変わるのであれば修正が必要
#state = State()
#state.P_position.extend([1,2,3,4,5])
#state.E_position.extend([26,27,28,29,30])
#MakeTree.makeTree(state,3)


def makeTree(state : State, depth : int) -> list[StateNode]:
    node = StateNode(state)
    tree = [node]
    for treeInx,n in enumerate(tree):
        if _checkEnd(n.state):
            continue
        elif n.depth >= depth:
            #for t in tree:
            #    print(t.depth,t.state.P_position,t.state.E_position)
            #    print("    ",t.childNum,t.parent)
            break

        ban = _checkBan(n.state)
        turn = (n.depth % 2 == 0)
        stones = (n.state.P_position if turn else n.state.E_position)
        
        for posInx,position in enumerate(stones):
            move = _checkCanMove(position,ban,turn)
            #print(move,position)
            for m in move:
                tree.append(_getNextNode(n,m,treeInx,posInx,turn))
            n.childNum += len(move)
    return tree
        

def _checkEnd(state : State) -> bool:
    end = False
    if (([i for i in state.P_position if i%100 > 30]) or 
        ([i for i in state.E_position if i%100 <= 0]) or
        (not [i for i in state.P_position if i < 100]) or
        (not [i for i in state.E_position if i < 100])):
        end = True
    #print(end)
    return end

def _getNextNode(n : StateNode, m : int, treeInx : int,posInx : int,turn : bool) -> StateNode:
    pList = [i + 100 if i % 100 == m else i for i in n.state.P_position]
    eList = [i + 100 if i % 100 == m else i for i in n.state.E_position]
    turnList = pList if turn else eList
    tmp = turnList[posInx]
    turnList[posInx] = m
    pList = [i - 100 if i % 100 == tmp else i for i in pList]
    eList = [i - 100 if i % 100 == tmp else i for i in eList]    
    
    nextState = State()
    nextState.P_position = pList
    nextState.E_position = eList
    nextNode = StateNode(nextState)
    nextNode.parent = treeInx
    nextNode.depth = n.depth + 1
    return nextNode

def _checkCanMove(p : int, tripleZone : array.array("i",[]), turn : bool) -> array.array("i",[]):
    xy_p = p % 100
    ban = array.array("i",[])
    if  p // 100 != 0:
        return ban
    if xy_p % 5 == 0:
        ban.extend([p-4,p+1,p+6])
    elif xy_p % 5 == 1:
        ban.extend([p+4,p-1,p-6])
    ((ban.extend([p-6,p-5,p-4]) if xy_p <= 5 else None )
     if turn else 
     (ban.extend([p+6,p+5,p+4]) if xy_p >=26 else None))
    
    
    ban.extend(tripleZone)

    canMoveTo = {p-6, p-1, p+4,
                 p-5,      p+5,
                 p-4, p+1, p+6}

    for i in set(ban):
        canMoveTo.discard(i)

    return array.array("i",canMoveTo)


def _checkBan(state : State) -> array.array("i",[]):
    banList = [i - 200 for i in 
               (state.E_position + state.P_position) 
                if i > 200]
    #print("ban: ",banList)
    return banList
