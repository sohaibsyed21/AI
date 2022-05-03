from queue import PriorityQueue
import sys
import timeit
import csv

from numpy import average
from NodeClass_A20439074 import Node

numberOfArgumentsPassedFromCommandLine = len(sys.argv)
initial=sys.argv[1]
goal=sys.argv[2]
if numberOfArgumentsPassedFromCommandLine != 3:
    print("ERROR: Not enough or too many input arguments.")
    quit()

driving_dict={}
straight_dict={}

with open('driving.csv', 'rt') as f:
    driving = csv.DictReader(f)
    for row in driving:
        state = row['STATE']
        del row['STATE']
        driving_dict[state] = dict(row)

with open('straightline.csv', 'rt') as s:
    straight = csv.DictReader(s)
    for row in straight:
        state = row['STATE']
        del row['STATE']
        straight_dict[state] = dict(row)


print("Initial state:", initial)
print("Goal state:", goal)
print()
if (goal not in straight_dict or initial not in straight_dict) or (goal not in driving_dict or initial not in driving_dict):
        print("Greedy Best First Search:")
        print("Solution path: FAILURE: NO PATH FOUND")
        print("Number of state on a path: 0")
        print("Path cost: 0")
        print("Execution time: 0")
        print()
        print("A* Search:")
        print("Solution path: FAILURE: NO PATH FOUND")
        print("Number of state on a path: 0")
        print("Path cost: 0")
        print("Execution time: 0")
        quit()
        
def GBFS(initial,goal):
    timeStart = timeit.default_timer()
    reached=dict()
    start=Node(state=initial,parent=None,pathCost=0,heuristics=int(straight_dict[initial][goal]), algorithm='GBFS')
    frontier=PriorityQueue()
    frontier.put((start.getEval(),start))
    reached.update({initial:start})
    while not frontier.qsize()==0:
        g,currNode=frontier.get()
        if currNode.getState()==goal:
            timeEnd = timeit.default_timer()
            return [currNode,timeEnd-timeStart]
        for child in GBFS_Expand(initial,currNode):
            s=child.getState()
            if s not in reached or child.getEval()<reached[s].getEval():
                reached[s]=child
                frontier.put((child.getEval(), child))
    return [start,timeEnd-timeStart]

def ASTAR(initial,goal):
    timeStart = timeit.default_timer()
    reached=dict()
    start=Node(state=initial,parent=None,pathCost=0,heuristics=int(straight_dict[initial][goal]), algorithm='ASTAR')
    frontier=PriorityQueue()
    frontier.put((start.getEval(),start))
    reached.update({initial:start})
    while not frontier.qsize()==0:
        g,currNode=frontier.get()
        if currNode.getState()==goal:
            timeEnd = timeit.default_timer()
            return [currNode,timeEnd-timeStart]
        for child in AExpand(initial,currNode):
            s=child.getState()
            if s not in reached or child.getEval()<reached[s].getEval():
                reached[s]=child
                frontier.put((child.getEval(), child))
    timeEnd = timeit.default_timer()
    return [start,timeEnd-timeStart]

def GBFS_Expand(initial,toExpand):
    children=[]
    s=toExpand.getState()
    for key,val in driving_dict[s].items():
        if val =='-1':
            pass
        else:
            sprime=key
            cost=int(val)+toExpand.getPathCost()
            children.append(Node(sprime,toExpand,cost,int(straight_dict[sprime][goal]),'GBFS'))
    return children

def AExpand(initial,toExpand):
    children=[]
    s=toExpand.getState()
    for key,val in driving_dict[s].items():
        if val =='-1':
            pass
        else:
            sprime=key
            cost=int(val)+toExpand.getPathCost()
            children.append(Node(sprime,toExpand,cost,int(straight_dict[sprime][goal]),'ASTAR'))
    return children

greedy_Node=GBFS(initial,goal)
astar_Node=ASTAR(initial,goal)
gCost=greedy_Node[0].getPathCost()
aCost=astar_Node[0].getPathCost()
gPath=[]
aPath=[]
while greedy_Node[0]!=None:
    gPath.append(greedy_Node[0].getState())
    greedy_Node[0]=greedy_Node[0].getParent()
gPath.reverse()
while astar_Node[0]!=None:
    aPath.append(astar_Node[0].getState())
    astar_Node[0]=astar_Node[0].getParent()
aPath.reverse()

print("Greedy Best First Search:")
print("Solution path:", gPath)
print("Number of state on a path:", len(gPath))
print("Path cost:",gCost)
print("Execution time:", greedy_Node[1])
print()
print("A* Search:")
print("Solution path:",aPath)
print("Number of state on a path:",len(aPath))
print("Path cost:", aCost)
print("Execution time:",astar_Node[1])
print()
GBFS_time=0
Astar_time=0
for i in range(10):
    GBFS_time+=GBFS(initial,goal)[1]
    Astar_time+=ASTAR(initial,goal)[1]
print("GBFS average",GBFS_time/(10.0))
print("ASTAR average", Astar_time/(10.0))
