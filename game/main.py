from websockets.sync.client import connect
from network import Network
import websockets
import asyncio
import json


import pygame,random

pygame.init() 

clock = pygame.time.Clock()

screen = pygame.display.set_mode([1000, 500])

loadTips = []
with open('loadTips.txt') as file:
    while True:
        line = file.readline()
        if not line:
            break
        elif line != '\n':
            line = line[:-1]
            loadTips.append(line)

class Button:
    def __init__(self,width,height,colour,text,font):
        self.rect = pygame.Rect(0,0,width,height)
        self.colour = colour
        self.text = text
        self.font = font
        self.border = 1
        self.lastClicked = -5000
        self.active = False

    def setColour(self,colour):
        self.colour = colour

    def setText(self,text):
        self.text = text

    def draw(self,surface,offset):
        self.rect.center = (surface.get_width()//2 + offset[1],surface.get_height()//2 + offset[0])
        pygame.draw.rect(surface,self.colour,self.rect)
        textSurface = self.font.render(self.text, True, (0,0,0)) 
        surface.blit(textSurface, (self.rect.x+5,self.rect.y+5))
        self.rect.w = max(100, textSurface.get_width()+10)
        pygame.draw.rect(surface,(255,255,255),self.rect,self.border)
        

    def clicked(self,event):
        self.hover()
        returner = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.time.get_ticks() - self.lastClicked > 100:
            if self.rect.collidepoint(event.pos):
                self.border = 1
                self.lastClicked = pygame.time.get_ticks()
                returner =  True
        return returner

    def hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.border = 3
            self.colour = pygame.Color('lightskyblue3')
        else:
            self.border = 1
            self.colour = pygame.Color('chartreuse4')

    def textBoxCode(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.colour = pygame.Color('lightskyblue3')
                self.active = True
            else:
                self.colour = pygame.Color('chartreuse4')
                self.active = False

    def activeCode(self,event):
        if (event.type == pygame.KEYDOWN) and self.active:
            if event.key == pygame.K_BACKSPACE:  
                    self.text = self.text[:-1] 
            else: 
                    self.text += event.unicode
            
        



class Animation:
    def __init__(self,offset,width,height,pics,host,multiList):
        self.images = []
        self.width = width
        self.height = height
        for pic in pics:
            self.images.append(pygame.image.load(pic))
        self.lastChange = -5000
        self.num = 0
        self.num2= 0
        self.currentImage = pygame.transform.scale(self.images[self.num],(self.width,self.height))
        self.offset = offset
        self.host = host
        self.multi = multiList

    def setImage(self):
        self.num += 1
        if self.num >= len(self.images):
            self.num = 0
        self.currentImage = pygame.transform.scale(self.images[self.num],(self.width*self.multi[self.num2],self.height*self.multi[self.num2]))

    def setImageSize(self):
        self.num2 += 1
        if self.num2 >= len(self.multi):
            self.num2 = 0
        self.currentImage = pygame.transform.scale(self.images[self.num],(self.width*self.multi[self.num2],self.height*self.multi[self.num2]))
        

    def draw(self,surface):
        box = self.currentImage.get_rect()
        box.center = (surface.get_width()//2 + self.offset[1],surface.get_height()//2 + self.offset[0])
        surface.blit(self.currentImage,box)

class CharSelect:
    def __init__(self,y,x,width,height,image,altImage,name):
        self.offset = (x,y)
        self.image = pygame.image.load(image)
        self.scaledImage = pygame.transform.scale(self.image,(width,height))
        self.altImage = pygame.image.load(altImage)
        self.altScaledImage = pygame.transform.scale(self.altImage,(width,height))
        self.name = name
        self.currentImage = self.scaledImage
        self.lastClicked = -5000
        self.border = 1

    def draw(self,surface):
        box = self.currentImage.get_rect()
        box.center = (surface.get_width()//2 + self.offset[1],surface.get_height()//2 + self.offset[0])
        surface.blit(self.currentImage,box)
        pygame.draw.rect(surface,(255,255,255),box,self.border)

    def clicked(self,event,surface):
        box = self.currentImage.get_rect()
        box.center = (surface.get_width()//2 + self.offset[1],surface.get_height()//2 + self.offset[0])
        self.hover(box)
        returner = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.time.get_ticks() - self.lastClicked > 100:
            if box.collidepoint(event.pos):
                self.border = 1
                self.lastClicked = pygame.time.get_ticks()
                returner =  True
        return returner

    def hover(self,box):
        if box.collidepoint(pygame.mouse.get_pos()):
            self.border = 3
            self.currentImage = self.altScaledImage
        else:
            self.border = 1
            self.currentImage = self.scaledImage

class Player:
    def __init__(self,name,weakness,strength,rap,defence,lethality,host):
        self.health = 100
        self.name = name
        self.weakness = weakness
        self.strength = strength
        self.rapTxt = rap
        self.defence = defence
        self.lethality = lethality
        self.host = host

    def damage(self,damage):
        self.health -= damage
        

def createPlayer(name,offset,host,multi):
    match name:
        case "Flash":
            user = Player(name,'cold','hot','',0.5,1.5,host)
            img = Animation(offset,200,200,['flash_pics/flash.png','flash_pics/flash1.png','flash_pics/flash.png','flash_pics/flash2.png'],host,multi)
        case "Buzz":
            user = Player(name,'anxiety','nature','',1.5,0.5,host)
            img = Animation(offset,200,200,['buzz_pics/buzz.png','buzz_pics/buzz1.png','buzz_pics/buzz.png','buzz_pics/buzz2.png'],host,multi)
        case "Sensor":
            user = Player(name,'parent','brainrot','',1,1,host)
            img = Animation(offset,200,200,['sensor_pics/sensor.png','sensor_pics/sensor1.png','sensor_pics/sensor.png','sensor_pics/sensor2.png'],host,multi)
    return user,img

def randomTip(loadTips):
    return loadTips[random.randint(0,len(loadTips)-1)]

def endRound(fullRap,base_font,host,nw):
    p=0
    if host==True:
        p=1
    data = nw.submit_rap(fullRap,p,fullRap)
    enemyRap = data['opponent_rap']
    if host:
        raps = fullRap
        rap2 = enemyRap
    else:
        raps = enemyRap
        rap2 = fullRap
    #send rap
    #recieve rap
    #send damange
    #recieve damage
    damageRecieved = data['your_damage']
    damageDone = data['opponent_damage']
    #player1.damage(damageRecieved)
    #player2.damage(damageDone)
    rapLines = []
    for rap in raps:
        rapLines.append(Button(140,32,(255,255,255),rap,base_font))
    return rapLines, rap2, damageRecieved, damageDone
    




def gameLoop(nw):
        
    base_font = pygame.font.Font(None, 32)
    background = pygame.image.load('background.png')
    background = pygame.transform.scale(background,(1000,500))

    colour_active = pygame.Color('lightskyblue3')
    colour_passive = pygame.Color('chartreuse4')

    #state 1
    gameIDInput = Button(140,32,colour_passive,'',base_font)
    createGame = Button(140,32,colour_passive,'Create new game!',base_font)
    joinGame = Button(140,32,colour_passive,'Join game with code!',base_font)
    #state2
    char1 = CharSelect(-200,0,100,100,'flash_pics/flash.png','names_pics/flashname.png','Flash')
    char2 = CharSelect(0,0,100,100,'buzz_pics/buzz.png','names_pics/buzzname.png','Buzz')
    char3 = CharSelect(200,0,100,100,'sensor_pics/sensor.png','names_pics/sensorname.png','Sensor')
    selectTxt = Button(140,32,(255,255,255),'SELECT YOUR FIGHTER!',base_font)
    #state 3
    loadTxt = Button(140,32,(255,255,255),randomTip(loadTips),base_font)
    codeTxt = Button(140,32,(255,255,255),'',base_font)
    #state 4
    rapInput1 = Button(140,32,colour_passive,'',base_font)
    rapInput2 = Button(140,32,colour_passive,'',base_font)
    rapInput3 = Button(140,32,colour_passive,'',base_font)
    rapInput4 = Button(140,32,colour_passive,'',base_font)
    timerTxt = Button(140,32,(255,255,255),'10',base_font)
    p1DmgTxt = Button(140,32,(255,255,255),'Health: 100',base_font)
    p2DmgTxt = Button(140,32,(255,255,255),'Health: 100',base_font)
    

    active = False
    rapActive = 0
    gameRun = True
    state = 1
    subState = True

    while gameRun:
        dt = clock.tick(30)
        if state == 1:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    gameRun = False

                gameIDInput.textBoxCode(event)
                gameIDInput.activeCode(event)
                    
                if createGame.clicked(event):
                    state += 1 #create a game
                    host = True
                elif joinGame.clicked(event):
                    state += 1 #join a game
                    host = False

            screen.fill((0,0,0))

            gameIDInput.draw(screen,(0,0))
            createGame.draw(screen,(-100,0))
            joinGame.draw(screen,(100,0))
            
        elif state == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameRun = False

                if char1.clicked(event,screen):
                    player1,p1Img = createPlayer(char1.name,(100,-300),host,[1,1.5,0.5])
                    if host==True:
                        thing = player1.__dict__
                        thing['player'] = 1
                        codeTxt.setText(nw.create_lobby(thing))
                    else:
                        thing = player1.__dict__
                        thing['player'] = 2
                        nw.join_lobby(thing,gameIDInput.text)
                    state += 1
                elif char2.clicked(event,screen):
                    player1,p1Img = createPlayer(char2.name,(100,-300),host,[1,1.5,0.5])
                    if host==True:
                        thing = player1.__dict__
                        thing['player'] = 1
                        codeTxt.setText(nw.create_lobby(thing))
                    else:
                        thing = player1.__dict__
                        thing['player'] = 2
                        nw.join_lobby(thing,gameIDInput.text)
                    state += 1
                elif char3.clicked(event,screen):
                    player1,p1Img = createPlayer(char3.name,(100,-300),host,[1,1.5,0.5])
                    if host==True:
                        thing = player1.__dict__
                        thing['player'] = 1
                        codeTxt.setText(nw.create_lobby(thing))
                    else:
                        thing = player1.__dict__
                        thing['player'] = 2
                        nw.join_lobby(thing,gameIDInput.text)
                    state += 1
                

            screen.fill((0,0,0))

            char1.draw(screen)
            char2.draw(screen)
            char3.draw(screen)

            selectTxt.draw(screen,(-100,0))
        elif state == 3:
            #request player2 data (name of fighter picked)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    gameRun = False

            screen.fill((0,0,0))

            if not message_queue.empty():
                message = json.load(asyncio.wait_for(message_queue.get(), timeout=0.1))
                loadTxt.lastClicked = pygame.time.get_ticks()
                loadTxt.setText(randomTip(loadTips))
                state += 1 #this is load area wait for players.
                player2,p2Img = createPlayer(message["opponent_attributes"]["name"],(-100,300),host,[1,0.5,1.5])

            loadTxt.draw(screen,(0,0))
            codeTxt.draw(screen,(100,0))
        elif state == 4:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    gameRun = False

                if subState:
                    rapInput1.textBoxCode(event)
                    rapInput2.textBoxCode(event)
                    rapInput3.textBoxCode(event)
                    rapInput4.textBoxCode(event)

                    rapInput1.activeCode(event)
                    rapInput2.activeCode(event)
                    rapInput3.activeCode(event)
                    rapInput4.activeCode(event)

            screen.blit(background,(0,0))

            if pygame.time.get_ticks() - p1Img.lastChange > 1000:
                p1Img.setImage()
                p1Img.lastChange = pygame.time.get_ticks()
            if pygame.time.get_ticks() - p2Img.lastChange > 1000:
                p2Img.setImage()
                p2Img.lastChange = pygame.time.get_ticks()
            if (pygame.time.get_ticks() - timerTxt.lastClicked > 1000) and subState:
                if timerTxt.text == '0':
                    timerTxt.setText('181')
                    subState = False
                    fullRap = [rapInput1.text,rapInput2.text,rapInput3.text,rapInput4.text]
                    rapTxts, rapNew, damageRecieved, damageDone = endRound(fullRap, base_font, host,nw)
                    p1Img.setImageSize()
                    p2Img.setImageSize()
                timerTxt.setText(str(int(timerTxt.text) - 1))
                timerTxt.lastClicked = pygame.time.get_ticks()
            if  (not subState) and (pygame.time.get_ticks() - timerTxt.lastClicked > 10000) and (p1Img.num2 == 1): #need to be time taken for rap to be read out
                p1Img.setImageSize()
                p2Img.setImageSize()
                for i in range(0,len(rapTxts)):
                    rapTxts[i].setText(rapNew[i])
                if host:
                    player2.damage(damageDone)
                    p2DmgTxt.setText('Health: ' + str(player2.health))
                else:
                    player1.damage(damageRecieved)
                    p1DmgTxt.setText('Health: ' + str(player1.health))
            elif  (not subState) and (pygame.time.get_ticks() - timerTxt.lastClicked > 20000) and (p1Img.num2 == 2): #need to be time taken for rap to be read out
                p1Img.setImageSize()
                p2Img.setImageSize()
                if host:
                    player1.damage(damageRecieved)
                    p1DmgTxt.setText('Health: ' + str(player1.health))
                    
                else:
                    player2.damage(damageDone)
                    p2DmgTxt.setText('Health: ' + str(player2.health))
                subState = True

            p1Img.draw(screen)
            p2Img.draw(screen)
            if subState:
                rapInput1.draw(screen,(50,0))
                rapInput2.draw(screen,(100,0))
                rapInput3.draw(screen,(150,0))
                rapInput4.draw(screen,(200,0))
                timerTxt.draw(screen,(-230,-430))
            else:
                for i in range(0,len(rapTxts)):
                    rapTxts[i].draw(screen,(32*i,0))
            p1DmgTxt.draw(screen,(230,-430))
            p2DmgTxt.draw(screen,(-230,430))

                

                
        pygame.display.flip()


async def receive_messages(websocket, message_queue):
    try:
        while True:
            message = await websocket.recv()
            await message_queue.put(message)
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed.")



async def main():
    uri = "ws://172.22.236.99:8765"
    async with websockets.connect(uri) as websocket:
        nw = Network(websocket)
        message_queue=asyncio.Queue()
        asyncio.create_task(receive_messages(websocket, message_queue))
        gameLoop(nw)

asyncio.run(main())
