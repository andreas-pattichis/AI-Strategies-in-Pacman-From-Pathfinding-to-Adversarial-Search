# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # Initialize the stack to manage the nodes to be visited
    stack = util.Stack()
    # Set to store the visited nodes and avoid revisiting them
    visited = set()
    # Starting node with empty action path
    start_node = (problem.getStartState(), [])

    stack.push(start_node)  # Push the starting node to the stack

    # While there are nodes to be visited
    while not stack.isEmpty():
        # Pop the node from the stack
        location, path = stack.pop()

        # If the node has not been visited
        if location not in visited:
            visited.add(location)  # Mark the node as visited

            # If the node is the goal state, return the path
            if problem.isGoalState(location):
                return path  # Return the path

            successors = problem.getSuccessors(location)  # Get the successors of the node

            # Iterate over the successors and push them to the stack if they have not been visited
            for successor in successors:
                successor_location, action, cost = successor

                if successor_location not in visited:
                    stack.push((successor_location, path + [action]))

    return []  # Return an empty list if no path was found

def heuristic(node1, node2):
    return util.manhattanDistance(node1,node2)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # Initialize the queue to manage the nodes to be visited
    queue = util.Queue()
    # Set to store the visited nodes and avoid revisiting them
    visited = set()
    # Starting node with empty action path
    start_node = (problem.getStartState(), [])

    queue.push(start_node)  # Push the starting node to the queue

    # While there are nodes to be visited
    while not queue.isEmpty():
        # Pop the node from the queue
        location, path = queue.pop()

        # If the node has not been visited
        if location not in visited:
            visited.add(location)  # Mark the node as visited

            # If the node is the goal state, return the path
            if problem.isGoalState(location):
                return path  # Return the path

            successors = problem.getSuccessors(location)  # Get the successors of the node

            # Iterate over the successors and push them to the queue if they have not been visited
            for successor in successors:
                successor_location, action, cost = successor

                if successor_location not in visited:
                    queue.push((successor_location, path + [action]))

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # Initialize the priority queue to manage the nodes to be visited
    priority_queue = util.PriorityQueue()
    # Set to store the visited nodes and avoid revisiting them
    visited = set()
    # Start state of the problem
    start_state = problem.getStartState()
    # Starting node with empty action path and zero cost
    start_node = (start_state, [], 0)  # Node format: (state, path, cost)

    priority_queue.push(start_node, 0)  # Push the starting node to the priority queue

    # While there are nodes to be visited
    while not priority_queue.isEmpty():
        # Pop the node from the priority queue
        current_state, path, current_cost = priority_queue.pop()

        # If the node has not been visited then continue
        if current_state in visited:
            continue

        visited.add(current_state)  # Mark the node as visited

        # If the node is the goal state, return the path
        if problem.isGoalState(current_state):
            return path

        # Get the successors of the node and iterate over them
        for successor_state, action, step_cost in problem.getSuccessors(current_state):
            # If the successor has not been visited
            if successor_state not in visited:
                # Create a new node with the successor state, the path to the successor and the cost to get there
                new_path = path + [action]
                new_cost = current_cost + step_cost
                new_node = (successor_state, new_path, new_cost)
                # Push the new node to the priority queue
                priority_queue.push(new_node, new_cost)

    return []  # Return an empty list if no path was found


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # Initialize the priority queue to manage the nodes to be visited
    priority_queue = util.PriorityQueue()
    # Set to store the visited nodes and avoid revisiting them
    visited = set()
    # Start state of the problem
    start_state = problem.getStartState()
    # Starting node with empty action path and zero cost
    start_node = (start_state, [], 0)  # Node format: (state, path, cost)

    priority_queue.push(start_node, 0)  # Push the starting node to the priority queue

    # While there are nodes to be visited
    while not priority_queue.isEmpty():
        # Pop the node from the priority queue
        current_state, path, current_cost = priority_queue.pop()

        # If the node has not been visited then continue
        if current_state in visited:
            continue

        visited.add(current_state)  # Mark the node as visited

        # If the node is the goal state, return the path
        if problem.isGoalState(current_state):
            return path

        # Get the successors of the node and iterate over them
        for successor_state, action, step_cost in problem.getSuccessors(current_state):
            # If the successor has not been visited
            if successor_state not in visited:
                # Create a new node with the successor state, the path to the successor and the cost to get there
                new_path = path + [action]
                new_cost = current_cost + step_cost
                total_cost = new_cost + heuristic(successor_state, problem)  # Combined cost and heuristic
                new_node = (successor_state, new_path, new_cost)
                # Push the new node to the priority queue
                priority_queue.push(new_node, total_cost)

    return []  # Return an empty list if no path was found


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
