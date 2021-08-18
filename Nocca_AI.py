from Operator import Operator 
from State import State
import MakeTree
import evaluateState
import NOCCA_slecteval

class Nocca_AI(object):

    def select_move(self,state: State) -> Operator:
      # print(state.E_position,state.P_position)
      nodeList = MakeTree.makeTree(state,3)
      # print("a",nodeList)
      newState = evaluateState.evaluateState(nodeList)
      # print("b",newState)
      newOp = NOCCA_slecteval.SelectEval(newState)
      return newOp      

    def select_stone(self, board: list[list[list]], stone: list[int]) -> int:
        return stone[0]

    def select_direction(self, direction: list)-> int:
        return 7
