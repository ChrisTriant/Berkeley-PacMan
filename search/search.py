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

class Node:

  def __init__(self,previous,state,action,cost):
    self.previous=previous
    self.state=state
    self.action=action
    self.cost=cost

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    explore=[]
    node=Node(None,problem.getStartState(),None,None)
    frontier = util.Stack()
    frontier.push(node)
    while not frontier.isEmpty():
      node=frontier.pop()
      if node.state not in explore:
        explore.append(node.state)
      if problem.isGoalState(node.state):
        break
      else:
        succ=problem.getSuccessors(node.state)
        for s,x,y in succ :
          if s not in explore:
            node2=Node(node,s,x,None)
            frontier.push(node2)
    path=[]
    while node.action!=None :
      path.insert(0,node.action)
      node=node.previous
    return path
            
      




def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    explored=[]
    node=Node(None,problem.getStartState(),None,None)
    frontier = util.Queue()
    frontier.push(node)
    while not frontier.isEmpty():
      node=frontier.pop()
      if (node.state not in explored):
        explored.append(node.state)
        if problem.isGoalState(node.state):
          break
        else:
          succ=problem.getSuccessors(node.state)
          for s,x,y in succ :
            if s not in explored:
              node2=Node(node,s,x,None)
              if (node not in frontier.list):
                frontier.push(node2)
    path=[]
    while node.action!=None :
      path.insert(0,node.action)
      node=node.previous
    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    explored=[]
    node=Node(None,problem.getStartState(),None,0)
    frontier = util.PriorityQueue()
    frontier.update(node,node.cost)
    while True:
      node=frontier.pop()
      current_cost=node.cost
      if (node.state not in explored):
        explored.append(node.state)
        if problem.isGoalState(node.state):
          break
        else:
          succ=problem.getSuccessors(node.state)
          for s,x,y in succ :
            if s not in explored:
              node2=Node(node,s,x,y)
              if (node not in frontier.heap):
                full_cost=current_cost+node2.cost
                node2.cost=full_cost
                frontier.update(node2,full_cost)
    path=[]
    while node.action!=None :
      path.insert(0,node.action)
      node=node.previous
    return path
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    explored=[]
    node=Node(None,problem.getStartState(),None,0)
    frontier = util.PriorityQueue()
    frontier.update(node,node.cost+heuristic(node.state,problem))
    while True:
      node=frontier.pop()
      current_cost=node.cost
      if (node.state not in explored):
        explored.append(node.state)
        if problem.isGoalState(node.state):
          break
        else:
          succ=problem.getSuccessors(node.state)
          for s,x,y in succ :
            if s not in explored:
              node2=Node(node,s,x,y)
              if (node not in frontier.heap):
                full_cost=current_cost+node2.cost
                node2.cost=full_cost
                frontier.update(node2,node2.cost+heuristic(node2.state,problem))
    path=[]
    while node.action!=None :
      path.insert(0,node.action)
      node=node.previous
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
