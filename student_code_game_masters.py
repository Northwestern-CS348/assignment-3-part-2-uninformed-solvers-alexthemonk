from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        state = []
        # initialize a list to store all states for easier operation
        # cast back to tuple later
        peg_query = parse_input("fact: (inst ?X Peg)")
        for i in range(len(self.kb.kb_ask(peg_query))):
            index = i + 1
            current_state = []
            disk_query = parse_input("fact: (on ?X peg%d)" % index)
            answer = self.kb.kb_ask(disk_query)
            # list of bindings
            if answer:
                # answer found
                for j in answer:
                    # iterate through list of bindings for value
                    # print(j['?X'][-1])
                    current_state.append(int(j['?X'][-1]))
            state.append(tuple(sorted(current_state)))
        # print("Returning State: ", state)
        return tuple(state)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        (disk, old_peg, new_peg) = movable_statement.terms
        # print(disk, old_peg, new_peg)

        # retract the fact that disk in top of old_peg
        self.kb.kb_retract(parse_input("fact: (top %s %s)" % (disk, old_peg)))

        self.kb.kb_retract(parse_input("fact: (on %s %s)" % (disk, old_peg)))
        # get the second disk under the first disk asking onTopOf
        ask_result = self.kb.kb_ask(parse_input("fact: (onTopOf %s ?X)" % disk))
        if ask_result:
            # should only have one binding
            # remove that fact of this disk being onTopOf the other one
            self.kb.kb_retract(parse_input("fact: (onTopOf %s %s)" % (disk, ask_result[0]['?X'])))
            # add the fact that the second disk is now top of old_peg
            self.kb.kb_assert(parse_input("fact: (top %s %s)" % (ask_result[0]['?X'], old_peg)))
        else:
            # the old peg is now empty
            self.kb.kb_assert(parse_input("fact: (empty %s)" % old_peg))
        # print(second_disk_old_peg)

        # get the top of new_peg by asking top
        ask_result = self.kb.kb_ask(parse_input("fact: (top ?X %s)" % new_peg))
        if ask_result:
            # should only have one binding
            # retract the fact that this disk is top of new_peg
            self.kb.kb_retract(parse_input("fact: (top %s %s)" % (ask_result[0]['?X'], new_peg)))
            # add the fact that the disk is now onTopOf that disk
            self.kb.kb_assert(parse_input("fact: (onTopOf %s %s)" % (disk, ask_result[0]['?X'])))
        else:
            # the new peg was empty, remove the fact stating that peg was empty
            self.kb.kb_retract(parse_input("fact: (empty %s)" % new_peg))
        # add the fact that the disk is now top of new_peg
        self.kb.kb_assert(parse_input("fact: (top %s %s)" % (disk, new_peg)))
        self.kb.kb_assert(parse_input("fact: (on %s %s)" % (disk, new_peg)))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        state = []
        # initialize a list to store all states for easier operation
        # cast back to tuple later
        for i in range(3):
            # index for y
            y = i + 1
            current_state = []
            for j in range(3):
                # index for x
                x = j + 1
                tile_query = parse_input("fact: (pos ?X pos%d pos%d)" % (x, y))
                answer = self.kb.kb_ask(tile_query)
                # list of bindings
                if answer:
                    # answer found
                    # should only have one binding
                    tile_found = answer[0]['?X']
                    if tile_found == 'empty':
                        current_state.append(-1)
                    else:
                        current_state.append(int(tile_found[-1]))
                else:
                    print("I'm pretty sure something was not right")
            state.append(tuple(current_state))
        # print("Returning State: ", state)
        return tuple(state)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        (tile, old_x, old_y, new_x, new_y) = movable_statement.terms

        # remove the fact that the old position had tile
        self.kb.kb_retract(parse_input("fact: (pos %s %s %s)" % (tile, old_x, old_y)))
        # add the fact that the old position is empty
        self.kb.kb_add(parse_input("fact: (pos empty %s %s)" % (old_x, old_y)))
        # remove the fact that the new position was empty
        self.kb.kb_retract(parse_input("fact: (pos empty %s %s)" % (new_x, new_y)))
        # add the fact that the new position has tile
        self.kb.kb_add(parse_input("fact: (pos %s %s %s)" % (tile, new_x, new_y)))


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
