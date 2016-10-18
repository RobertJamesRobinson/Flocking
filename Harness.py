'''
Created on Feb 12, 2012

@author: robert
'''
import pygame
from random import randint
from math import hypot
from time import sleep
from Vector import Vector
from FlockMember import FlockMember
from FlockController import FlockController




if __name__ == '__main__':
    mems=[]
    for i in range(60):
        maxSpeed=randint(15,30)
        nradius=randint(150,200)
        pspace=nradius*.50
        mems.append(FlockMember({'pos':(randint(100,700),randint(100,700)),'vector':Vector(randint(0,359),3),'maxTurnRate':5,'maxSpeed':maxSpeed,'neighborhoodRadius':nradius,'personalSpace':pspace,'cohesion':2.0,'separation':1.0,'alignment':0.5}))
    flock=FlockController({'bounds':(1800,1000),'members':mems})
    pygame.init()
    screen=pygame.display.set_mode((1800,1000))
    running=True
    render=False
    debug=False
    while running:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                running=False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                debug=not debug
                
            if event.type==pygame.QUIT:
                running=False
                
            if event.type==pygame.MOUSEBUTTONDOWN:
                tmpX=flock.members[0].pos[0]
                tmpY=flock.members[0].pos[1]
                bestDist=hypot(tmpX-event.pos[0],tmpY-event.pos[1])
                bestIndex=0
                for key in range(1,len(flock.members)):
                    tmpX=flock.members[key].pos[0]
                    tmpY=flock.members[key].pos[1]
                    dist=hypot(tmpX-event.pos[0],tmpY-event.pos[1])
                    if dist<bestDist:
                        bestDist=dist
                        bestIndex=key
                print "Index: %i\nDirectional Vector: %s\nCohesion Vector: %s\nSeparation Vector: %s\nAlignment Vector: %s" % (bestIndex,flock.members[bestIndex].vector,flock.members[bestIndex].cVec,flock.members[bestIndex].sVec,flock.members[bestIndex].aVec)
        #sleep(1)            
        flock.tick()
        render=True
        if render:
            screen.fill((0,0,0))
            for member in flock.members:
                thisPos=int(member.pos[0]),int(member.pos[1])
                #pygame.draw.circle(screen, (255,255,255), thisPos, 2)
                if debug:
                    pygame.draw.circle(screen,(255,255,0),thisPos,member.neighborhoodRadius,1)
                    pygame.draw.circle(screen,(255,0,0),thisPos,int(member.personalSpace),1)
                    
                    direction=member.vector.plot()
                    direction=direction[0]*30+member.pos[0],direction[1]*30+member.pos[1]
                    
                    cohesion=member.cVec.plot()
                    cohesion=cohesion[0]*30+member.pos[0],cohesion[1]*30+member.pos[1]
                    
                    separation=member.sVec.plot()
                    separation=separation[0]*30+member.pos[0],separation[1]*30+member.pos[1]
                    
                    alignment=member.aVec.plot()
                    alignment=alignment[0]*30+member.pos[0],alignment[1]*30+member.pos[1]
                    
                    pygame.draw.line(screen, (0,255,255), thisPos, direction)
                    pygame.draw.line(screen, (255,0,0), thisPos, cohesion)
                    pygame.draw.line(screen, (0,255,0), thisPos, separation)
                    pygame.draw.line(screen, (0,0,255), thisPos, alignment)
                
                #draw the boid
                front=Vector(0,10)
                bl=Vector(225,10)
                br=Vector(135,10)
                front.direction+=member.vector.direction
                bl.direction+=member.vector.direction
                br.direction+=member.vector.direction
                fp=front.plot()
                blp=bl.plot()
                brp=br.plot()
                fp=fp[0]+thisPos[0],fp[1]+thisPos[1]
                blp=blp[0]+thisPos[0],blp[1]+thisPos[1]
                brp=brp[0]+thisPos[0],brp[1]+thisPos[1]
                
                pygame.draw.polygon(screen, (255,255,255), (fp,blp,brp))
            
            pygame.display.flip()
            render=False
    pygame.quit()
        
