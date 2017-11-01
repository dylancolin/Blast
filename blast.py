import pygame
from random import randint
import math, time

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 22)
myfont2 = pygame.font.SysFont('Comic Sans MS', 14)

ok = True
run = False
BLUE=(0,0,255)
RED=(255,0,0)
PBUL_COLOR=(172,233,67)
CBUL_COLOR=(193,70,140)
speed=2
bulspeed=3
dodge_speed = 6
clock = pygame.time.Clock()

obst = []
pbullet = [0,0,0,0,0]
cbullet = [0,0,0,0,0]
pball=[10,50]
cball=[390,250]

screen.fill((0, 0, 0))


def draw_arena():
    global obst, pbullet, cbullet, pball, cball, screen, speed, bulspeed
    
    if len(obst) == 0:
        for i in range(15):
            if randint(0, 1) == 0:
                x = randint(50,350)
                y = randint(20,240)
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(x,y,0,40))
                obst.append([1,x,y])
            else:
                x = randint(50,300)
                y = randint(20,280)
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(x,y,40,0))
                obst.append([2,x,y])
    else:
        for i in range(15):
            if obst[i][0] == 1:
                x = obst[i][1]
                y = obst[i][2]
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(x,y,0,40))
            else:
                x = obst[i][1]
                y = obst[i][2]
                pygame.draw.rect(screen, (255,255,255), pygame.Rect(x,y,40,0))


def obst_clash(px,py):
    ok=1
    global obst, pbullet, cbullet, pball, cball, screen, speed, bulspeed
    for i in range(15):
        if obst[i][0]==2 and px+5>=obst[i][1] and px-5<=obst[i][1]+40 and obst[i][2]>=py-5 and obst[i][2]<=py+5:
            ok=0
        elif obst[i][0]==1 and py+5>=obst[i][2] and py-5<=obst[i][2]+40 and obst[i][1]>=px-5 and obst[i][1]<=px+5:
            ok=0
    if px-5>=0 and px+5<=400 and py-5>=0 and py+5<=300 and ok==1:
        return False
    else: return True

def bullet_collision(q):
    global obst, pbullet, cbullet, pball, cball, screen, speed, bulspeed

    if q=="pbullet":
        bul = pbullet
    else:
        bul = cbullet

    px=bul[3]
    py=bul[4]
    ok=1
    tempx=(bul[1]-bul[3])
    tempy=(bul[2]-bul[4])
    if tempx > bulspeed: tempx=bulspeed
    if tempy > bulspeed: tempy=bulspeed
    nxt_x = bul[3]-tempx
    nxt_y = bul[4]-tempy
    
    for i in range(15):
        if obst[i][0]==2 and px+5>=obst[i][1] and px-5<=obst[i][1]+40 and obst[i][2]>=py-5 and obst[i][2]<=py+5:
            ok=2
            break
        elif obst[i][0]==1 and py+5>=obst[i][2] and py-5<=obst[i][2]+40 and obst[i][1]>=px-5 and obst[i][1]<=px+5:
            ok=3
            break

    if ok==2:
        nxt_x = bul[3]-tempx
        nxt_y = bul[2]
    elif ok==3:
        nxt_y = bul[4]-tempy
        nxt_x = bul[1]
    elif ok==1 and (px-5<=0 or px+5>=400 or py-5<=0 or py+5>=300):
        if q=="pbullet": pbullet[0] = 0
        else: cbullet[0] = 0
        return "deleted"
    
    if q=="pbullet": pbullet=[pbullet[0],pbullet[3],pbullet[4],nxt_x,nxt_y]
    else: cbullet=[cbullet[0],cbullet[3],cbullet[4],nxt_x,nxt_y]
    return "ok"

def rect_collision(x1,x2,y1,y2,w1,w2,h1,h2):
    if x1 >= x2 and x1 <= x2 + w2 or x1 + w1 >= x2 and x1 + w1 <= x2 + w2:
        if y1 >= y2 and y1 <= y2 + h2 or y1 + h1 >= y2 and y1 + h1 <= y2 + h2:
            return True

def calc_dist(x1,y1,x2,y2):
    #check if obst_clash if yes put dist high
    dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    if obst_clash(x1,y1): dist=699
    return dist

def slope(x1,y1,x2,y2):
    if x1==x2:
        return 999
    return (y2-y1)/(x2-x1)

def bul_simulate(x1,y1):
    global obst, pbullet, cbullet, pball, cball, screen, speed, bulspeed
    costs=[]
    for i in [-10,0,10]:
        for j in [-10,0,10]:
            costs.append([calc_dist(x1+i,y1+j,pball[0],pball[1]),i,j])

    costs=sorted(costs, key=lambda cost: cost[0])
    return [costs[0][0],costs[0][1],costs[0][2]]

def cpu_move():
    global obst, pbullet, cbullet, pball, cball, screen, speed, bulspeed

    if pbullet[0]==1 and slope(cball[0],cball[1],pbullet[3],pbullet[4])==slope(cball[0],cball[1],pbullet[1],pbullet[2]) and calc_dist(cball[0],cball[1],pbullet[3],pbullet[4])<calc_dist(cball[0],cball[1],pbullet[1],pbullet[2]):
        if slope(cball[0]-dodge_speed,cball[1],pbullet[3],pbullet[4])!=slope(cball[0]-dodge_speed,cball[1],pbullet[1],pbullet[2]) and not obst_clash(cball[0]-dodge_speed,cball[1]):
            cball[0]-=dodge_speed
        elif slope(cball[0]+dodge_speed,cball[1],pbullet[3],pbullet[4])!=slope(cball[0]+dodge_speed,cball[1],pbullet[1],pbullet[2]) and not obst_clash(cball[0]+dodge_speed,cball[1]):
            cball[0]+=dodge_speed
        elif slope(cball[0],cball[1]-dodge_speed,pbullet[3],pbullet[4])!=slope(cball[0],cball[1]-dodge_speed,pbullet[1],pbullet[2]) and not obst_clash(cball[0],cball[1]-dodge_speed):
            cball[1]-=dodge_speed
        elif slope(cball[0],cball[1]+dodge_speed,pbullet[3],pbullet[4])!=slope(cball[0],cball[1]+dodge_speed,pbullet[1],pbullet[2]) and not obst_clash(cball[0],cball[1]+dodge_speed):
            cball[1]+=dodge_speed
        else:
            txy=randint(0,1)
            if randint(0,1)==0:
                cball[txy]-=speed
            else:
                cball[txy]+=speed

    elif cbullet[0] == 0:
        bposs = [] 
        bposs.append([bul_simulate(cball[0],cball[1]),0,0])
        bposs.append([bul_simulate(cball[0]-speed,cball[1]),-speed,0])
        bposs.append([bul_simulate(cball[0]+speed,cball[1]),speed,0])
        bposs.append([bul_simulate(cball[0],cball[1]-speed),0,-speed])
        bposs.append([bul_simulate(cball[0],cball[1]+speed),0,speed])
        bposs=sorted(bposs, key=lambda posibilities: posibilities[0][0])
        
        cball[0]+=bposs[0][1]
        cball[1]+=bposs[0][2]
        cbullet = [1,cball[0],cball[1],cball[0]+bposs[0][0][1],cball[1]+bposs[0][0][2]]                      
    
    else:
        dist=[]
        dist.append([calc_dist(cball[0],cball[1],pball[0],pball[1]),0,0])
        dist.append([calc_dist(cball[0]-speed,cball[1],pball[0],pball[1]),-speed,0])
        dist.append([calc_dist(cball[0]+speed,cball[1],pball[0],pball[1]),speed,0])
        dist.append([calc_dist(cball[0],cball[1]-speed,pball[0],pball[1]),0,-speed])
        dist.append([calc_dist(cball[0],cball[1]+speed,pball[0],pball[1]),0,speed])
        dist=sorted(dist, key=lambda distances: distances[0])

        for i in dist:
            if i[0] != 699:
                cball[0]+=dist[0][1] 
                cball[1]+=dist[0][2]
                break


while ok:
    if run:
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,400,300))
        draw_arena()
        pygame.draw.circle(screen,BLUE,pball,5,0)
        pygame.draw.circle(screen,RED,cball,5,0)

        if pbullet[0]==1:
            if bullet_collision("pbullet") == "ok": 
                pygame.draw.circle(screen,PBUL_COLOR,[pbullet[3],pbullet[4]],5,0)

        if cbullet[0]==1:
            if bullet_collision("cbullet") == "ok": 
                pygame.draw.circle(screen,CBUL_COLOR,[cbullet[3],cbullet[4]],5,0)

        #collision with bullet
        if (cbullet[0]==1) and rect_collision(pball[0]-5,cbullet[3]-5,pball[1]-5,cbullet[4]-5,10,10,10,10):
            run=False
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,400,300))
            textsurface = myfont.render('You LOST !', False, (255,255,255))
            screen.blit(textsurface,(10,20))
            pygame.display.flip()
            clock.tick(60)
            time.sleep(2)
            print("YOU LOST !")
        elif (pbullet[0]==1) and rect_collision(cball[0]-5,pbullet[3]-5,cball[1]-5,pbullet[4]-5,10,10,10,10):
            run=False
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,400,300))
            textsurface = myfont.render('You WON !', False, (255,255,255))
            screen.blit(textsurface,(10,20))
            pygame.display.flip()
            clock.tick(60)
            time.sleep(2)
            print("YOU WON !")
        else:
            cpu_move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                ok = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pass
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
          if pressed[pygame.K_UP] and pressed[pygame.K_LEFT] and not obst_clash(pball[0]-bulspeed,pball[1]-bulspeed):
              pbullet = [1,pball[0],pball[1],pball[0]-bulspeed,pball[1]-bulspeed]
          elif pressed[pygame.K_UP] and pressed[pygame.K_RIGHT] and not obst_clash(pball[0]+bulspeed,pball[1]-bulspeed):
              pbullet = [1,pball[0],pball[1],pball[0]+bulspeed,pball[1]-bulspeed]
          elif pressed[pygame.K_DOWN] and pressed[pygame.K_LEFT] and not obst_clash(pball[0]-bulspeed,pball[1]+bulspeed):
              pbullet = [1,pball[0],pball[1],pball[0]-bulspeed,pball[1]+bulspeed]
          elif pressed[pygame.K_DOWN] and pressed[pygame.K_RIGHT] and not obst_clash(pball[0]+bulspeed,pball[1]+bulspeed):
              pbullet = [1,pball[0],pball[1],pball[0]+bulspeed,pball[1]+bulspeed]
          elif pressed[pygame.K_UP] and not obst_clash(pball[0],pball[1]-bulspeed):
              pbullet = [1,pball[0],pball[1],pball[0],pball[1]-bulspeed]
          elif pressed[pygame.K_DOWN] and not obst_clash(pball[0],pball[1]+bulspeed):
              pbullet = [1,pball[0],pball[1],pball[0],pball[1]+bulspeed]
          elif pressed[pygame.K_LEFT] and not obst_clash(pball[0]-bulspeed,pball[1]):
              pbullet = [1,pball[0],pball[1],pball[0]-bulspeed,pball[1]]
          elif pressed[pygame.K_RIGHT] and not obst_clash(pball[0]+bulspeed,pball[1]):
              pbullet = [1,pball[0],pball[1],pball[0]+bulspeed,pball[1]]
              
        if pressed[pygame.K_UP] and not obst_clash(pball[0],pball[1]-speed):
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(pball[0]-5,pball[1]-5,10,10))
            pball[1]-=speed
            pygame.draw.circle(screen,BLUE,pball,5,0) 
        elif pressed[pygame.K_DOWN] and not obst_clash(pball[0],pball[1]+speed):
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(pball[0]-5,pball[1]-5,10,10))
            pball[1]+=speed
            pygame.draw.circle(screen,BLUE,pball,5,0)
        elif pressed[pygame.K_LEFT] and not obst_clash(pball[0]-speed,pball[1]):
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(pball[0]-5,pball[1]-5,10,10))
            pball[0]-=speed
            pygame.draw.circle(screen,BLUE,pball,5,0)
        elif pressed[pygame.K_RIGHT] and not obst_clash(pball[0]+speed,pball[1]):
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(pball[0]-5,pball[1]-5,10,10))
            pball[0]+=speed
            pygame.draw.circle(screen,BLUE,pball,5,0)

        pygame.display.flip()
        clock.tick(60)
    
    else:
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,400,300))
        
        textsurface = myfont.render('BLAST', False, (65,176,255))
        screen.blit(textsurface,(10,20))
        
        textsurface = myfont.render('Instructions', False, (255,255,255))
        screen.blit(textsurface,(10,70))
        pygame.draw.circle(screen,BLUE,[10,130],5,0)
        pygame.draw.circle(screen,RED,[10,150],5,0)
        pygame.draw.circle(screen,PBUL_COLOR,[170,130],5,0)
        pygame.draw.circle(screen,CBUL_COLOR,[170,150],5,0)
        textsurface = myfont2.render('Player', False, (255,255,255))
        screen.blit(textsurface,(20,120))
        textsurface = myfont2.render('CPU', False, (255,255,255))
        screen.blit(textsurface,(20,140))
        textsurface = myfont2.render('Player Bullet', False, (255,255,255))
        screen.blit(textsurface,(190,120))
        textsurface = myfont2.render('CPU Bullet', False, (255,255,255))
        screen.blit(textsurface,(190,140))
        textsurface = myfont2.render('Player Movement : Arrow Keys | Shoot Bullet with "A"', False, (255,255,255))
        screen.blit(textsurface,(10,180))        
        textsurface = myfont2.render('Win By Hitting the Bullet to Opponent !', False, (255,255,255))
        screen.blit(textsurface,(10,200))    

        pygame.draw.rect(screen, [255, 0, 0], pygame.Rect(10, 240, 5, 50))
        textsurface = myfont.render('Press P to play', False, (255,255,255))
        screen.blit(textsurface,(25,240))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                ok = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_p]:
            run = True
            pbullet = [0,0,0,0,0]
            cbullet = [0,0,0,0,0]
            pball=[10,50]
            cball=[390,250]
            obst=[]            

        pygame.display.flip()
        clock.tick(60)