# -*- coding: utf-8 -*-

from StateNode import StateNode 
from State import State
from Operator import Operator


def make_dummy () -> list[StateNode] :
    
    list = []
    a = State()
    a.P_position.append(0)
    n = StateNode(a)
    list.append(n)
    
    #eval = [5,3,2,4]
    for j in range(2):
        a= State()
        a.P_position.append(j+1)
        n = StateNode(a)
        n.parent = 0
        n.depth = 1
        list.append(n)

    for k in range(4):
        a= State()
        a.P_position.append(k+3)
        n = StateNode(a)
        n.parent = (k //2) + 1
        n.depth = 2
        n.eval = eval[k]
        list.append(n)

    #for i in list:
        #print(i.state.P_position)
        
    return list
    

def SelectEval(list: list[StateNode]) -> Operator :
    parent = []
    eval = []
    depth = list[-1].depth
    parent.append(list[-1].parent)
    state = State()

    for i in reversed(list):
    
        if parent[0] == i.parent:
            eval.append(i.eval)

        else :
           
            #print(max(eval) if depth % 2 == 0 else min(eval))
            list[parent[0]].eval = max(eval) if depth % 2 == 0 else min(eval)
           
            if parent[0] == 0:
                state =   list[(len(eval)+1) - eval.index(max(eval))].state
                #print(len(eval) - eval.index(max(eval)))
            
            
            ##print(list[parent[0]].eval)
            parent[0] = i.parent
            depth = i.depth
            eval.clear()
            eval.append(i.eval)
    
    #print(state.P_position)
 
    operator = getOperator(list[0].state, state)
    
    # state = State()
    # state.P_position = [1 ,2, 103 , 4, 5]
    # state2 = State()
    # state2.P_position = [1, 3, 203, 4, 5]
    
    # operator = getOperator(state, state2)
    print(operator.target, operator.derection)
    

    return operator




def getOperator(before: State , after: State) -> Operator:
    before2 = [i % 100 for i in before.P_position]
    operator = Operator()

    for i, j in enumerate(before2): #
        after2 = after.P_position[i]%100
        if not j == after2:
            operator.target = j
            operator.derection = after2 - j
           
            break
    
    return operator

    
            





        
            
                

            
            



        

















    





