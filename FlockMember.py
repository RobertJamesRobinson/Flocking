'''
Created on Feb 12, 2012

@author: robert
'''
from math import hypot
from Vector import Vector
from random import random

class FlockMember(object):
    '''
    classdocs
    '''
    pos=None
    vector=None
    maxTurnRate=None
    maxSpeed=None
    neighborhoodRadius=None
    cohesion=None
    separation=None
    alignment=None
    personalSpace=None
    cVec=Vector(0,0)
    sVec=Vector(0,0)
    aVec=Vector(0,0)
    
    def __init__(self,params=None): #params: 'pos','vector','maxTurnRate','maxSpeed','neighborhoodRadius','cohesion','separation','alignment'
        '''
        Constructor
        '''
        if isinstance(params,dict):
            
            if 'pos' in params.keys():
                self.pos=params['pos']
            else:
                self.pos=(0,0)
                
            if 'vector' in params.keys():
                self.vector=params['vector']
            else:
                self.vector=Vector(0,0)
                
            if 'maxTurnRate' in params.keys():
                self.maxTurnRate=params['maxTurnRate']
            else:
                self.maxTurnRate=1
                
            if 'personalSpace' in params.keys():
                self.personalSpace=params['personalSpace']
            else:
                self.personalSpace=5
                
            if 'maxSpeed' in params.keys():
                self.maxSpeed=params['maxSpeed']
            else:
                self.maxSpeed=1
                
            if 'neighborhoodRadius' in params.keys():
                self.neighborhoodRadius=params['neighborhoodRadius']
            else:
                self.neighborhoodRadius=10
                
            if 'cohesion' in params.keys():
                self.cohesion=params['cohesion']
                self.cohesion+=random()*(self.cohesion-0.1)-((self.cohesion-0.1)/2.0)
            else:
                self.cohesion=0.5
                
            if 'separation' in params.keys():
                self.separation=params['separation']
                self.separation+=random()*(self.separation-0.1)-((self.separation-0.1)/2.0)
            else:
                self.separation=0.5
                
            if 'alignment' in params.keys():
                self.alignment=params['alignment']
                self.alignment+=random()*(self.alignment-0.1)-((self.alignment-0.1)/2.0)
            else:
                self.alignment=0.5
        else:
            self.pos=(0,0)
            self.vector=Vector(0,0)
            self.maxTurnRate=1
            self.maxSpeed=1
            self.neighborhoodRadius=10
            self.personalSpace=5
            self.cohesion=0.5
            self.separation=0.5
            self.alignment=0.5
    
    def steerTo(self,targetVector,easement):
        self.vector=self.vector+targetVector*easement
        if self.vector.magnitude>self.maxSpeed:
            self.vector.magnitude=self.maxSpeed  
        #self.vector.magnitude/=2
        #self.vector.magnitude*=(easement*5)
        #self.vector.magnitude/=2
        #if self.vector.magnitude>self.maxSpeed:
        #    self.vector.magnitude=self.maxSpeed           
            
    
    def getNeighbors(self,memberList):
        neighbors=[]
        for member in memberList:
            if not member==self:
                if self.getDistTo(member)<=self.neighborhoodRadius:
                    neighbors.append(member)
        return neighbors
    
    def getTooClose(self,memberList):
        result=[]
        for member in memberList:
            if not member==self:
                if self.getDistTo(member)<=self.personalSpace:
                    result.append(member)
        return result
            
    def getDistTo(self,member):
        return hypot(self.pos[0]-member.pos[0],self.pos[1]-member.pos[1])
        