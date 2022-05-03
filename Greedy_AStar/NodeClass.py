class Node:
    def __init__(self, state, parent, pathCost, heuristics, algorithm):
        self.STATE = state
        self.PARENT = parent
        self.PATHCOST = pathCost
        self.HEURISTICS = heuristics
        if algorithm == 'GBFS':
            self.EVAL = self.HEURISTICS
        elif algorithm == 'ASTAR':
            self.EVAL = self.PATHCOST + self.HEURISTICS
        
    def getState(self):
        return self.STATE
        
    def getParent(self):
        return self.PARENT

    def getPathCost(self):
        return self.PATHCOST
        
    def getHeuristics(self):
        return self.HEURISTICS
      
    def getEval(self):
        return self.EVAL
      
    def __lt__(self, other):
        return self.getEval() < other.getEval()