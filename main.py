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

nb_agent=15
n = 5
grid = [[0 for x in range(n)] for y in range(n)]
lock = RLock()
lock2 = RLock()
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

def possibleMove(x,y, sender) :
    possiblemoves = []
    if(x+1 < n and grid[y][x+1] != sender) :
        possiblemoves.append(-1)
    if(x-1 >= 0 and grid[y][x-1] != sender) :
        possiblemoves.append(1)
    if(y+1 < n and grid[y+1][x] != sender) :
        possiblemoves.append(-2)
    if(y-1 >= 0 and grid[y-1][x] != sender) :
        possiblemoves.append(2)
    return possiblemoves

def possibleMoveFree(x,y) :
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

def findEmptySlot():
    x = randint(1, n-1)
    y = randint(1, n-1)
    while grid[y][x] != 0 :
        x = randint(0, n-1)
        y = randint(1, n-1)
    return [x,y]


class Agent(Thread):
    def __init__(self,key, iniX, iniY, goalX, goalY):
        Thread.__init__(self)
        self.key = key
        self.posX = iniX
        self.posY = iniY
        self.goalX = goalX
        self.goalY = goalY
        self.waitingMove = 0
        global sharedMails
        sharedMails[self.key] = []
        with lock :
            grid[self.posY][self.posX] = key


    def move(self, nextMove):
        with lock :
            grid[self.posY][self.posX] = 0
            moved = False
            if nextMove == -2:
                if(grid[self.posY+1][self.posX] == 0):
                    self.posY += 1
                    moved = True
            elif nextMove == -1 :
                if(grid[self.posY][self.posX+1] == 0):
                    self.posX += 1
                    moved = True
            elif nextMove == 1 :
                if(grid[self.posY][self.posX-1] == 0):
                    self.posX -= 1
                    moved = True
            elif nextMove == 2 :
                if(grid[self.posY-1][self.posX] == 0):
                    self.posY -= 1
                    moved = True
            grid[self.posY][self.posX] = self.key
            print("move from "+ str(self.key))
            for i in range(n):
                print(grid[i])
            print("\n")
        if not moved :
            self.sendMail(nextMove, 0)

    def sendMail(self, nextMove, toGo) :
        agentKey = agentafterMove(self.posX, self.posY, nextMove)
        if(agentKey != 0) :
            #print(str(self.key)+" send mail")
            sharedMails[agentKey].append([self.key, toGo])
            self.waitingMove = nextMove
        else :
            self.move(nextMove)

    def run(self):
        threshold = randint(2, 10)
        tempGoalX = self.goalX
        tempGoalY = self.goalY
        global grid
        global sharedMails
        cont = 0
        contConflict = 0
        timer = 0
        contFailWaitMove = 0
        waitMove = False
        while checkWin() == 0 :
            #print("Agent "+ str(self.key)+ " c "+str(cont))
            if(len(sharedMails[self.key]) > 0):
                lastMail = sharedMails[self.key].pop()
                sharedMails[self.key][:] = []
                contConflict += 1
            else :
                lastMail = -1
                contConflict -= 1
                if(contConflict < 0 ) :
                    contConflict = 0
            if timer > 0 :
                timer -= 1
            if(contConflict >= threshold) :
                print(str(self.key) + " NEW GOAL")
                newGoal = findEmptySlot()
                tempGoalX = newGoal[0]
                tempGoalY = newGoal[1]
                timer = 10
                contConflict = 0
            if timer == 0 :
                tempGoalX = self.goalX
                tempGoalY = self.goalY
            if self.waitingMove != 0 :
                contFailWaitMove += 1
                if contFailWaitMove > 5 :
                    (possible, nextMoves) = dijkstra.dijkstra(grid,[self.posY, self.posX], [tempGoalY, tempGoalX])
                    waitMove = False
                else :
                    waitMove = True
                    possible = 1
            else :
                (possible, nextMoves) = dijkstra.dijkstra(grid,[self.posY, self.posX], [tempGoalY, tempGoalX])
                waitMove = False
            #print(str(self.key) + " : "+str(possible)+ " "+ str(nextMoves))
            if possible == -1 :
                #print("no move possible for "+ str(self.key)+ " goal "+ str(self.goalX)+","+str(self.goalY))
                if(lastMail != -1) :
                    contConflict += 1
                    sender = lastMail[0]
                    objSender = lastMail[1]
                    moves = possibleMoveFree(self.posX, self.posY)
                    if(objSender in moves) :
                        moves.remove(objSender)
                    if(len(moves) == 0) :
                        moves = possibleMove(self.posX, self.posY, sender)
                        if(objSender in moves) :
                            moves.remove(objSender)
                    if(len(moves) > 0) :
                        possible = 1
                        selectedMove = randint(0, len(moves) - 1)
                        nextMove = moves[selectedMove]
                        self.move(nextMove)
                        time.sleep(2)
                    else :
                        if objSender != 0 :
                            self.move(objSender)
                else :
                    if(checkWinSingle(self.key, tempGoalX, tempGoalY) == 0) :
                        if(len(nextMoves) > 1) :
                            self.sendMail(nextMoves[0], nextMoves[1])
                        else :
                            self.sendMail(nextMoves[0], 0)

            else :
                if waitMove :
                    nextMove = self.waitingMove
                    self.waitingMove = 0
                else :
                    nextMove = nextMoves[0]
                self.move(nextMove)
            cont +=1
            time.sleep(1)
agents = [None] * nb_agent
for i in range(nb_agent) :
    agent = Agent(i+1,(n-1-i)%n,i//n,i%n,n-(i//n)-1)
    agents[i] = agent
for i in range(nb_agent) :
    agents[i].start()
for i in range(nb_agent) :
    agents[i].join()
