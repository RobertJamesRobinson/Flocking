'''
Created on Feb 12, 2012

@author: robert
'''
from math import radians,cos,sin,degrees,atan2,hypot

class Vector(object):
    '''
    classdocs
    '''
    direction=None
    magnitude=None

    def __init__(self,direction,magnitude=None):
        '''
        Constructor
        '''
        if isinstance(direction,(float,int)) and isinstance(magnitude,(float,int)):
            self.direction=float(direction)
            self.magnitude=float(magnitude)
        elif isinstance(direction,(tuple,list)):
            tmpVect=self.vectorfy(direction)
            self.direction=tmpVect.direction
            self.magnitude=tmpVect.magnitude
        
    def __len__(self):
        return self.magnitude
    
    def normalise(self):
        result=Vector(self.direction,1)
        return result.plot()
    
    def norm(self):
        self.magnitude=1
    
    def __str__(self):
        pnt=self.plot()
        return "Direction: %0.2f, Magnitude: %0.2f, X: %0.2f, Y: %0.2f" % (self.direction,self.magnitude,pnt[0],pnt[1])
    
    def __setattr__(self,name,value):
        self.__dict__[name]=value
        if name=='direction':
            while self.direction>=360:
                self.direction-=360
            while self.direction<0:
                self.direction+=360
    def __mul__(self,other):
        if isinstance(other,(int,float)):
            return Vector(self.direction,self.magnitude*other)
    def __imul__(self,other):
        if isinstance(other,(int,float)):
            return Vector(self.direction,self.magnitude*other)
    def __div__(self,other):
        if isinstance(other,(int,float)):
            return Vector(self.direction,self.magnitude/other)
    def __idiv__(self,other):
        if isinstance(other,(int,float)):
            return Vector(self.direction,self.magnitude/other)
        
       
    def __iadd__(self,other):
        if isinstance(other,Vector):
            thisPoint=self.plot()
            otherPoint=self.plot(other)
            newPoint=thisPoint[0]+otherPoint[0],thisPoint[1]+otherPoint[1]
            return self.vectorfy(newPoint)
        
        elif isinstance(other,(tuple,list)):
            thisPoint=self.plot()
            otherPoint=other
            newPoint=thisPoint[0]+otherPoint[0],thisPoint[1]+otherPoint[1]
            return self.vectorfy(newPoint)
        
        elif isinstance(other,(int,float)):
            return Vector(self.direction,self.magnitude+other)
            
    def __add__(self,other):
        if isinstance(other,Vector):
            thisPoint=self.plot()
            otherPoint=self.plot(other)
            newPoint=thisPoint[0]+otherPoint[0],thisPoint[1]+otherPoint[1]
            return self.vectorfy(newPoint)
        
        elif isinstance(other,(tuple,list)):
            thisPoint=self.plot()
            otherPoint=other
            newPoint=thisPoint[0]+otherPoint[0],thisPoint[1]+otherPoint[1]
            return self.vectorfy(newPoint)
        
        elif isinstance(other,(int,float)):
            return Vector(self.direction,self.magnitude+other)
        
    def __isub__(self,other):
        if isinstance(other,Vector):
            thisPoint=self.plot()
            otherPoint=self.plot(other)
            newPoint=thisPoint[0]-otherPoint[0],thisPoint[1]-otherPoint[1]
            return self.vectorfy(newPoint)
        
        elif isinstance(other,(tuple,list)):
            thisPoint=self.plot()
            otherPoint=other
            newPoint=thisPoint[0]-otherPoint[0],thisPoint[1]-otherPoint[1]
            return self.vectorfy(newPoint)
        
        elif isinstance(other,(int,float)):
            return Vector(self.direction,self.magnitude-other)
    
    def diff(self,other):
        return (self.direction+1000)-(other.direction+1000)
        
    def __sub__(self,other):
        if isinstance(other,Vector):
            thisPoint=self.plot()
            otherPoint=self.plot(other)
            newPoint=thisPoint[0]-otherPoint[0],thisPoint[1]-otherPoint[1]
            return self.vectorfy(newPoint)
        
        elif isinstance(other,(tuple,list)):
            thisPoint=self.plot()
            otherPoint=other
            newPoint=thisPoint[0]-otherPoint[0],thisPoint[1]-otherPoint[1]
            return self.vectorfy(newPoint)
        
        elif isinstance(other,(int,float)):
            return Vector(self.direction,self.magnitude-other)    
    
    def plot(self,vector=None):
        if vector==None:
            vect=self.direction,self.magnitude
        else:
            vect=vector.direction,vector.magnitude
        x=cos(radians(vect[0]))*vect[1]
        y=sin(radians(vect[0]))*vect[1]
        return x,y
    
    def vectorfy(self,point):
        dirn=degrees(atan2(point[1],point[0]))
        mag=hypot(point[0],point[1])
        return Vector(dirn,mag)