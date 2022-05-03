from mimetypes import init
import sys
import timeit
import csv

if len(sys.argv) != 3: # if the number of arguments is not 3
    print("ERROR: Not enough or too many input arguments.")
    quit()
initial=sys.argv[1] #save first input argument which should be the desired initial state
num_parks=int(sys.argv[2]) # save second argument which should be desired min number of parks to vist
#initialize 3 dictionarys that hold driving distance, number of parks, and zone number, respectively 
driving_dict={}
parks_dict={}
zone_dict={}

# create a dictionary of dictionaries for the driving2 csv file since each state also needs to hold information about other states
# for example, AL will include driving distance from AL to other states including itself
with open('driving2.csv', 'rt') as f:
    driving = csv.DictReader(f)
    for row in driving:
        state = row['STATE']
        del row['STATE']
        driving_dict[state] = dict(row)
#create a regular dictionary that contains the state and the number of parks it has in it
#for example, AL will store the number of national parks it has which is 0 
with open("parks.csv",'rt') as f:
    p=csv.DictReader(f)
    for row in p:
        del row['STATE']
        parks_dict=row
#create a regular dictionary that contains the state and the zone it is a part of
#for example, AL will store the zone number it is a part of which is 6 
with open("zones.csv",'rt') as f:
    z=csv.DictReader(f)
    for row in z:
        del row['STATE']
        zone_dict=row

# Add print statements to setup output
print("Syed, Sohaib, A20439074 soltuion:") 
print("Initial state:", initial)
print("Minimum number of parks:", num_parks)
print()

# check if the initial state user wants to start at is an appropriate state that exists in the driving dictionary
if(initial not in driving_dict):
    print("Soltuion path: FAILURE: NO PATH FOUND")
    print("Number of states on a path:",0)
    print("Path cost:",0)
    print("Number of national parks visited:",0)
    quit()
# intialize a dictionary that will act as the 'assignment' argument from pseudocode
assignment={}
#define backtracking_search where initial is the state and num_parks is the number of minimum expected parks to be visted
def backtracking_search(initial,num_parks):
    f=int(zone_dict[initial]) # get zone of initial state
    i=f # assign same value to i to make appropriate sized assignment dictionary
    for x in range(i,13):
        assignment.update({x:None})# set all initial values of dictionary to be none for each zone, where the x is the zone number
    actual=int(parks_dict[initial]) # number of parks that have been visited, starting with the initial state
    assignment.update({f:(initial,int(driving_dict[initial][initial]))})#where f is the key representing the zone, set value to a tuple with values('STATE LABEL',Driving distance to get to that state)
    return backtrack(initial,num_parks,actual,driving_dict,parks_dict,zone_dict,assignment) # initial call to backtrack where in addition to initial and num_parks(described above), I also pass: number of parks visited so far, the 3 csv dictionries and the assignment dictionary

#define the recursive backtrack function with the arguments described above
def backtrack(state,expected,actual,driving,parks,zone,a):
    if a[12]!=None: # check for if assignment has finished, in my case the last key in the assignment argument is NOT None
        if actual>=expected: #if the number of parks actually visited is at least the expected number of parks to be visted
            return (assignment,actual) # if both cases are true return a tuple containing the assignment dictionary and total number parks traveled
        return -1 # if last state has a value but number of states visted didn't meet expected than return -1 to indicate failure
    neighbors=[] #initialize array to hold bordering states
    var=int(zone[state])+1 # get NEXT zone
    for key,val in driving_dict[state].items(): #iterate throuh dictionary looking for bordering states, add to neigbors array if there exists such states
        if val=='-1' or val =='0':
            pass
        else:
            neighbors.append(key)
    for x in neighbors: # go through each neighbor
        if int(zone[x])==var: #check if neighbor is in next zone
            a.update({var:(x,int(driving_dict[state][x]))}) # update assignment dicitonary to hold appropriate values for the key (var in my case which is the zone of the neighbor)
            result=backtrack(x,expected,actual+int(parks[x]),driving,parks,zone,a) # recurse on function, with updated csp values and assignment dictionary
            if result == -1: #if the recursion returned a failure, set the value of the zone back to None
                a.update({var:None})
            else:
                return result# else return updated dictionary and number of parks visted
    return -1
result=backtracking_search(initial,num_parks) #inital call to algorithm to be saved into 'result'
cost=0 #define initial cost
path=[] #define initial path
if(result==-1): #print this if no path was found
    print("Soltuion path: FAILURE: NO PATH FOUND")
    print("Number of states on a path:",0)
    print("Path cost:",0)
    print("Number of national parks visited:",0)
else: #print this if successful path found
    for key,val in result[0].items(): #loop through first element of 'result' which was the assignment dictioanry
        cost+=val[1] # accumulate total cost by summing second value of 'val' which was the cost to get to that state from previous state
        path.append(val[0])# append states visted 
    print("Soltuion path:",path)
    print("Number of states on a path:",len(result[0]))
    print("Path cost:",cost)
    print("Number of national parks visited:",result[1])
    print()