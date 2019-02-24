
from solver import *
import queue
from copy import deepcopy

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        # deal with current state
        # generate children for it if necessary
        # select the next state to explore
        self.visited[self.currentState] = True

        if self.currentState.state == self.victoryCondition:
            # damn son
            return True
        moves = self.gm.getMovables()
        if len(moves) == 0 or self.currentState.nextChildToVisit == len(moves):
            # no more children to explore
            # set the next state to be the previous one
            self.currentState = self.currentState.parent
            if self.currentState.requiredMovable:
                # go back to previous state
                self.gm.reverseMove(currentState.requiredMovable)
            return False
        else:
            # there are children unvisited, supposingly
            starting_index = self.currentState.nextChildToVisit
            for child_move in moves[starting_index:]:
                self.gm.makeMove(child_move)
                this_state = GameState(self.gm.getGameState(), self.currentState.depth+1, child_move)
                this_state.parent = self.currentState
                self.currentState.children.append(this_state)
                if this_state in self.visited.keys() and self.visited[this_state]:
                    # already visited
                    self.currentState.nextChildToVisit += 1
                    self.gm.reverseMove(child_move)
                    continue
                else:
                    # do this child
                    self.currentState = this_state
                    self.visited[this_state] = True
                    return False
            # all checked, but no child could be explored
            # reverse
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return False

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.q = queue.Queue()
        self.kb_cache = dict()
        # trying to cache all the mother fucking kb here
        # for fewer operations
        # self.q.put(self.currentState)
        self.kb_cache[self.currentState] = deepcopy(self.gm.kb)


        self.counter = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        # restore the stored state that should be visited

        if self.currentState.state == self.victoryCondition:
            # damn son
            return True
        moves = self.gm.getMovables()
        # for i in moves:
        #     print(i)
        # get all possible child moves
        for child_move in moves:
            # use those moves to generate childrens
            self.gm.makeMove(child_move)
            this_state = GameState(self.gm.getGameState(), self.currentState.depth+1, child_move)
            this_state.parent = self.currentState
            self.currentState.children.append(this_state)
            # add these children to queue and cache
            if this_state in self.visited.keys() and self.visited[this_state]:
                # already visited
                self.gm.reverseMove(child_move)
                continue
            self.q.put(this_state)
            self.visited[this_state] = True
            self.kb_cache[this_state] = deepcopy(self.gm.kb)
            # done storing, reverse
            self.gm.reverseMove(child_move)

        self.currentState = self.q.get()
        self.gm.kb = deepcopy(self.kb_cache[self.currentState])
        return False
