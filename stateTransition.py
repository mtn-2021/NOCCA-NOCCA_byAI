from array import array
from StateNode import StateNode
from State import State
from Operator import Operator
BLACK = 0
WHITE = 1
HEIGHT = 6
WIDTH = 5

def stateToBoard(state: State) -> list:
  board = [[] for _ in range(WIDTH*HEIGHT)]
  ead = [e for e in state.E_position if e >= 100]
  pad = [p for p in state.P_position if p >= 100]
  ea = [e for e in state.E_position if (e < 100 and (e in list(map(lambda x: x%100, pad))))]
  pa = [p for p in state.P_position if (p < 100 and (p in list(map(lambda x: x%100, ead))))]
  for e in state.E_position:
    if not e%100 in (ea + pa): board[e % 100].append(BLACK)
  for p in state.P_position:
    if not p%100 in (pa + ea): board[p % 100].append(WHITE)
  # print(board)
  # print("BLACK:0")
  # print("E_POS", state.E_position)
  # print("E_BeCovered", ead)
  # print("E_Cover", ea)
  # print("WHITE:1")
  # print("P_POS", state.P_position)
  # print("P_BeCovered", pad)
  # print("P_Cover", pa)
  for e in ead:
    index = e % 100
    depth = e // 100
    tmp = [p for p in pad if p % 100 == index]
    tmpdepth = -1
    maxdepth = -1
    if tmp:
      tmpdepth = tmp.pop() // 100
    maxdepth = max(depth, tmpdepth)
    while len(board[index])-1 < maxdepth: board[index].append(-1)
    board[index][len(board[index])-depth-1] = BLACK
  for p in pad:
    index = p % 100
    depth = p // 100
    tmp = [e for e in ead if e % 100 == index]
    tmpdepth = -1
    maxdepth = -1
    if tmp:
      tmpdepth = tmp.pop() // 100
    maxdepth = max(depth, tmpdepth)
    while len(board[index])-1 < maxdepth: board[index].append(-1)
    board[index][len(board[index])-depth-1] = WHITE
  for e in ea:
    index = e
    top = len(board[index]) - 1
    board[index][top] = BLACK
  for p in pa:
    index = p
    top = len(board[index]) - 1 
    board[index][top] = WHITE
  return board

def boardToState(board: list) -> State:
  state = State()
  e = []
  p = []
  for index, ep in enumerate(board):
    if ep:
      depth = len(ep)
      for dep in range(depth):
        if ep[dep] == BLACK:
          e.append((depth-dep-1)*100 + index)
        elif ep[dep] == WHITE:
          p.append((depth-dep-1)*100 + index)
  state.E_position = e
  state.P_position = p
  # print(state.E_position, state.P_position)
  # state.E_position = [15,120,102,3,4]
  # state.P_position = [20,2,27,28,29]
  return state

def printState(state: State):
  board = stateToBoard(state)
      
  print('i\j|', end='')
  print('   '.join(map(str, range(WIDTH))))
  print('---+', end='')
  print('-' * WIDTH * 4)
  for i in range(HEIGHT):
    print('{i}  |'.format(
    i=i
    ), end='')
    print(' '.join(map(lambda j: ''.join(map(str, board[i*5+j])) + '_' * (3-len(board[i*5+j])), range(WIDTH))))
  print('=' * WIDTH * 5)
  print('NEXT')
  print('=' * WIDTH * 5)

def stateTransition(operator: Operator, state: State) -> State:
  if operator.target >= 100:
    print("error")
    return
  # print("OPERATOR", operator.target, operator.derection)
  board = stateToBoard(state)
  # print("BEFORE", board)
  # print("OPTARG", operator.target)
  # print("OPDIREC", operator.derection)
  target = board[operator.target].pop()
  # print("TARG", target)
  nextTarget = operator.target + operator.derection
  if nextTarget < 0 or nextTarget > 29:
    return None
  board[operator.target + operator.derection].append(target)
  # print("AFTER", board)
  fixState = boardToState(board)
  pl = [p for p in fixState.P_position if p < 100]
  el = [e for e in fixState.E_position if e < 100]
  if not pl or not el:
    return None
  return fixState

""""""""""
def main():
  state = State()
  # state.E_position = [0,1,2,3,4]
  # state.P_position = [25,26,27,28,29]
  # printState(state)
  state.E_position = [20,220,102,3,4]
  state.P_position = [120,2,27,28,29]
  printState(state)
  # print("BEFORE STATE", state.E_position, state.P_position)
  op = Operator()
  # op.target = 120
  # op.derection = -5
  # stateTransition(op, state, WHITE)
  op.target = 120
  op.derection = 5
  nextState = stateTransition(op, state)
  # print("AFTER STATE", nextState.E_position, nextState.P_position)
  printState(nextState)

main()
"""""""""