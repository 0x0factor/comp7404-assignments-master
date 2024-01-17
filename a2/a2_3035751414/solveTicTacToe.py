#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
from os import get_blocking
import util 
import sys
import random
import time
from optparse import OptionParser

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """

        # Set wining status
        self.winingStatus = ['a', 'bb', 'bc', 'cc']
        
        # Set all possible statuses

        # a status
        status_a_1 = (True, False, False, False, False, False, False, False, True)
        status_a_2 = (False, True, False, True, False, False, False, False, False)
        status_a_3 = (False, True, False, False, False, False, False, True, False)
        status_a_4 = (True, True, False, False, False, False, True, False, False)
        status_a_5 = (True, False, True, False, True, False, False, False, False) 
        status_a_6 = (True, False, True, False, False, False, False, True, False)
        status_a_7 = (True, False, False, False, True, True, False, False, False) 
        status_a_8 = (True, True, False, True, True, False, False, False, False)
        status_a_9 = (True, True, False, True, False, True, False, False, False)
        status_a_10 = (True, True, False, True, False, False, False, False, True)
        status_a_11 = (True, True, False, False, False, False, False, True, True)
        status_a_12 = (True, False, True, False, False, False, True, False, True)
        status_a_13 = (False, True, False, True, False, True, False, True, False)
        status_a_14 = (True, True, False, False, True, True, True, False, False)
        status_a_15 = (True, True, False, False, False, True, True, True, False)
        status_a_16 = (True, True, False, False, False, True, True, False, True)
        status_a_17 = (True, True, False, True, False, True, False, True, True)

        # ab status
        status_ab_1 = (True, True, False, False, True, False, False, False, False)
        status_ab_2 = (True, False, True, False, False, False, True, False, False)
        status_ab_3 = (False, True, False, True, True, False, False, False, False)
        status_ab_4 = (True, True, False, False, False, True, False, True, False)
        status_ab_5 = (True, True, False, False, False, True, False, False, True)

        # ad status
        status_ad_1 = (True, True, False, False, False, False, False, False, False)

        # b status
        status_b_1 = (True, False, True, False, False, False, False, False, False)
        status_b_2 = (True, False, False, False, True, False, False, False, False)
        status_b_3 = (True, False, False, False, False, True, False, False, False)
        status_b_4 = (False, True, False, False, True, False, False, False, False)
        status_b_5 = (True, True, False, True, False, False, False, False, False)
        status_b_6 = (False, True, False, True, False, True, False, False, False)
        status_b_7 = (True, True, False, False, True, True, False, False, False)
        status_b_8 = (True, True, False, False, True, False, True, False, False)
        status_b_9 = (True, True, False, False, False, True, True, False, False)
        status_b_10 = (True, True, False, False, False, False, True, True, False)
        status_b_11 = (True, True, False, False, False, False, True, False, True)
        status_b_12 = (True, False, True, False, True, False, False, True, False)
        status_b_13 = (True, False, False, False, True, True, False, True, False)
        status_b_14 = (True, True, False, True, False, True, False, False, True)
        status_b_15 = (True, True, False, True, False, True, False, True, False)

        # c status
        status_c_1 = (False, False, False, False, False, False, False, False, False)

        # cc status
        status_cc_1 = (False, False, False, False, True, False, False, False, False)

        # d status
        status_d_1 = (True, True, False, False, False, True, False, False, False)
        status_d_2 = (True, True, False, False, False, False, False, True, False)
        status_d_3 = (True, True, False, False, False, False, False, False, True)

        # Other status
        status_other_1 = (True, False, False, False, False, False, False, False, False)
        status_other_2 = (False, True, False, False, False, False, False, False, False)
        status_other_3 = (True, False, False, False, False, True, False, True, False)
        
        # Set statusDict
        self.statusDict = {
            # a status dict
            status_a_1: "a",
            status_a_2: "a",
            status_a_3: "a",
            status_a_4: "a",
            status_a_5: "a",
            status_a_6: "a",
            status_a_7: "a",
            status_a_8: "a",
            status_a_9: "a",
            status_a_10: "a",
            status_a_11: "a",
            status_a_12: "a",
            status_a_13: "a",
            status_a_14: "a",
            status_a_15: "a",
            status_a_16: "a",
            status_a_17: "a",

            # ab status dict
            status_ab_1: "ab",
            status_ab_2: "ab",
            status_ab_3: "ab",
            status_ab_4: "ab",
            status_ab_5: "ab",

            # ad status dict
            status_ad_1: "ad",

            # b status dict
            status_b_1: "b",
            status_b_2: "b",
            status_b_3: "b",
            status_b_4: "b",
            status_b_5: "b",
            status_b_6: "b",
            status_b_7: "b",
            status_b_8: "b",
            status_b_9: "b",
            status_b_10: "b",
            status_b_11: "b",
            status_b_12: "b",
            status_b_13: "b",
            status_b_14: "b",
            status_b_15: "b",

            # c status dict
            status_c_1: "c",

            # cc status dict
            status_cc_1: "cc",

            # d status dict
            status_d_1: "d",
            status_d_2: "d",
            status_d_3: "d",

            # Other status dict
            status_other_1: "",
            status_other_2: "",
            status_other_3: ""
        }

    # An personal implementation of a related paper The Secrets of Notakto: Winning at X-only Tic-Tac-Toe
    # This paper was written by Thane E. Plambeck, Greg Whitehead, https://arxiv.org/pdf/1301.1672.pdf
    # This paper applies a method to solve this problem
    # I have no idea about how to sovle it using other methods
    # If it's not allowed to use paper as a reference, just ignore it
    # Thank you so so much!!!

    def getBoardList(self, board):
        
        # Get reversed board
        boardReversed = [board[i * 3 + j] for j in range(0, 3) for i in range(3)]
        
        # get reflected board
        boardReflect1 = board[::-1]
        boardReflect2 = boardReversed[::-1]

        return [board, boardReflect1, boardReversed, boardReflect2]

    def getPattern(self, board):
        
        boardList = self.getBoardList(board)
        boardDict = self.statusDict

        # Construct new board
        for i in range(0, 4):
            newBoard = [boardList[i][r * 3 + c] for c in range(0, 3, 1) for r in range(2, -1, -1)]
            boardList.append(newBoard)
        
        for board in boardList:
            board = tuple(board)
            if board in boardDict: return boardDict[board]

    def evaluationFunction(self, gameState, gameRules):
        
        winingStatus = self.winingStatus
        status = []
        result = []
        
        for board in gameState.boards:
            newPattern = self.getPattern(board)
            
            # Dead test
            if gameRules.deadTest(board):
                continue
            else:
                status += newPattern
        
        # Sort status
        status = sorted(status)
        
        # Check winingStatus
        result = ''.join(status) in winingStatus

        return result

    def getAction(self, gameState, gameRules):
        
        gameActions = gameState.getLegalActions(gameRules)
        
        for action in gameActions:
            
            # Check winingStatus
            stateAction = gameState.generateSuccessor(action)
            if self.evaluationFunction(stateAction, gameRules): return action
        
        # Choose action randomly and return
        betterAction = random.shuffle(gameState.getLegalActions(gameRules))[0]
        return betterAction

class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """
    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)

class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """
    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):
        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30 

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()