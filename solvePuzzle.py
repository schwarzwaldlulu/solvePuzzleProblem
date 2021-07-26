# using bfs, dft and asterisk to solve the puzzle problem
# using a list of numbers from 0 to 8 to represent the board, where 0 is the only not-occupied space
# 1 to 8 are the tiles on the board
# define the data structures we need queue, stack and priorityQueue
# and the search method bfs, dfs, heuristik(asterisk)

import sys
from math import *
import heapq
import time
import resource


class Board(object):
    
    def __init__(self, tiles = []):
        """using a list of numbers to represent the 8-puzzle board"""
        self.tiles = tiles
        
    def getTiles(self):
        return self.tiles
     
    def __eq__(self, other):
        return self.tiles == other.tiles

    
    def isGoal(self):
        return self.tiles == [0,1,2,3,4,5,6,7,8]

    
    def legalMoves(self):
        """returns a list of legal moves for the not occupied cell"""
        moves = []
        indexOfZero = self.tiles.index(0)
        
        if indexOfZero == 0:
            moves.append('Down')
            moves.append('Right')
        elif indexOfZero == 1:
            moves.append('Down')
            moves.append('Left')
            moves.append('Right')
        elif indexOfZero == 2:
            moves.append('Down')
            moves.append('Left')
        elif indexOfZero == 3:
            moves.append('Up')
            moves.append('Down')
            moves.append('Right')
        elif indexOfZero == 4:
            moves.append('Up')
            moves.append('Down')
            moves.append('Left')
            moves.append('Right')
        elif indexOfZero == 5:
            moves.append('Up')
            moves.append('Down')
            moves.append('Left')
        elif indexOfZero == 6:
            moves.append('Up')
            moves.append('Right')
        elif indexOfZero == 7:
            moves.append('Up')
            moves.append('Left')
            moves.append('Right')
        elif indexOfZero == 8:
            moves.append('Up')
            moves.append('Left')
        else:
            print('something wrong with board')
        return moves

    def childAfterMove(self, m):
        """assumes m is one of the movements 'Up', 'Down', 'Left', 'Right',
             returns a Board resulting from the movement m"""
        indexOfZero = self.tiles.index(0)
        initial = self.tiles[:]
        child = Board(initial)
        if m == 'Up':
            assert(indexOfZero > 2)
            temp = self.tiles[indexOfZero - 3]
            child.tiles[indexOfZero] = temp
            child.tiles[indexOfZero - 3] = 0
        elif m == 'Down':
            assert(indexOfZero < 6)
            temp = self.tiles[indexOfZero + 3]
            child.tiles[indexOfZero] = temp
            child.tiles[indexOfZero + 3] = 0
        elif m == 'Left':
            assert(indexOfZero != 0 and indexOfZero != 3 and indexOfZero != 6)
            temp = self.tiles[indexOfZero - 1]
            child.tiles[indexOfZero] = temp
            child.tiles[indexOfZero - 1] = 0
        elif m == 'Right':
            assert(indexOfZero != 2 and indexOfZero != 5 and indexOfZero != 8)
            temp = self.tiles[indexOfZero + 1]
            child.tiles[indexOfZero] = temp
            child.tiles[indexOfZero + 1] = 0
        else:
            print(m + ' is not a legal movement')
        return child
    
   
    def __hash__(self):
        return hash(str(self.tiles))

    def __str__(self):
        return str(self.tiles)
    
    def __repr__(self):
        return str(self.tiles)

class State(object):
    
    def __init__(self, node):
        """assumes node and parent are both of type Board
           using parent and depth to keep track of the actions leading to the goal"""
        self.node = node
        self.parent = None
        self.depth = None
        
    def __eq__(self, other):
        return self.node == other.node
        
    def setDepth(self, depth):
        self.depth = depth
    def getDepth(self):
        return self.depth
    def setParent(self, parent):
        """assumes parent is of type Node"""
        self.parent = parent
    
    def getParent(self):
        return self.parent
    
    def neighbors(self):
        n = []
        moves = self.node.legalMoves()
        for m in moves:
            node = self.node.childAfterMove(m)
            n.append( State(node) )
        return n
    
    def neighbors_movements_dict(self):
        d = {}
        moves = self.node.legalMoves()
        for m in moves:
            node = self.node.childAfterMove(m)
            d[State(node)] = m
        return d

            
    def __str__(self):
        return str(self.node)
    def __repr__(self):
        return str(self.node)
    def __hash__(self):
        return hash(str(self.node))


# in the following we define 3 data structures, Queue, Stack, PriorityQueue needed
# for the BFS, DFS, A-Star search algorithms

class Queue(object):
    def __init__(self):
        self.items = []
    
    def getItems(self):
        return self.items

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
    def __str__(self):
        return str(self.items)

class Stack(object):
     def __init__(self):
         self.items = []
         
     def getItems(self):
         return self.items
    
     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def size(self):
         return len(self.items)
     def __str__(self):
         return str(self.items)

class PriorityQueue(object):

    def __init__(self):
        """assumes the elements are tuples(value, state)"""
        self.items = []
        
    def getItemByValue(self, value):
        L = [item[0] for item in self.items] #list of the values
        try:
            i = L.index(value)
            return self.items[i]
        except:
            print('can not find the item')
    
    def getItemByKey(self, state):
        L = [item[1] for item in self.items] #list of the values
        for l in L:
            if l == state:
                i = L.index(l)
                return self.items[i]
        print('can not find the item')
    
    def isEmpty(self):
         return self.items == []
           
        
    def pop_smallest(self):
        """returns the state with the smallest value"""
        values = [item[0] for item in self.items] #list of the values
        #values = L[:]
        heapq.heapify(values)
        smallest = heapq.heappop(values)#not forgetting heapq.heapify(values)
         #directly writing t = heapq.heappop([4,2,4]) would result in t = 4
        i = self.getItemByValue(smallest)
        self.items.remove(i)
        return i[1]  
    
    def setItem(self, state, value):
        self.items.append( (value, state) )
        
    def updateIfBetter(self, state, newValue):
        L = [item[1] for item in self.items]
        try:
            index = L.index(state)
            i = self.items[index]
            if i[0] > newValue:
                i[0] = newValue
        except:
            print('can not find the item')

    def __str__(self):
        return str(self.items)
    def __repr__(self):
        return str(self.items)
        

        

def goalTest(state):
    return state.node.isGoal()

#using heuristic in the a-star search to help evaluate the nodes
def heuristicManhattan(state):
    """assumes state is of type State"""
    t = state.node.getTiles()
    tArray = [t[i:i+3] for i  in range(0, 9, 3)]
    heuristik = 0
    for row in range(len(tArray)):
        for col in range(len(tArray[row])):
            if tArray[row][col] == 1:
                heuristik += abs(row) + abs(col - 1)
            elif tArray[row][col] == 2:
                heuristik += abs(row) + abs(col - 2)
            elif tArray[row][col] == 3:
                heuristik += abs(row - 1) + abs(col)
            elif tArray[row][col] == 4:
                heuristik += abs(row - 1) + abs(col - 1)
            elif tArray[row][col] == 5:
                heuristik += abs(row - 1) + abs(col - 2)
            elif tArray[row][col] == 6:
                heuristik += abs(row - 2) + abs(col)
            elif tArray[row][col] == 7:
                heuristik += abs(row - 2) + abs(col - 1)  
            elif tArray[row][col] == 8:
                heuristik += abs(row - 2) + abs(col - 2)
    return heuristik 
    
        

    
def bfs(initialState, goalTest, setOfFrontier = set(), explored = set(), 
        setOfDepth = set(), frontier = Queue() ):
    #frontier is a list of States, here Boards
    initialState.setDepth(0)
    frontier.enqueue(initialState)
    setOfFrontier.add(initialState.node)
    setOfDepth.add(initialState.getDepth())
    while not frontier.isEmpty():
        state = frontier.dequeue()
        setOfFrontier.remove(state.node)
        #print(len(explored))
        if goalTest(state):
            return (state, "Success!")
        explored.add(state)
        for n in state.neighbors():
            frontierCheck = n.node in setOfFrontier
            if ( not frontierCheck ) and ( n not in explored):
                n.setParent(state)
                n.setDepth( state.getDepth() + 1 )
                setOfDepth.add(n.getDepth())
                frontier.enqueue(n)
                setOfFrontier.add(n.node)
    return (None, "Failure!")


def dfs(initialState, goalTest, setOfFrontier = set(), explored = set(), 
        setOfDepth = set(), frontier = Stack() ):
    initialState.setDepth(0)
    frontier.push(initialState)
    setOfFrontier.add(initialState.node) 
    setOfDepth.add(initialState.getDepth())
    while not frontier.isEmpty():
        state = frontier.pop()
        setOfFrontier.remove(state.node)
        #print(len(explored))
        if goalTest(state):
            return (state, "Success!")
        explored.add(state)
        N = state.neighbors()
        N.reverse() #state.neighbors().reverse() would return None
        for n in N:
            frontierCheck = n.node in setOfFrontier
            if ( not frontierCheck ) and ( n not in explored):
                n.setParent(state)
                n.setDepth( state.getDepth() + 1 )
                setOfDepth.add(n.getDepth())
                frontier.push(n)
                setOfFrontier.add(n.node)
    return (None, "Failure!")

def ast(initialState, goalTest, setOfFrontier = set(), explored = set(), 
        setOfDepth = set(), frontier = PriorityQueue() ):
    initialState.setDepth(0)
    frontier.setItem(initialState, heuristicManhattan(initialState))
    setOfFrontier.add(initialState.node) 
    setOfDepth.add(initialState.getDepth())
    while not frontier.isEmpty():
        state = frontier.pop_smallest() #forgetting () would result in bound 
                                        #method Error
        setOfFrontier.remove(state.node)
        if goalTest(state):
            return (state, "Success!")
        explored.add(state)
        for n in state.neighbors():
            frontierCheck = n.node in setOfFrontier
            if ( not frontierCheck ) and ( n not in explored):
                n.setParent(state)
                n.setDepth( state.getDepth() + 1 )
                setOfDepth.add(n.getDepth())
                frontier.setItem(n, heuristicManhattan(n) + n.getDepth())
                setOfFrontier.add(n.node)
            elif frontierCheck:
                 node = frontier.getItemByKey(n)[1]
#                print(setOfFrontier)
#                print(n)
#                print(n.getDepth())
                 frontier.updateIfBetter(node, heuristicManhattan(node) + node.getDepth())
    return (None, "Failure!")


if __name__ == "__main__":
   start_time = time.time()   
   l = [ 1, 6, 0, 2,5,7,3,4,8 ]
   board = Board(l)
   #board = Board( list( map(int, sys.argv[2].split(',')) ) )
   initialState = State(board)
   searchMethode = bfs
   #searchMethode = globals()[ sys.argv[1] ]
   setOfFrontier = set()
   explored = set()
   setOfDepth = set()
   result = searchMethode(initialState, goalTest, setOfFrontier, explored, setOfDepth)

   maxDepth = max(setOfDepth)
   #get search depth
   if (result[1] == "Success!"  ):
      searchDepth = result[0].getDepth()

   path_to_goal = []
   state = result[0]

   for i in range(searchDepth):
       parent = state.getParent()
       d = parent.neighbors_movements_dict()
       m = d[state]
       path_to_goal.append(m)
       state = parent
   path_to_goal.reverse()
   sizeOfPath = len(path_to_goal)


   f = open('output.txt', 'w')
   f.write('path_to_goal: ' + str(path_to_goal) + '\n' )
   f.write('cost_of_path: ' + str(sizeOfPath) + '\n')
   f.write('nodes_expanded: ' + str(len(explored)) + '\n')
   f.write('search_depth: ' + str(searchDepth) + '\n')
   f.write('max_search_depth: ' + str(maxDepth) + '\n')
   f.write('running_time: ' + str( round( time.time() - start_time, 8 ) ) + '\n' )
   f.write('max_ram_usage: ' + str( resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000 ) + '\n')
   f.close()
