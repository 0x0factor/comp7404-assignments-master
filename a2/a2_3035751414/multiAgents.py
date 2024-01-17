from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # Get foodList
        newFoodList = newFood.asList()
        
        # Get gameScore
        gameScore = successorGameState.getScore()
        
        # Calculate distances to food/ghost
        distanceToFoodList = [manhattanDistance(newPos, food) for food in newFoodList]
        distanceToGhost = manhattanDistance(newPos, newGhostStates[0].getPosition())
        
        # Initiate the score(weight) of food/ghost
        scoreOfFood, scoreOfGhost = 1, 1

        # Calculate the final score and return
        if distanceToFoodList: gameScore += scoreOfFood/((min(distanceToFoodList)) * 1.0)
        if distanceToGhost: gameScore -= scoreOfGhost/(distanceToGhost * 1.0)
        
        return gameScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        
        agentNumber = gameState.getNumAgents()

        # Define a function to get score of a state
        def getGameScore(nowState, depth, agentIndex):

            # Check game status (Win/Lose)
            if nowState.isWin() or nowState.isLose(): return self.evaluationFunction(nowState)
            
            # Get a legal actions list of the state
            actionList = nowState.getLegalActions(agentIndex)
            
            # Initialize a game score list
            gameScoreList = []

            # Main function
            for action in  actionList:
                if (agentIndex == agentNumber - 1):
                    if (depth == 1):
                        gameScore = self.evaluationFunction(nowState.generateSuccessor(agentIndex, action))
                        gameScoreList += [gameScore]
                    else:
                        gameScore = getGameScore(nowState.generateSuccessor(agentIndex, action), depth - 1, 0)
                        gameScoreList += [gameScore]
                else:
                    gameScore = getGameScore(nowState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
                    gameScoreList += [gameScore]

            # Return function result (score)
            return max(gameScoreList) if agentIndex == 0 else min(gameScoreList)
        
        # Initialize a game score list
        gameScoreList = []

        # Get a legal actions list
        actionList = gameState.getLegalActions(0)
        
        for action in actionList: gameScore = getGameScore(gameState.generateSuccessor(0, action), self.depth, 1); gameScoreList += [gameScore]
        
        # Get index and return game score result
        i = 0
        for gameScore in gameScoreList:
            if gameScore == max(gameScoreList): break
            i += 1

        return actionList[i]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        agentNumber = gameState.getNumAgents()

        # Define a function to get score of a state
        def getGameScore(nowState, depth, alpha, beta, agentIndex):

            # Check game status (Win/Lose)
            if nowState.isWin() or nowState.isLose(): return self.evaluationFunction(nowState)
            
            # Get a legal actions list of the state
            actionList = nowState.getLegalActions(agentIndex)
            
            # Initialize a game score list
            gameScoreList = []

            # Main function (Sorry for so many nested if-else statements...I'll try to improve my coding style)
            for action in  actionList:
                if (agentIndex == agentNumber - 1):
                    if (depth == 1):
                        gameScore = self.evaluationFunction(nowState.generateSuccessor(agentIndex, action))
                        gameScoreList += [gameScore]
                        if (agentIndex == 0):
                            alpha = max(gameScore, alpha)
                        else:
                            beta = min(gameScore, beta)
                    else:
                        gameScore = getGameScore(nowState.generateSuccessor(agentIndex, action), depth - 1, alpha, beta, 0)
                        gameScoreList += [gameScore]
                        beta = min(gameScore, beta)
                else:
                    gameScore = getGameScore(nowState.generateSuccessor(agentIndex, action), depth, alpha, beta, agentIndex + 1)
                    gameScoreList += [gameScore]
                    if (agentIndex == 0):
                        alpha = max(gameScore, alpha)
                    else:
                        beta = min(gameScore, beta)
                if (beta < alpha): break

            # Return function result (score)
            return max(gameScoreList) if agentIndex == 0 else min(gameScoreList)
        
        # Initialize a game score list
        gameScoreList = []
        alpha, beta = -float('inf'), float('inf')
        # Get a legal actions list
        actionList = gameState.getLegalActions(0)
        
        for action in actionList:
            gameScore = getGameScore(gameState.generateSuccessor(0, action), self.depth, alpha, beta, 1)
            gameScoreList += [gameScore]
            if (gameScore > alpha): betterScore = action; alpha = gameScore    
            if (beta < alpha): break
        
        # Return game score result
        return betterScore

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        agentNumber = gameState.getNumAgents()

        # Define a function to get score of a state
        def getGameScore(nowState, depth, agentIndex):

            # Check game status (Win/Lose)
            if nowState.isWin() or nowState.isLose(): return self.evaluationFunction(nowState)
            
            # Get a legal actions list of the state
            actionList = nowState.getLegalActions(agentIndex)
            
            # Initialize a game score list
            gameScoreList = []

            # Main function
            for action in  actionList:
                if (agentIndex == agentNumber - 1):
                    if (depth == 1):
                        gameScore = self.evaluationFunction(nowState.generateSuccessor(agentIndex, action))
                        gameScoreList += [gameScore]
                    else:
                        gameScore = getGameScore(nowState.generateSuccessor(agentIndex, action), depth - 1, 0)
                        gameScoreList += [gameScore]
                else:
                    gameScore = getGameScore(nowState.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
                    gameScoreList += [gameScore]

            # Return function result (score)
            return max(gameScoreList) if agentIndex == 0 else (sum(gameScoreList) * 1.0)/len(gameScoreList)
        
        # Initialize a game score list
        gameScoreList = []

        # Get a legal actions list
        actionList = gameState.getLegalActions(0)
        
        for action in actionList: gameScore = getGameScore(gameState.generateSuccessor(0, action), self.depth, 1); gameScoreList += [gameScore]
        
        # Get index and return game score result
        i = 0
        for gameScore in gameScoreList:
            if gameScore == max(gameScoreList): break
            i += 1

        return actionList[i]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: Consider the scaredTimer to get a better one
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    
    # From support files
    # Get newFood
    newFood = currentGameState.getFood()
    # Construct newFoodList
    newFoodList = newFood.asList()
    # Get newPos
    newPos = currentGameState.getPacmanPosition()
    # Get gameScore
    gameScore = currentGameState.getScore()
    # Get newGhostStates
    newGhostStates = currentGameState.getGhostStates()

    # Initiate the score(weight) of food/ghost
    scoreOfFood, scoreOfScaredGhost = 1, 10
    
    # Calculate distances to food/ghost, calculate the final score and return
    distanceToFoodList = [manhattanDistance(newPos, food) for food in newFoodList]
    if distanceToFoodList: gameScore += scoreOfFood/((min(distanceToFoodList)) * 1.0)
    
    for ghost in newGhostStates:
            distanceToGhost = manhattanDistance(newPos, ghost.getPosition())
            if ghost.scaredTimer: gameScore += scoreOfScaredGhost/(distanceToGhost * 1.0)
    
    return gameScore
    
# Abbreviation
better = betterEvaluationFunction