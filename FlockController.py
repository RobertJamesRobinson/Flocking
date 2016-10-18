'''
Created on Feb 12, 2012

@author: robert
'''

from FlockMember import FlockMember
from time import time
from math import sqrt
from Vector import Vector
from random import randint

class FlockController(object):
    '''
    classdocs
    '''
    members=None
    lastTick=None
    bounds=None
    bindMethod=False
    
    def __init__(self,params=None):
        '''
        Constructor
        '''
        if isinstance(params,dict):
            if 'bounds' in params.keys() and isinstance(params['bounds'],(list,tuple)):
                self.bounds=params['bounds']
            else:
                self.bounds=(1000,1000)
                
            if 'members' in params.keys() and isinstance(params['members'],(list,tuple)):
                self.members=params['members']
            else:
                self.members=[]      
        else:
            self.bounds=(1000,1000)
            self.members=[]
            
        self.lastTick=time()
        
    def addMember(self,member):
        if isinstance(member,FlockMember):
            self.members.append(member)
            
    def tick(self):
        timeSinceLastTick=time()-self.lastTick
        self.lastTick=time()
        for member in self.members:
            desiredVector=Vector(0,0)
            neighbors=member.getNeighbors(self.members)
            tooClose=member.getTooClose(neighbors)
            
            # move away from walls
            nearWall=False
            wallRepulsion=Vector(0,0)
            wallRepulsion.magnitude=0.0
            if not self.bindMethod:
                if (member.pos[0]>(self.bounds[0]-member.personalSpace)):
                    wallRepulsion+=Vector((-1,0))
                    nearWall=True
                if (member.pos[0]<(member.personalSpace)):
                    wallRepulsion+=Vector((1,0))
                    nearWall=True
                if (member.pos[1]>(self.bounds[1]-member.personalSpace)):
                    wallRepulsion+=Vector((0,-1))
                    nearWall=True
                if (member.pos[1]<(member.personalSpace)):
                    wallRepulsion+=Vector((0,1))
                    nearWall=True
                tmpPlot=wallRepulsion.plot()
                wallRepulsion.magnitude=member.maxSpeed*5
                #print "member pos(%0.2f,%0.2f), force(%0.2f, %0.2f) " % (member.pos[0],member.pos[1],tmpPlot[0],tmpPlot[1])
                
            
            #cohesion
            cohesionForce=Vector(0,0)
            if len(neighbors)>0:
                points=[]
                for boid in neighbors:
                    points.append(boid.pos)
                avgPoint=self.avgPoints(points)
                #print avgPoint
                #create the cohesion steering force
                cohesionForce=Vector((avgPoint[0]-member.pos[0],avgPoint[1]-member.pos[1]))
                if cohesionForce>member.maxSpeed:
                    cohesionForce.magnitude=member.maxSpeed
                #cohesionForce.norm()
                cohesionForce.magnitude*=member.cohesion
                
            #alignment
            alignmentForce=Vector(0,0)
            if len(neighbors)>0:    
                for boid in neighbors:
                    alignmentForce+=boid.vector
                #create the alignment steering force
                alignmentForce.magnitude/=len(neighbors)
                if alignmentForce.magnitude>member.maxSpeed:
                    alignmentForce.magnitude=member.maxSpeed
                alignmentForce.magnitude*=member.alignment
                
            #separation
            separationForce=Vector(0,0)
            if len(tooClose)>0:
                for boid in tooClose:
                    dist=self.getDist(member.pos,boid.pos)
                    #thisBoid=member.vector-boid.vector
                    #thisBoid.magnitude=member.personalSpace-dist
                    thisVector=Vector((member.pos[0]-boid.pos[0],member.pos[1]-boid.pos[1]))
                    amount=member.personalSpace-dist
                    thisVector.magnitude=amount
                    separationForce+=thisVector
                    
                #separationForce.magnitude*=
                separationForce.magnitude*=member.separation
            
            #put each vec into the member for debugging
            member.cVec=cohesionForce
            member.sVec=separationForce
            member.aVec=alignmentForce
                
            #combine all forces
            desiredVector+=cohesionForce
            desiredVector+=separationForce
            desiredVector+=alignmentForce
            if nearWall:
                desiredVector+=wallRepulsion
                
            #weight the vector based of the time it has taken to get here
            #desiredVector.magnitude*=timeSinceLastTick
                
            #apply this steering force to the member
            member.steerTo(desiredVector,timeSinceLastTick)
                
        #now that everyones new vectors have been calculated, apply the new vectors to their positions
        for member in self.members:
            #membersPos=member.pos
            #membersTarg=member.vector.plot()
            member.pos=self.bindX(member.pos[0]+member.vector.plot()[0]),self.bindY(member.pos[1]+member.vector.plot()[1])
    
    def getDist(self,p1,p2):
        return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)      
    def bindX(self,myX):
        if self.bindMethod:
            if myX>self.bounds[0]:
                myX=0
            if myX<0:
                myX=self.bounds[0]
            return myX
        else:
            if myX>self.bounds[0]:
                myX=self.bounds[0]-1
            if myX<0:
                myX=1
            return myX
    def bindY(self,myY):
        if self.bindMethod:
            if myY>self.bounds[1]:
                myY=0
            if myY<0:
                myY=self.bounds[1]
            return myY
        else:
            if myY>self.bounds[1]:
                myY=self.bounds[1]-1
            if myY<0:
                myY=1
            return myY
            
    def avgPoints(self,points):
        if len(points)>0:
            avgX=0
            avgY=0
            for point in points:
                avgX+=point[0]
                avgY+=point[1]
            avgX=avgX/float(len(points))
            avgY=avgY/float(len(points))
            return avgX,avgY
        return None
        
            
    