# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodList = newFood.asList()
        food_dist=[]
        for food in newFoodList:
            distance = manhattanDistance(newPos, food)
            food_dist.append(distance)
        if food_dist:    
          min_food_dist=min(food_dist)
        else:
          min_food_dist=-1

        distances_to_ghosts = 1
        danger = 0
        for ghost_state in successorGameState.getGhostPositions():
            distance = manhattanDistance(newPos, ghost_state)
            distances_to_ghosts += distance
            if distance <= 1:
                danger+= 5

        count=1 / float(min_food_dist) - 1 / float(distances_to_ghosts) - danger
        return successorGameState.getScore() + count




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
        """
        "*** YOUR CODE HERE ***"
        def minimax(agent,depth,gameState):
            minimax_list=[]
            if not gameState.getLegalActions(agent) or depth == self.depth: #if game ended
                return self.evaluationFunction(gameState)
            elif agent == 0:  # pacman->max
                for action in gameState.getLegalActions():
                  nextVal=minimax(1,depth,gameState.generateSuccessor(agent,action))
                  minimax_list.append(nextVal)
                return max(minimax_list)
            else:  # ghosts->min
                new_agent=agent+1  
                if gameState.getNumAgents() == new_agent or new_agent==0:
                    new_agent=0
                    depth+=1
                for action in gameState.getLegalActions(agent):
                  nextVal=minimax(new_agent,depth,gameState.generateSuccessor(agent,action))
                  minimax_list.append(nextVal)
                return min(minimax_list)
    #root->max
        maxVal=float("-inf")
        action=Directions.STOP
        for legal_action in gameState.getLegalActions():
            nextVal=minimax(1,0,gameState.generateSuccessor(0,legal_action))
            if nextVal>maxVal:
                maxVal=nextVal
                action=legal_action

        return action




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self,gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def max_Value(game_state,a,b,agent,depth):
            v = float("-inf")
            for newState in game_state.getLegalActions(agent):
                v = max(v,alpha_beta_pruning(game_state.generateSuccessor(agent, newState),a,b,1,depth))
                if v>b:
                    return v
                a=max(a,v)
            return v

        def min_Value(gameState,a,b,agent,depth):  
            v=float("inf")
            new_agent=agent+1  #get the next agent
            if gameState.getNumAgents() == new_agent or new_agent == 0:
                new_agent=0
                depth+=1
            for action in gameState.getLegalActions(agent):
                v=min(v,alpha_beta_pruning(gameState.generateSuccessor(agent, action),a,b,new_agent,depth))
                if v<a:
                    return v
                b=min(b,v)
            return v

        def alpha_beta_pruning(gameState,a,b,agent,depth):
            if not gameState.getLegalActions(agent) or depth == self.depth:  #if game ended
                return self.evaluationFunction(gameState)
            if agent == 0:  #pacman->max
                return max_Value( gameState,a,b,agent,depth)
            else:  # ghosts->min
                return min_Value(gameState,a,b,agent,depth)

        #prune for root
        maxVal=float("-inf")
        action=Directions.STOP
        a=float("-inf")
        b=float("inf")
        for agentState in gameState.getLegalActions(0):
            ghostValue=alpha_beta_pruning(gameState.generateSuccessor(0,agentState),a,b,1,0)
            if ghostValue>maxVal:
                maxVal=ghostValue
                action=agentState
            if maxVal>b:
                return maxVal
            a=max(a,maxVal)

        return action



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
        def expectimax(gameState,agent, depth):
            if not gameState.getLegalActions() or depth == self.depth:  # if game has ended
                return self.evaluationFunction(gameState)
            expec_list=[]
            if agent == 0:  # pacman->max
              for legal_action in gameState.getLegalActions(agent):
                next_expec_val=expectimax(gameState.generateSuccessor(agent, legal_action),1, depth)
                expec_list.append(next_expec_val)
              return max(expec_list)
            else:  # performing expectimax action for ghosts/chance nodes.
                nextAgent=agent+1  # calculate the next agent and increase depth accordingly.
                if gameState.getNumAgents() == nextAgent or nextAgent == 0:
                    nextAgent=0
                    depth+=1
                sum=0
                for legal_action in gameState.getLegalActions(agent):
                  sum+=expectimax(gameState.generateSuccessor(agent, legal_action),nextAgent, depth) 
                return sum/(len(gameState.getLegalActions(agent)))

        #root->max
        maxVal=float("-inf")
        action=Directions.STOP
        for legal_action in gameState.getLegalActions(0):
            nextVal=expectimax(gameState.generateSuccessor(0,legal_action),1,0)
            if nextVal>maxVal :
                maxVal=nextVal
                action=legal_action
        return action
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pac_pos=currentGameState.getPacmanPosition()
    Food=currentGameState.getFood()
    ghost_states=currentGameState.getGhostStates()
    scared_times=[]
    for ghostState in ghost_states:
      scared_times.append(ghostState.scaredTimer)

    ghost_dist_list=[]
    for ghost in ghost_states:
        ghost_dist = util.manhattanDistance(pac_pos, ghost.getPosition())
        ghost_dist_list.append(ghost_dist)
    min_ghost_dist=min(ghost_dist_list)

    min_food_dist = float('Inf')
    food_list=[]
    for food in Food.asList():
        food_dist=util.manhattanDistance(pac_pos, food)
        food_list.append(food_dist)
        if food_list:
          min_food_dist=min(food_list)

    if not scared_times:
        return currentGameState.getScore()+10*min_ghost_dist/min_food_dist
    else:
        return currentGameState.getScore()+min_ghost_dist/min_food_dist+sum(scared_times)


# Abbreviation
better = betterEvaluationFunction

