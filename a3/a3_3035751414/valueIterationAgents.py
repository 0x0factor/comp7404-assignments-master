import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        
        # Initialization
        newValueDict = {}
        actionList = []
        
        for i in range(self.iterations):
            
            # Construct new value dict
            newValueDict = self.values.copy()

            for state in self.mdp.getStates():
                
                # Check state
                if self.mdp.isTerminal(state): continue
                
                # Get action lists
                actionList = self.mdp.getPossibleActions(state)
                
                # Get Q Value
                QValues = [self.getQValue(state, action) for action in actionList]
                
                # Get optimial value
                optimialValue = max(QValues)
                newValueDict[state] = optimialValue

            self.values = newValueDict
            
            # Counter
            i += 1

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # Initialization
        QValue = .0

        # Get states And prob
        transStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)

        for newState, prob in transStatesAndProbs:
            
            # Get reward and new value
            reward = self.mdp.getReward(state, action, newState)
            newValue = self.values[newState]
            
            # Calculate Q Value
            QValue += prob * (reward + self.discount * newValue)

        return QValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

        # Initialization
        optimialActionDict = util.Counter()
        optimialAction = ""
        
        # Get action list
        actionList = self.mdp.getPossibleActions(state)
        
        for action in actionList:
            
            # Construct optimial action dict
            optimialActionDict[action] = self.getQValue(state, action)
        
        # Returns the key with the highest value (best Action)
        optimialAction = optimialActionDict.argMax()
        
        return optimialAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
