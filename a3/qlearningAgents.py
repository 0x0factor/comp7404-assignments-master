from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        
        # Initialization
        self.QValue = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # check
        if (state, action) not in self.QValue:
          return 0.0
        else:
          # Get QValue
          return self.QValue[(state, action)]

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        
        # Initialization
        optimialAction = ""
        optimialValue = 0.
        optimialActionDict = util.Counter()

        # Get legal action list
        legalActionList = self.getLegalActions(state)
        
        # Check
        if len(legalActionList) == 0: return 0.0
        
        for action in legalActionList:
          
          # Construct optimial action dict
          optimialActionDict[action] = self.getQValue(state, action)
        
        # Returns the key with the highest value (best Value)
        optimialAction = optimialActionDict.argMax()
        optimialValue = optimialActionDict[optimialAction]

        return optimialValue

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        
        # Initialization
        
        optimialAction = ""
        optimialActionDict = util.Counter()

        # Get legal action list
        legalActionList = self.getLegalActions(state)
        
        # Check
        if len(legalActionList) == 0: return 0.0
        
        for action in legalActionList:
          
          # Construct optimial action dict
          optimialActionDict[action] = self.getQValue(state, action)
        
        # Returns the key with the highest value (best Value)
        optimialAction = optimialActionDict.argMax()

        return optimialAction

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        # Initialization
        pickAction = ""

        # Get legal action list
        legalActionList = self.getLegalActions(state)
        
        # Check
        if len(legalActionList) == 0: return None

        pickAction = (random.choice(legalActionList) if util.flipCoin(self.epsilon) else self.computeActionFromQValues(state))
        return pickAction

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        
        # Get prevQVlaue
        prevQVlaue = self.getQValue(state, action)

        # Update QValue
        self.QValue[(state, action)] = (prevQVlaue * (1 - self.alpha)) + self.alpha * (reward + self.getValue(nextState) * self.discount)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # Get feature list
        featureList = self.featExtractor.getFeatures(state, action)
        
        # Get weight
        weights = self.getWeights()
        
        # Calculate QValue
        QValue = sum([(featureList[feature] * weights[feature]) for feature in featureList]) 
        
        return QValue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # Get feature list
        featureList = self.featExtractor.getFeatures(state, action)

        # Get weight
        weights = self.getWeights()
        
        # Calculate difference
        difference = reward + self.computeValueFromQValues(nextState) * self.discount - self.getQValue(state,action)

        # Update weight
        for feature in featureList: weights[feature] += featureList[feature] * self.alpha * difference

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass