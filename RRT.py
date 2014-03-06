#!/usr/bin/env python

# rrt.py
# This program generates a simple rapidly
# exploring random tree (RRT) in a rectangular region.
#
# Written by Steve LaValle
# May 2011

import sys, random, math, pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2

class Node(object):
    """Node in a tree"""
    def __init__(self, point, parent):
        super(Node, self).__init__()
        self.point = point
        self.parent = parent

#constants
XDIM = 640
YDIM = 480
WINSIZE = [XDIM, YDIM]
EPSILON = 7.0
NUMNODES = 5000
GOAL_RADIUS = 10
MIN_DISTANCE_TO_ADD = 1.0

pygame.init()

#initialize and prepare screen
screen = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption('Rapidly Exploring Random Tree')
white = 255, 240, 200
black = 20, 20, 40
red = 255, 0, 0
blue = 0, 255, 0
green = 0, 0, 255
cyan = 0,255,255
screen.fill(black)
count = 0

rectObs = []

fpsClock = pygame.time.Clock()

def dist(p1,p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def step_from_to(p1,p2):
    if dist(p1,p2) < EPSILON:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + EPSILON*cos(theta), p1[1] + EPSILON*sin(theta)

def collides(p):
    for rect in rectObs:
        if rect.collidepoint(p) == True:
            # print ("collision with object: " + str(rect))
            return True
    return False


def init_obstacles(configNum):
    global rectObs
    rectObs = []
    print("config "+ str(configNum))
    if (configNum == 0):
        rectObs.append(pygame.Rect((40,10),(100,200)))

    for rect in rectObs:
        pygame.draw.rect(screen, red, rect)

def get_random():
    return random.random()*XDIM, random.random()*YDIM

def get_random_clear():
    while True:
        p = random.random()*XDIM, random.random()*YDIM
        noCollision = collides(p)
        if noCollision == False:
            return p

def point_circle_collision(p1, p2, radius):
    distance = dist(p1,p2)
    if (distance <= radius):
        return True
    return False

def reset():
    global count
    screen.fill(black)
    init_obstacles(0)
    count = 0

def main():
    global count
    
    initPoseSet = False
    initialPoint = Node(None, None)
    goalPoseSet = False
    goalPoint = Node(None, None)
    goalFound = False
    buildTreePhase = False
    setPointPhase = True

    nodes = []
    reset()
    init_obstacles(0)

    while True:
        if setPointPhase == True:
            buildTreePhase = False
            goalFound = False
            print('goal point not yet set')
            fpsClock.tick(10)
        elif goalFound == True:
            #traceback
            currNode = goalNode.parent
            while currNode.parent != None:
                pygame.draw.line(screen,cyan,currNode.point,currNode.parent.point)
                currNode = currNode.parent

        elif buildTreePhase == True:
            count = count+1
            if count < NUMNODES:
                foundNext = False
                while foundNext == False:
                    rand = get_random_clear()
                    # print("random num = " + str(rand))
                    parentNode = nodes[0]
                    if count == 0:
                        foundNext = True

                    for p in nodes: #find nearest vertex
                        if dist(p.point,rand) <= dist(parentNode.point,rand): #check to see if this vertex is closer than the previously selected closest
                            newPoint = step_from_to(p.point,rand)
                            if collides(newPoint) == False: # check if a collision would occur with the newly selected vertex
                                parentNode = p #the new point is not in collision, so update this new vertex as the best
                                foundNext = True

                newnode = step_from_to(parentNode.point,rand)
                nodes.append(Node(newnode, parentNode))
                pygame.draw.line(screen,white,parentNode.point,newnode)

                if point_circle_collision(newnode, goalPoint.point, GOAL_RADIUS):
                    goalFound = True
                    goalNode = nodes[len(nodes)-1]

                if count%100 == 0:
                    print("node: " + str(count))
            else:
                print("Finished")
                break;

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Leaving because you requested it.")
            if e.type == MOUSEBUTTONDOWN:
                print('mouse down')
                if setPointPhase == True:
                    if initPoseSet == False:
                        nodes = []
                        if collides(e.pos) == False:
                            print('initiale pose set: '+str(e.pos))

                            initialPoint = Node(e.pos, None)
                            nodes.append(initialPoint) # Start in the center
                            initPoseSet = True
                            pygame.draw.circle(screen, blue, initialPoint.point, GOAL_RADIUS)
                    elif goalPoseSet == False:
                        print('goal pose set: '+str(e.pos))
                        if collides(e.pos) == False:
                            goalPoint = Node(e.pos,None)
                            goalPoseSet = True
                            pygame.draw.circle(screen, green, goalPoint.point, GOAL_RADIUS)
                            buildTreePhase = True
                            setPointPhase = False
                else:
                    setPointPhase = True
                    initPoseSet = False
                    goalPoseSet = False
                    reset()

        pygame.display.update()
        fpsClock.tick(10000)


# if python says run, then we should run
if __name__ == '__main__':
    main()
    raw_input("press any key to quit")
