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
		newFood = successorGameState.getFood().asList()
		newGhostStates = successorGameState.getGhostStates()
		newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

		"*** YOUR CODE HERE ***"
		# strategy: focus on eating food and don't go near the ghosts.
		minFoodDist = float("inf")	#init minimal food distance
		ghostdist = successorGameState.getGhostPositions()
		for food in newFood:		#find food with the shortest distance
			minFoodDist = min(minFoodDist, manhattanDistance(newPos, food))
		#avoid ghost that is too close
		for ghosts in ghostdist:
			if(manhattanDistance(newPos, ghosts) < 2):
				return -float('inf')
		scared_time = min(newScaredTimes) #for power pellet	 	
		#reciprocal	
		return 1.0/minFoodDist + scared_time * 0.75 + successorGameState.getScore()

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
		def minmax(gameState, agent, depth):
			if agent >= gameState.getNumAgents():	
				agent = 0
				depth += 1
			if (gameState.isWin() or gameState.isLose() or self.depth == depth):	#return in case the game is over or the defined depth is reached
				return self.evaluationFunction(gameState)
			return util_function(gameState, agent, depth)
		
		def util_function(gameState, agent, depth):		#util_function = maximize if the agent is pacman and minimize otherwise
			if agent == 0:
				best_action = ["max", -float("inf")]		#array to save the output [chosen action, score]
			else:
				best_action = ["min", float("inf")]
			if not gameState.getLegalActions(agent):		#no legal action for the agent, return
				return self.evaluationFunction(gameState)
			for action in gameState.getLegalActions(agent):
				successor_state = gameState.generateSuccessor(agent, action)
				score = minmax(successor_state, agent+1, depth)
				ret_score = score[1] if type(score) == list else score
				if agent == 0:	
					if(ret_score > best_action[1]):			#maximize
						best_action[0] = action
						best_action[1] = ret_score
				else:
					if(ret_score < best_action[1]):			#minimize
						best_action[0] = action
						best_action[1] = ret_score		
			return best_action   	
		return minmax(gameState, 0, 0)[0]		  

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		"*** YOUR CODE HERE ***"
		# very similar with question 2. Lines 207-209 and 216-218 are the added parts. It is the implementation of the pseudo-code given in the problem descriptions. 
		def minmax(gameState, agent, depth, alpha, beta):
			if agent >= gameState.getNumAgents():	
				agent = 0
				depth += 1
			if (gameState.isWin() or gameState.isLose() or self.depth == depth):
				return self.evaluationFunction(gameState)
			return util_function(gameState, agent, depth, alpha, beta)
		
		def util_function(gameState, agent, depth, alpha, beta):
			if agent == 0:
				best_action = ["max", -float("inf")]		
			else:
				best_action = ["min", float("inf")]
			if not gameState.getLegalActions(agent):		
				return self.evaluationFunction(gameState)	
			for action in gameState.getLegalActions(agent):
				successor_state = gameState.generateSuccessor(agent, action)
				score = minmax(successor_state, agent+1, depth, alpha, beta)
				ret_score = score[1] if type(score) == list else score
				if agent == 0:	
					if(ret_score > best_action[1]):			#maximize
						best_action[0] = action
						best_action[1] = ret_score
					if ret_score > beta:					#alpha-beta pruning
						return [action, ret_score]
					alpha = max(alpha, ret_score)				
				else:
					if(ret_score < best_action[1]):			#minimize
						best_action[0] = action
						best_action[1] = ret_score
					if ret_score < alpha:					#alpha-beta pruning
						return [action, ret_score]
					beta = min(beta, ret_score)		
			return best_action
		
		return minmax(gameState, 0, 0, -float("inf"), float("inf"))[0]		#init alpha = -inf, beta = inf				

				

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
		#the structure of these functions follow the structure of the functions of minmax closely, with slight modifications.
		def expectimax(gameState, agent, depth):
			if agent >= gameState.getNumAgents():	
				agent = 0
				depth += 1
			if (gameState.isWin() or gameState.isLose() or self.depth == depth):
				return self.evaluationFunction(gameState)
			return util_function(gameState, agent, depth)

		def util_function(gameState, agent, depth):
			if agent == 0:
				best_action = ["max", -float("inf")]		
			else:
				best_action = ["exp", 0]
			if not gameState.getLegalActions(agent):		
				return self.evaluationFunction(gameState)
			for action in gameState.getLegalActions(agent):
				successor_state = gameState.generateSuccessor(agent, action)
				score = expectimax(successor_state, agent+1, depth)
				ret_score = score[1] if type(score) == list else score
				if agent == 0:
					if ret_score > best_action[1]:
						best_action[0] = action
						best_action[1] = ret_score
				else:						#expect
					best_action[0] = action
					best_action[1] += ret_score * 1.0/len(gameState.getLegalActions(agent))	 #multiply ret_score with the probability. Assume all nodes have equal p
			return best_action
		
		return expectimax(gameState, 0, 0)[0]		

def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION: <write something here so we know what you did>
	"""
	"*** YOUR CODE HERE ***"
	# problem not defined
	util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

