from threading import Thread, RLock
import socket
import dijkstra
import time
from random import randint

"""
Created on Mon Oct 16 16:10:10 2017

@author: Quentin
2=top
1=left
-1=right
-2=bot
"""

nb_agent=10
n = 5
grid = [[0 for x in range(n)] for y in range(n)]
lock = RLock()
sharedMails = {}

def checkWin() :
    for i in range(nb_agent):
        if grid[int(i/n)][int(i%n)] != i+1 :
            return 0
    return 1

def checkWinSingle(agent, goalX, goalY) :
    if grid[goalY][goalX] != agent :
            return 0
    return 1 

def possibleMove(x,y) :
    possiblemoves = []
    if(x+1 < n and grid[y][x+1] == 0) :
        possiblemoves.append(-1)
    if(x-1 >= 0 and grid[y][x-1] == 0) :
        possiblemoves.append(1)
    if(y+1 < n and grid[y+1][x] == 0) :
        possiblemoves.append(-2)
    if(y-1 >= 0 and grid[y-1][x] == 0) :
        possiblemoves.append(2)
    return possiblemoves

def agentafterMove(x,y,move) :
    if move == -2:
        return grid[y+1][x]                        
    elif move == -1 :
        return grid[y][x+1]       
    elif move == 1 :
        return grid[y][x-1]       
    elif move == 2 :
        return grid[y-1][x]
    else :
        return 0


class Agent(Thread):
    def __init__(self,key, iniX, iniY, goalX, goalY): 
        Thread.__init__(self)
        self.key = key
        self.posX = iniX
        self.posY = iniY
        self.goalX = goalX
        self.goalY = goalY
        global sharedMails
        sharedMails[self.key] = []
        with lock :
            grid[self.posY][self.posX] = key



    def run(self):
        global grid
        global sharedMails
        cont = 0
        while checkWin() == 0 and cont < 30 :
            if(len(sharedMails[self.key]) > 0):
                lastMail = sharedMails[self.key].pop()
                sharedMails[self.key][:] = []
            else :
                lastMail = -1
            if self.key == 1:
                for i in range(n):
                    print(grid[i])
                print("\n")
            (possible, nextMoves) = dijkstra.dijkstra(grid,[self.posY, self.posX], [self.goalY, self.goalX])
            #print(str(self.key) + " : "+str(possible)+ " "+ str(nextMoves))
            if possible == -1 :
                #print("no move possible for "+ str(self.key)+ " goal "+ str(self.goalX)+","+str(self.goalY))
                if(lastMail != -1) : 
                    moves = possibleMove(self.posX, self.posY)
                    if(len(moves) > 0) :
                        possible = 1
                        selectedMove = randint(0, len(moves) - 1)
                        nextMove = moves[selectedMove]
                        print(str(self.key) +" MOVE BECAUSE OF "+lastMail+ " NEXT MOVE "+ str(nextMove))
                else :
                    if(checkWinSingle(self.key, self.goalX, self.goalY) == 0) :
                        needToMove = nextMoves[0]
                        agentKey = agentafterMove(self.posX, self.posY, needToMove)
                        if(agentKey != 0) : 
                            sharedMails[agentKey].append("FROM 1 MOVE")
                            #print(str(self.key) + " SAYS TO "+str(agent.key)+" TO MOVE!")
            else :
                nextMove = nextMoves[0]
            if possible == 1 :
                with lock :
                    grid[self.posY][self.posX] = 0 
                    if nextMove == -2:
                        if(grid[self.posY+1][self.posX] == 0):
                            self.posY += 1                        
                    elif nextMove == -1 :
                        if(grid[self.posY][self.posX+1] == 0):
                            self.posX += 1
                    elif nextMove == 1 :
                        if(grid[self.posY][self.posX-1] == 0):
                            self.posX -= 1
                    elif nextMove == 2 :
                        if(grid[self.posY-1][self.posX] == 0):
                            self.posY -= 1
                    grid[self.posY][self.posX] = self.key
                cont +=1
            time.sleep(1) #seconds
                    
agents = [None] * nb_agent
for i in range(nb_agent) :
    agent = Agent(i+1,(n-1-i)%n,i//n,i%n,n-(i//n)-1)
    agents[i] = agent
for i in range(nb_agent) :
    agents[i].start() 
for i in range(nb_agent) :
    agents[i].join()

            
        
