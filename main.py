#THIS IS A GAME CALLED "COLOR GENOCIDE"
#YOU PLAY AS A QUADRI-POLAR GUY WHO CAN CHANGE COLORS
#DEPENDING ON HIS PERSONALITY, YOU GET DIFFERENT STATS
#YOU CAN CHANGE HIS COLOR/PERSONALITY BY PRESSING X
#note: very inspired by Undertale

import os
from pygame import *
from time import *
from copy import deepcopy
from math import *
from random import *
os.environ['SDL_VIDEO_WINDOW_POS'] = '70,25'
#----METADATA----#
__name__ = "Color Genocide"
__author__ = "Yttrium Z (You Zhou)"
__purpose__ = "Codeday"
__date__ = "February 13 - 14, 2016"
#----SETUP----#
screen = display.set_mode((1200,736))
gameover = False
try:
    display.set_icon(image.load("images/icon.png"))
except:
    pass
display.set_caption("COLOR GENOCIDE BY YTTRIUM Z - KILL EVERYTHING... WITH STYLE","COLOR GENOCIDE")
#----FONTS----#
font.init()
titleFont = font.SysFont("papyrus",50)
papyrus = font.SysFont("papyrus",20)
lucidaConsole = font.SysFont("lucidaconsole",20)
msgFont = lucidaConsole
smallfont = font.SysFont("lucidaconsole",12)
#----LOADING SCREEN----#
screen.blit(titleFont.render("YTTRIUM-Z PREZENTS...",True,(255,255,255)),(250,305))
display.flip()
screen.fill((0,0,0))
#----SOUND----#
init()
mixer.init()
mainBackMusic = mixer.Sound("music/mus_waterfall.ogg")
instructMusic = mixer.Sound("music/mus_yourbestfriend_3.ogg")
gameoverMusic = mixer.Sound("music/mus_toomuch.ogg")
bossMusic = mixer.Sound("music/mus_undyneboss.ogg")
victoryMusic = mixer.Sound("music/mus_town.ogg")
textMusic = mixer.Sound("music/mus_papyrusboss.ogg")
deadBossEffect = mixer.Sound("music/mus_churchbell.ogg")
hiteffect = mixer.Sound("sound/snd_flameloop.ogg")
enhiteffect = mixer.Sound("sound/snd_bombsplosion.ogg")
healeffect = mixer.Sound("sound/snd_mushroomdance.ogg")
LVeffect = mixer.Sound("sound/snd_ballchime.ogg")
transformEffect = mixer.Sound("music/mus_sfx_a_grab.ogg")
backMusic = mixer.Channel(0)
effects = mixer.Channel(1)
backMusic.play(instructMusic,-1)
#----COLORS----#
RED = (255,0,0,255)
GREEN = (0,255,0,255)
BLUE = (0,0,255,255)
YELLOW = (255,255,0,255)
CYAN = (0,255,255,255)
MAGENTA = (255,0,255,255)
BLACK = (0,0,0,255)
WHITE = (255,255,255,255)
GREY = (123,123,123,255)
BLUE_GREY = (65,65,80,255)
#----IMAGES----#
normalFrisk = image.load("images/frisk.png")
movingNormalFrisk = image.load("images/movingFrisk.png")
attackingNormalFrisk = image.load("images/attackingFrisk.png")
yellowFrisk = image.load("images/yellowFrisk.png")
movingYellowFrisk = image.load("images/movingYellowFrisk.png")
attackingYellowFrisk = image.load("images/attackingYellowFrisk.png")
redFrisk = image.load("images/redFrisk.png")
movingRedFrisk = image.load("images/movingRedFrisk.png")
attackingRedFrisk = image.load("images/attackingRedFrisk.png")
blueFrisk = image.load("images/blueFrisk.png")
movingBlueFrisk = image.load("images/movingBlueFrisk.png")
attackingBlueFrisk = image.load("images/attackingBlueFrisk.png")
froggySprite = image.load("images/froggy.png")
movingFroggy = image.load("images/movingFroggy.png")
bucketHeadSprite = image.load("images/bucketHead.png")
movingBucketHead = image.load("images/movingBucketHead.png")
pyrantSprite = image.load("images/pyrAnt.png")
movingPyrant = image.load("images/movingPyrant.png")
frogKing = image.load("images/frogKing.png")
deadFrogKing = image.load("images/deadFrogKing.png")
enhancedPyrant = image.load("images/enhancedPyrant.png")
movingEnhancedPyrant = image.load("images/movingEnhancedPyrant.png")
goatdog = image.load("images/goatdog.png")
healPoint = image.load("images/healpoint.png")
#----INSTRUCTIONS SCREEN----#
instructions = True
screen.blit(lucidaConsole.render("Arrow keys to move",True,WHITE),(450,280))
screen.blit(lucidaConsole.render("Press Z to attack",True,WHITE),(450,320))
screen.blit(lucidaConsole.render("Press X to transform into other colors",True,WHITE),(450,360))
screen.blit(lucidaConsole.render("Yellow Stars heal",True,YELLOW),(450,400))
screen.blit(lucidaConsole.render("Dark Blue spots are traversable",True,BLUE_GREY),(450,440))
screen.blit(lucidaConsole.render("Anything else is an enemy",True,GREEN),(450,480))
screen.blit(lucidaConsole.render("Ruthlessly murder everything",True,RED),(450,520))
screen.blit(lucidaConsole.render("[Any key or click to continue]",True,WHITE),(425,600))
screenBuffer = screen.copy()
while instructions:
    for e in event.get():
        if e.type == QUIT:
            instructions = False
            quit()
        if e.type in [KEYDOWN,MOUSEBUTTONDOWN]:
            instructions = False
            backMusic.stop()
            backMusic.play(mainBackMusic,-1)
    screen.blit(screenBuffer,(0,0))
    if 0.05 < time()%2 < 0.75 or 0.85 < time()%2 < 1.95:
        screen.blit(titleFont.render("COLOR GENOCIDE",True,RED),(320,100))
    if time()%0.5 < 0.25:
        screen.blit(healPoint,(400,383))
    else:
        screen.blit(transform.flip(healPoint,True,True),(400,383))
    display.flip()
#----FUNCTIONS----#
def touching(en,rect=None):
    'check if two rects touch'
    if rect == None:
        friskRect = Rect(chara.x,chara.y,chara.width,chara.height)
    else:
        friskRect = rect #sets friskRect to the atkRect used to call this function
    enRect = Rect(en.x,en.y,en.width,en.height)
    friskCorners = getCorners(friskRect)
    enCorners = getCorners(enRect)
    touching = False
    for c in friskCorners:
        #checks if frisk's corners touch enemy
        if enRect.collidepoint(c):
            touching = True
            break
    for c in enCorners:
        #checks if enemy's corners touch frisk
        if friskRect.collidepoint(c):
            touching = True
            break
    return touching 
def getCorners(unit):
    "returns unit's corners as a list"
    return [(unit.x,unit.y),(unit.x,unit.y+unit.height),(unit.x+unit.width,unit.y),(unit.x+unit.width,unit.y+unit.height)]
def changeMsg(newmsg,newfont=lucidaConsole):
    'change the global variable msg'
    global msg,msgFont
    msg = newmsg
    msgFont = newfont #new font
#----CLASSES----#
class Frisk():
    'The main character'
    def __init__(self):
        'Initialize Frisk class'
        self.x,self.y = 1,31
        self.width,self.height = 100,150
        self.atkRect = Rect(self.width,self.height//2,45,self.height//2) #attack rect for normal Frisk
        self.mode = 'normal'
        self.sprite = normalFrisk
        self.movingSprite = movingNormalFrisk
        self.attackingSprite = attackingNormalFrisk
        self.moving = False
        self.dir = 1 #direction Frisk is facing 1 = right, 0 = left
        self.damaged = 0 #damage timer - doesn't allow frisk to be hurt too much within 100 milliseconds
        self.attacking = 0 #attack timer
        self.modes = ["normal","yellow","red","blue"] #modes of frisk
        #STATS
        self.maxhp = 10
        self.atkspd = 0.5 #atk speed in seconds
        self.hp = 10
        self.atk = 1
        self.defen = 1
        self.spd = 3
        self.xp = 0
        self.lv = 1
        self.watk = 3 #weapon attack
        self.adef = 0 #armor defense
    def draw(self,screen):
        'Draw Frisk'
        offset = -100 if self.mode == "blue" and not self.dir else 0 #offset for drawing (-100 if frisk is blue and facing left)
        if time() - self.damaged < 1 and time()%0.2 < 0.1:
            #if we are getting hurt, we imitate a flashing effect
            return 0
        if time() - self.attacking < self.atkspd/2:
            #draws attacking sprite if it has been a second since the user pressed attack
            screen.blit(self.attackingSprite,(self.x-self.atkRect.width+self.atkRect.width*self.dir,self.y))
        elif self.moving and time()%0.5 < 0.25:
            screen.blit(self.movingSprite,(self.x+offset,self.y))
        else:
            screen.blit(self.sprite,(self.x+offset,self.y))
    def move(self,coords):
        'Move Frisk'
        #flips sprites if chara changed directions
        if (not self.dir and coords[0] > self.x) or (self.dir and coords[0] < self.x):
            self.sprite = transform.flip(self.sprite,True,False)
            self.movingSprite = transform.flip(self.movingSprite,True,False)
            self.attackingSprite = transform.flip(self.attackingSprite,True,False)
        self.moving = True
        oldx,oldy = self.x,self.y #old x and y
        self.x,self.y = coords
        corners = getCorners(self)
        for c in corners:
            for r in moveable:
                if r.collidepoint(c):
                    break #if we touched a moveable rect, we are all good
            else:
                self.x,self.y = oldx,oldy
                return 0 #we don't move if we didn't touch one
        for en in enemies:
            if touching(en):
                self.x,self.y = oldx,oldy #doesn't allow movement through enemies
                break
    def attack(self):
        'attack with Frisk'
        if time() - self.attacking < self.atkspd:
            #attacking lasts atkspd seconds - if user presses attack twice within atkspd seconds it returns method to cancel
            return 0
        atkRect = Rect(self.atkRect.x,self.atkRect.y,self.atkRect.width,self.atkRect.height)
        atkRect.x += self.x
        atkRect.y += self.y #sets attack rect co-ords
        if not self.dir:
            #if we are facing to the left we negative the atkRect width
            atkRect.x = self.x
            atkRect.width = -1*atkRect.width
            atkRect.normalize()
        self.attacking = time()
        for en in enemies:
            if touching(en,atkRect):
                #checks if enemy is touching the attack rect
                if self.atk+self.watk-en.defen > 0:
                    changeMsg("You hurt "+en.name+"! How rude!")
                    effects.play(hiteffect)
                else:
                    changeMsg("You tried to hurt "+en.name+" but you're too weak in this mode.")
                en.setHp(min(en.hp,en.hp-self.atk-self.watk+en.defen)) #sets enemies' hp to be at most enemies current health
                if en.hp == 0:
                    changeMsg(en.name+" died... :(")
                    self.gainXp(20*en.lv) #gains 20 xp multiplied by enemy's level
    def setHp(self,hp):
        'sets Frisk hp'
        global gameover
        self.hp = round(min(max(0,hp),self.maxhp),2) #limits hp to be between 0 and maxhp
        if self.hp == 0:
            gameover = True #if Frisk is out of HP, it is game over
            backMusic.stop()
            backMusic.play(gameoverMusic,-1)
    def gainXp(self,xp):
        self.xp += xp
        while self.xp >= 100*self.lv:
            self.xp -= self.lv*100
            self.lv += 1
            self.atk += 1
            self.defen += 1
            self.maxhp += 3
            changeMsg("LV INCREASED TO "+str(self.lv)+"!")
            effects.queue(LVeffect)
    def changeMode(self,mode):
        'change to a mode'
        self.mode = mode
        if self.mode == "normal":
            #changes to Normal
            self.watk = 3
            self.adef = 0
            self.spd = 3
            self.sprite = normalFrisk
            self.movingSprite = movingNormalFrisk
            self.attackingSprite = attackingNormalFrisk
            self.atkRect = Rect(self.width,self.height//2,45,self.height//2) #attack rect for normal Frisk
            self.atkspd = 0.5
        if self.mode == "yellow":
            #changes to Yellow
            self.watk = 6
            self.adef = 2
            self.spd = 1
            self.sprite = yellowFrisk
            self.movingSprite = movingYellowFrisk
            self.attackingSprite = attackingYellowFrisk
            self.atkRect = Rect(self.width,self.height,8,29) #attack rect for yellow Frisk
            self.atkspd = 0.8
        if self.mode == "red":
            #changes to Red
            self.watk = 4
            self.adef = 3
            self.spd = 2
            self.sprite = redFrisk
            self.movingSprite = movingRedFrisk
            self.attackingSprite = attackingRedFrisk
            self.atkRect = Rect(self.width,0,10,self.height+22) #attack rect for red Frisk
            self.atkspd = 0.6
        if self.mode == "blue":
            #changes to Blue
            self.watk = 3
            self.adef = 1
            self.spd = 2
            self.sprite = blueFrisk
            self.movingSprite = movingBlueFrisk
            self.attackingSprite = attackingBlueFrisk
            self.atkRect = Rect(self.width,self.height//2,100,7)
            self.atkspd = 0.3
        effects.stop()
        effects.play(transformEffect)
        #flips sprites if Frisk is facing left
        if not self.dir:
            self.sprite = transform.flip(self.sprite,True,False)
            self.movingSprite = transform.flip(self.movingSprite,True,False)
            self.attackingSprite = transform.flip(self.attackingSprite,True,False)
    def reset(self):
        'Reset Frisk'
        #resets Chara's booleans so that uh, they can be altered
        self.moving = False
class Enemy():
    'enemies'
    def __init__(self,name,sprite,movingsprite,x=0,y=0,width=100,height=100,maxhp=10,atk=1,defen=0,spd=1,lv=1):
        'Initalize the Enemy class'
        self.x,self.y = x,y
        self.width,self.height = width,height
        self.sprite = sprite
        self.movingsprite = movingsprite
        self.name = name
        self.moving = False
        self.damaged = 0
        self.attacking = 0
        #STATS
        self.maxhp = maxhp
        self.lv = lv
        self.hp = maxhp
        self.atk = atk
        self.defen = defen
        self.spd = spd
        self.boss = False
    def draw(self,screen):
        'draw enemy'
        if time() - self.damaged < 1 and time()%0.2 < 0.1 and self.hp > 0:
            #if we are getting hurt, we imitate a flashing effect
            return 0
        #if time() - self.attacking < self.atkspd/2:
        #    #draws attacking sprite if it has been a second since the enemy attacked
        #    screen.blit(self.attackingSprite,(self.x-self.atkRect.width+self.atkRect.width*self.dir,self.y))
        if self.moving and time()%0.5 < 0.25 and self.hp > 0:
            screen.blit(self.movingsprite,(self.x,self.y))
        else:
            screen.blit(self.sprite,(self.x,self.y))
        draw.rect(screen,RED,(self.x,self.y+self.height,self.width,3))
        draw.rect(screen,GREEN,(self.x,self.y+self.height,int((self.hp/self.maxhp)*self.width),3))
    def move(self,toward=True):
        'move enemy (this usually damages player)'
        dirx = (chara.x - self.x)/max(1,abs(chara.x-self.x))
        diry = (chara.y - self.y)/max(1,abs(chara.y - self.y))
        if not toward:
            #reverses direction when not moving toward
            dirx *= -1
            diry *= -1
        newx = self.x+dirx*self.spd
        newy = self.y+diry*self.spd
        oldx,oldy = self.x,self.y #old co-ords
        self.x,self.y = newx,newy #changes co-ords for calculation purposes
        #inflicts damage to player
        if touching(self):
            if time() - chara.damaged > 1:
                #if damage timer is over
                if self.atk < 0:
                    chara.setHp(chara.hp + self.atk) #allows true damage with negative attack
                else:
                    chara.setHp(min(chara.hp,chara.hp-self.atk+chara.adef+chara.defen)) #frisk loses hp for bumping into enemies
                effects.play(enhiteffect)
                chara.damaged = time() #sets timer for damage timer
        self.x,self.y = oldx,oldy
        #HORIZONTAL MOVEMENT
        self.x = newx
        corners = getCorners(self)
        for c in corners:
            for r in moveable:
                if r.collidepoint(c):
                    break #if we touched a moveable rect, we are all good
            else:
                self.x = oldx
                break
            if len(stagechangers) > 0:
                for sc in stagechangers:
                    if not sc[0].collidepoint(c):
                        break #if we are not touched by a stage change point, we are all good (since enemies can't touch those)
                else:
                    self.x = oldx
            #CHECKS COLLISIONS
            for en in [None]+[Rect(en.x,en.y,en.width,en.height) for en in enemies if en != self]:
                if touching(self,en):
                    self.x = oldx
                    break
        #VERTICAL MOVEMENT
        self.y = newy
        corners = getCorners(self)
        for c in corners:
            for r in moveable:
                if r.collidepoint(c):
                    break #if we touched a moveable rect, we are all good
            else:
                self.y = oldy
                break
            if len(stagechangers) > 0:
                for sc in stagechangers:
                    checkrect = deepcopy(sc[0])
                    checkrect.y -= 150
                    checkrect.height += 300 #check rect is 150 more to the top and bottom of a regular stage changer to make sure mob don't block
                    if not checkrect.collidepoint(c):
                        break #if we are not touched by a stage change point, we are all good (since enemies can't touch those)
                else:
                    self.y = oldy
            #CHECKS COLLISIONS
            for en in [None]+[Rect(en.x,en.y,en.width,en.height) for en in enemies if en != self]:
                if touching(self,en):
                    self.y = oldy
                    break

        self.moving = True
    def setHp(self,hp):
        'sets Enemy HP'
        if hp < self.hp:
            self.damaged = time() #sets damage timer
        self.hp = round(min(max(0,hp),self.maxhp),1)
        if self.hp == 0:
            enemies.remove(self)
    def reset(self):
        'resets enemy'
        self.moving = False
class FrogKing(Enemy):
    'Frog King Class'
    def __init__(self,name,sprite,movingsprite,x=0,y=0,width=100,height=100,maxhp=10,atk=1,defen=0,spd=1,lv=1):
        'Initialize the Frog King'
        super(FrogKing,self).__init__(name,sprite,movingsprite,x,y,width,height,maxhp,atk,defen,spd,lv) #super init
        self.boss = True
        self.summontimer = 0
    def setHp(self,hp):
        'Set Frog King\'s HP'
        if len(enemies) > 1:
            #if there are spawns, the frog king takes no damage
            changeMsg("You must kill the Frog King's minions before you can hurt him")
            return 0
        else:
            super(FrogKing,self).setHp(hp)
            if self.hp == 0:
                #if the frogking is dead we do an animation
                screenBuffer = screen.copy()
                chara.draw(screen)
                display.flip()
                self.sprite = transform.rotate(self.sprite,90)
                self.draw(screen)
                display.flip()
                screen.blit(screenBuffer,(0,0))
                sleep(2)
                chara.draw(screen)
                display.flip()
                self.sprite = transform.rotate(self.sprite,90)
                self.draw(screen)
                display.flip()
                sleep(2)
                self.sprite = deadFrogKing
                self.draw(screen)
                display.flip()
                backMusic.stop()
                backMusic.play(deadBossEffect)
                sleep(5)
    def move(self,toward=True):
        if len(enemies) > 1:
            return 0
        #the frog king doesn't move unless he is lower than 5/6 health and if there are no spawned monsters
        if self.hp < self.maxhp/3:
            super(FrogKing,self).move(False)
        elif self.hp < self.maxhp*5/6:
            super(FrogKing,self).move()
    def summon(self):
        #summons six random mobs
        if time() - self.summontimer > 50 and len(enemies) == 1:
            #every 50 seconds Frog King spawns things
            self.x,self.y = 500,35
            self.summontimer = time()
            changeMsg("\"FIGHT FOR ME MINIONS!\"",papyrus)
            enemy_types = ['Enemy("Lesser Froggy",froggySprite,movingFroggy,*x*,*y*,100,100,10,3,2,2)',
                           'Enemy("Greater Froggy",transform.scale(froggySprite,(150,150)),transform.scale(movingFroggy,(150,150)),*x*,*y*,150,150,15,5,2,1,3)',
                           'Enemy("Equaler Froggy",transform.scale(froggySprite,(125,125)),transform.scale(movingFroggy,(125,125)),*x*,*y*,125,125,12,4,2,2,2)',
                           'Enemy("Bucket Head",bucketHeadSprite,movingBucketHead,*x*,*y*,100,150,6,4,6,1,2)',
                           'Enemy("Pyrant",pyrantSprite,movingPyrant,*x*,*y*,50,150,20,-2,0,4,3)']
            enemy_coords = [(5,35),(1000,35),(5,205),(1000,205),(5,370),(1000,369)]
            for i in range(6):
                mob = choice(enemy_types)
                x,y = enemy_coords[i]
                mob = mob.replace("*x*",str(x))
                mob = mob.replace("*y*",str(y))
                entoAdd = eval(mob)
                if touching(entoAdd):
                    continue #we do not spawn it there if it is touching Chara
                entoAdd.atk = int(entoAdd.atk*1.5) #all minions get a buff
                entoAdd.defen += 1
                enemies.append(entoAdd)
#----The Stage Class----#
class Stage():
    'The class that is essentially a floor in the game'
    def __init__(self,moveable,enemies,stagechangers,healpoints=[]):
        'initializies stage'
        self.defaultEn = enemies #default enemies
        self.moveable = moveable #moveable rects
        self.enemies = [eval(en) for en in enemies] #enemies
        self.stagechangers = stagechangers #rects that allow departure to another stage
        self.healpoints = healpoints #sets heal points
    def draw(self,screen):
        'draws stage'
        global screenBuffer        
        transurface = Surface((1200,676),SRCALPHA)
        transurface.fill((0,0,0,50))
        for i in range(50):
            screen.blit(transurface,(0,30))
            display.flip()
            sleep(0.01)
        for r in self.moveable:
            draw.rect(screen,BLUE_GREY,r) #draws all moveable rects
        screenBuffer = screen.copy()
    def reset(self):
        'resets stage to original'
        self.enemies = [eval(en) for en in self.defaultEn] #enemies back to default
#----The Healing Point----#
class HealPoint():
    'The class that allows the player to heal'
    def __init__(self,x,y):
        self.x,self.y,self.width,self.height = x,y,40,40 #sets co-ords of HealPoint
    def getRect(self):
        return Rect(self.x,self.y,self.width,self.height) #gets rect
    def draw(self,screen):
        if time()%0.5 < 0.25:
            screen.blit(healPoint,self.getRect()) #blits the heal point at the point
        else:
            screen.blit(transform.flip(healPoint,True,True),self.getRect())
#----RESTART FUNCTION----#
def restart():
    'restarts game in game overs'
    global currstage,stage,moveable,stagechangers,enemies,died,screenBuffer,bossinit,stages,savedCharaStats
    currstage = 0
    stage = stages[currstage]
    moveable = stage.moveable
    enemies = stage.enemies
    stagechangers = stage.stagechangers
    stage.draw(screen)
    draw.rect(screen,GREY,(0,0,1200,30))
    draw.rect(screen,GREY,(0,706,1200,30))
    screenBuffer = screen.copy()
    if bossinit:
        #if the boss was initialized we delete last stage and unintialize boss
        del stages[-1]
        bossinit = False
        del stages[-1].moveable[-1]
        del stages[-1].stagechangers[-1]
##    chara.hp = chara.maxhp
##    chara.x = 0
##    chara.y = 30
##    chara.dir = 1
##    chara.changeMode("normal")
##    chara.lv = 1 #CHANGE THIS LATER TO BE LEVEL WAS AT CHECK POINT (once i figure out how lol)
    chara.__init__()
    for i,k in enumerate(savedCharaStats):
        exec("chara."+k+"="+str(savedCharaStats[k]))
    chara.hp = chara.maxhp
    died += 1
    #funny text based on how much you die
    if died == 1:
        changeMsg("Nothing new... except that you died once")
    elif died < 9:
        changeMsg("Nothing new... except that you died "+str(died)+" times")
    elif died < 20:
        changeMsg("Aren't you tired of dying yet?")
    elif died < 9000:
        changeMsg("...Please try pressing [X], it might help...")
    else:
        changeMsg("Your deaths... IT'S OVER 9000!")
    backMusic.stop()
    backMusic.play(mainBackMusic,-1)
#----UNITS AND OTHER VARIABLES----#
msg = "Nothing new"
 
chara = Frisk()
#----BACKGROUND----#
draw.rect(screen,GREY,(0,0,1200,30))
draw.rect(screen,GREY,(0,706,1200,30))
#stages
stages = [Stage([Rect(0,30,400,200),Rect(300,30,200,300),Rect(200,330,600,376),Rect(500,30,750,300)],
                ['Enemy("Lesser Froggy",froggySprite,movingFroggy,350,500,100,100,10,3,2,2)',
                'Enemy("Greater Froggy",transform.scale(froggySprite,(150,150)),transform.scale(movingFroggy,(150,150)),500,500,150,150,15,5,2,1,3)'],
                [(Rect(1150,30,100,200),1,(5,30)),
                 (Rect(200,700,600,6),3,(None,38))]),
          Stage([Rect(0,30,400,200),Rect(300,30,200,300),Rect(200,330,600,376)],
                ['Enemy("Lesser Froggy",froggySprite,movingFroggy,350,500,100,100,10,3,2,2)',
                'Enemy("Equaler Froggy",transform.scale(froggySprite,(125,125)),transform.scale(movingFroggy,(125,125)),500,500,125,125,12,4,2,2,2)'],
                [(Rect(0,30,3,200),0,(1044,30)),
                 (Rect(200,700,600,6),2,(None,38))],
                [HealPoint(205,645)]),
          Stage([Rect(200,30,600,676),Rect(800,100,70,600)],
                ['Enemy("Lesser Froggy",froggySprite,movingFroggy,350,450,100,100,10,3,2,2)',
                'Enemy("Equaler Froggy",transform.scale(froggySprite,(125,125)),transform.scale(movingFroggy,(125,125)),500,440,125,125,12,4,2,2,2)',
                'Enemy("Greater Froggy",transform.scale(froggySprite,(150,150)),transform.scale(movingFroggy,(150,150)),700,430,150,150,12,5,2,1,3)'],
                [(Rect(200,30,600,6),1,(None,549)),
                 (Rect(200,703,600,3),4,(1000,38))]),
          Stage([Rect(200,30,600,676),Rect(800,100,70,600)],
                ['Enemy("Bucket Head",bucketHeadSprite,movingBucketHead,350,500,100,150,6,4,6,1,3)',
                 'Enemy("Pyrant",pyrantSprite,movingPyrant,700,250,50,150,20,-2,0,4,3)'],
                [(Rect(200,30,600,6),0,(None,549)),
                 (Rect(200,703,600,3),4,(100,38))]),
          Stage([Rect(0,30,300,50),Rect(900,30,300,50),Rect(0,60,1200,646)],
                ['Enemy("Bucket Head",bucketHeadSprite,movingBucketHead,350,500,100,150,6,4,6,1,3)',
                 'Enemy("Pyrant",pyrantSprite,movingPyrant,700,250,50,150,20,-2,0,4,3)',
                 'Enemy("Lesser Froggy",froggySprite,movingFroggy,0,300,100,100,10,3,2,2)',
                 'Enemy("Equaler Froggy",transform.scale(froggySprite,(125,125)),transform.scale(movingFroggy,(125,125)),1000,500,125,125,12,4,2,2,2)',
                 'Enemy("Greater Froggy",transform.scale(froggySprite,(150,150)),transform.scale(movingFroggy,(150,150)),0,500,150,150,12,5,2,1,3)'],
                [(Rect(0,30,300,5),3,(500,550)),
                 (Rect(900,30,300,5),2,(500,550))])]
currstage = 0
stage = stages[currstage] #the stage we're on
stage.draw(screen)
enemies = stage.enemies
moveable = stage.moveable
died = 0
stagechangers = stage.stagechangers
screenBuffer = screen.copy() #screen buffer
level = 1
savedCharaStats = {"atk":1,"defen":1,"lv":1,"xp":0,"maxhp":10,"x":1,"y":31}
beatlevel = False
bossinit = False
textmode = False
texts = []
textat = 0
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if beatlevel:
                beatlevel = False
                backMusic.stop()
                backMusic.play(mainBackMusic,-1)
                level += 1
                draw.rect(screen,GREY,(0,0,1200,30))
                draw.rect(screen,GREY,(0,706,1200,30))
                if level == 2:
                    #stages
                    stages = [Stage([Rect(0,30,400,200),Rect(300,30,200,300),Rect(100,330,700,376),Rect(500,30,750,300)],
                                    ['Enemy("Maximum Froggy",transform.scale(froggySprite,(200,200)),transform.scale(movingFroggy,(200,200)),200,400,200,200,20,9,3,1,5)',
                                    'Enemy("Greater Froggy",transform.scale(froggySprite,(150,150)),transform.scale(movingFroggy,(150,150)),500,500,150,150,15,5,2,1,3)'],
                                    [(Rect(1150,30,100,200),1,(10,31)),
                                     (Rect(100,700,700,40),2,(100,38))]),
                              Stage([Rect(0,30,400,305),Rect(200,30,250,300),Rect(200,330,600,376)],
                                    ['Enemy("Enhanced Pyrant",enhancedPyrant,movingEnhancedPyrant,400,400,50,150,15,-4,3,3,5)',
                                     'Enemy("Enhanced Pyrant",enhancedPyrant,movingEnhancedPyrant,500,400,50,150,15,-4,3,3,5)'],
                                    [(Rect(0,30,5,305),0,(1040,31)),
                                     (Rect(200,700,600,40),2,(1000,38))],
                                    [HealPoint(520,340)]),
                              Stage([Rect(0,30,300,50),Rect(900,30,300,50),Rect(0,60,1200,646)],
                                ['Enemy("Goat Dog",goatdog,goatdog,500,100,300,200,17,11,5,3,7)',
                                 'Enemy("Enhanced Pyrant",enhancedPyrant,movingEnhancedPyrant,250,50,50,150,15,-4,3,3,5)',
                                 'Enemy("Maximum Froggy",transform.scale(froggySprite,(200,200)),transform.scale(movingFroggy,(200,200)),600,500,200,200,20,9,3,1,5)'],
                                [(Rect(0,30,300,5),0,(500,550)),
                                 (Rect(900,30,300,5),1,(500,550))])]
                    currstage = 0
                    stage = stages[currstage] #the stage we're on
                    stage.draw(screen)
                    defx,defy = 1,31
                #-sets default stats for Chara
                savedCharaStats["x"] = defx
                savedCharaStats["y"] = defy
                savedCharaStats["lv"] = chara.lv
                savedCharaStats["atk"] = chara.atk
                savedCharaStats["xp"] = chara.xp
                savedCharaStats["defen"] = chara.defen
                savedCharaStats["maxhp"] = chara.maxhp
                chara.hp = chara.maxhp
                chara.x,chara.y = defx,defy
                screenBuffer = screen.copy()
            if textmode and e.unicode.lower() == "z":
                #if it's textmode, z moves the text forward
                textat += 1
                if textat >= len(texts):
                    #if it's out of bounds we turn off text mode
                    textmode = False
                    backMusic.stop()
                    backMusic.play(mainBackMusic,-1)
                    textat = 0
            if e.unicode.lower() == "x":
                #changes modes
                currmodeIndex = chara.modes.index(chara.mode)
                if currmodeIndex + 1 == len(chara.modes):
                    currmodeIndex = -1
                modetoChange = chara.modes[currmodeIndex+1]
                chara.changeMode(modetoChange)
    if gameover:
        #gameover
        screen.fill(RED)
        screen.blit(lucidaConsole.render("GAME OVER",True,BLACK),(500,360))
        screen.blit(lucidaConsole.render("X to continue",True,BLACK),(475,380))
        if key.get_pressed()[K_x]:
            gameover = False
            for s in stages:
                s.reset() #restarts game
            restart()
    elif textmode:
        draw.rect(screen,GREY,(0,0,900,150))
        #text mode
        newFont = lucidaConsole if textat in [0,len(texts)-1] else papyrus #sets newFont to be Papyrus except for first line and last line
        changeMsg(texts[textat],newFont)
        #draws message
        screen.blit(msgFont.render(msg,True,BLACK),(10,5))
        if time()%1 < 0.5:
            screen.blit(smallfont.render("Press [Z] to continue.",True,BLACK),(730,5))
        chara.draw(screen)
    elif beatlevel:
        #level beat
        screen.fill(GREEN)
        screen.blit(lucidaConsole.render("YOU BEAT LEVEL "+str(level)+"!",True,BLACK),(500,360))
        screen.blit(lucidaConsole.render("The next level is kind of... incomplete [Press any key to continue]",True,BLACK),(250,380))
    else:
        screen.blit(screenBuffer,(0,0))
        screenBuffer = screen.copy()
        #sets this stage's enemies and moveable rects and stage changer rects
        enemies = stage.enemies
        moveable = stage.moveable
        stagechangers = stage.stagechangers
        kp = key.get_pressed()
        #handling Chara
        chara.reset() #resets chara
        #move chara
        if kp[K_UP]:
            chara.move((chara.x,chara.y-chara.spd))
        if kp[K_DOWN]:
            chara.move((chara.x,chara.y+chara.spd))
        if kp[K_LEFT]:
            chara.move((chara.x-chara.spd,chara.y))
            chara.dir = 0
        if kp[K_RIGHT]:
            chara.move((chara.x+chara.spd,chara.y))
            chara.dir = 1
        for s in stagechangers:
            if touching(s[0]):
                #changes stage
                currstage = s[1]
                stage = stages[currstage]
                moveable = stage.moveable
                enemies = stage.enemies
                stagechangers = stage.stagechangers
                stage.draw(screen)
                chara.x = s[2][0] if s[2][0] != None else chara.x #set chara's location to stagechangers end up location
                chara.y = s[2][1] if s[2][1] != None else chara.y
                if bossinit and currstage == len(stages)-1:
                    backMusic.stop()
                    backMusic.play(bossMusic,-1)
        if kp[K_z]:
            #attacks on z
            chara.attack()
        if kp[K_y]:
            #secret debug tool for me - gives me op ness
            chara.atk = 9001
            chara.maxhp = 9001
            chara.hp = 9001
            chara.spd = 5
            chara.defen = 9001
            chara.lv = 9001
            chara.atkspd = 0.1
        #draws chara's health bar
        draw.rect(screen,RED,(900,0,300,30))
        draw.rect(screen,GREEN,(900,0,int(300*chara.hp/chara.maxhp),30))
        screen.blit(lucidaConsole.render("HP: "+str(chara.hp)+"/"+str(chara.maxhp),True,BLACK),(920,5))
        #draws chara
        chara.draw(screen)
        for h in stage.healpoints:
            h.draw(screen)
            if touching(h):
                #if healpoint is touching Chara we recover health
                if time() % 0.5 > 0.25:
                    chara.setHp(chara.hp+1)
                effects.queue(healeffect)
        #end of handling Chara
        #handling Enemies
        for en in enemies:
            en.reset() #resets enemy
            #draws enemy
            #enemy moves once every spd they have
            if en.hp > en.maxhp/3:
                #if the enemy is not low health they move toward Frisk
                en.move()
            else:
                #if the enemy is low health they run away
                en.move(False)
            if type(en) == FrogKing:
                #if it's the FrogKing he summons things
                en.summon()
            en.draw(screen)
        #end of handling enemies
        #draws message
        screen.blit(msgFont.render(msg,True,BLACK),(10,5))
        #draws stats for Chara/Frisk
        if chara.mode == 'normal':
            txtcol = BLACK #text is black for normal mode
        else:
            txtcol = eval(chara.mode.upper()) #otherwise it is the color of the mode
        screen.blit(lucidaConsole.render("ATK: "+str(chara.atk+chara.watk)+" DEF: "+str(chara.defen+chara.adef)+" SPD: "+str(chara.spd)+" Attack Speed: attack/"+str(chara.atkspd)+" secs",True,txtcol,),(305,711))
        #draws xp bar and Level for Chara/Frisk
        draw.rect(screen,RED,(0,706,300,30))
        draw.rect(screen,BLUE,(0,706,int(300*chara.xp/(chara.lv*100)),30))
        screen.blit(lucidaConsole.render("XP: "+str(chara.xp)+"/"+str(chara.lv*100),True,BLACK),(10,711))
        screen.blit(lucidaConsole.render("LV: "+str(chara.lv),True,BLACK),(1110,711))
        for s in stages:
            if len(s.enemies) > 0:
                break
        else:
            #after checking if all enemies are dead, we allow the bossfight
            if bossinit:
                beatlevel = True #you beat level if the boss was initiated
                bossinit = False
                backMusic.stop()
                backMusic.play(victoryMusic,-1)
            elif level == 1:
                #makes it textmode
                textmode = True
                backMusic.stop()
                backMusic.play(textMusic,-1)
                bossinit = True #boss fight initiated
                texts = ["You hear a voice...",
                         "\"HOW DARE YOU MURDER MY SUBJECTS!",
                         "Come to the southernmost room...",
                         "You'll see a new path",
                         "Fight me!\"",
                         "Better go fight that guy."]
                stages[-1].stagechangers.append((Rect(400,30,400,6),5,(500,550)))
                stages[-1].moveable.append(Rect(400,30,400,50))
                stages.append(Stage([Rect(0,30,1200,676)],
                            ['FrogKing("Frog King",frogKing,frogKing,500,35,250,250,300,-0.1,4,6,7)'],
                            []))
                screen.blit(screenBuffer,(0,0))
                if stage == stages[-2]:
                    stages[-2].draw(screen)
    display.flip()
quit()
