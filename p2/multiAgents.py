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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        # Get a list of food positions and distances
        foodPositions = newFood.asList()
        foodDistances = [manhattanDistance(food, newPos) for food in foodPositions]

        # Get the ghost positions and their distances to Pacman
        ghostPositions = successorGameState.getGhostPositions()
        ghostDistances = [manhattanDistance(ghost, newPos) for ghost in ghostPositions]

        # Check if Pacman won (ate all the food)
        if len(foodDistances) == 0:
            return float("inf")

        # Check if Pacman lost (caught by a ghost)
        if min(ghostDistances) < 2:
            return -(float("inf"))

        if currentGameState.getPacmanPosition() == newPos:
            return (-(float("inf")))

        score = 0

        if currentGameState.getCapsules():
            score += 5 / (manhattanDistance(currentGameState.getCapsules()[0], newPos) + 1)

        score += 10 / min(foodDistances) + 10000 / (len(foodDistances))

        # Encourage Pacman to eat scared ghosts
        for ghostDistance, scaredTime in zip(ghostDistances, newScaredTimes):
            if scaredTime > 0:
                score += 50000 / (ghostDistance + 1)

        return score


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        def minimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None
            actions = gameState.getLegalActions(agentIndex)
            if agentIndex == 0:  # Pacman's turn (Max)
                values = [minimax(1, depth, gameState.generateSuccessor(agentIndex, action))[0] for action in actions]
                return max(values), actions[values.index(max(values))]
            else:  # Ghosts' turn (Min)
                nextAgent = agentIndex + 1 if agentIndex + 1 < gameState.getNumAgents() else 0
                nextDepth = depth + 1 if nextAgent == 0 else depth
                values = [minimax(nextAgent, nextDepth, gameState.generateSuccessor(agentIndex, action))[0] for action
                          in actions]
                return min(values), actions[values.index(min(values))]

        return minimax(0, 0, gameState)[1]

        # util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        def alphabeta(agentIndex, depth, gameState, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None
            actions = gameState.getLegalActions(agentIndex)
            if agentIndex == 0:  # Pacman's turn (Max)
                value = float('-inf')
                action_to_take = None
                for action in actions:
                    new_value, _ = alphabeta(1, depth, gameState.generateSuccessor(agentIndex, action), alpha, beta)
                    if new_value > value:
                        value = new_value
                        action_to_take = action
                    if value > beta:
                        return value, action_to_take
                    alpha = max(alpha, value)
                return value, action_to_take
            else:  # Ghosts' turn (Min)
                value = float('inf')
                action_to_take = None
                nextAgent = agentIndex + 1 if agentIndex + 1 < gameState.getNumAgents() else 0
                nextDepth = depth + 1 if nextAgent == 0 else depth
                for action in actions:
                    new_value, _ = alphabeta(nextAgent, nextDepth, gameState.generateSuccessor(agentIndex, action), alpha, beta)
                    if new_value < value:
                        value = new_value
                        action_to_take = action
                    if value < alpha:
                        return value, action_to_take
                    beta = min(beta, value)
                return value, action_to_take

        return alphabeta(0, 0, gameState, float('-inf'), float('inf'))[1]



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
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction