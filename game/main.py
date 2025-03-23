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
        



class Animation:
    def __init__(self,x,y,width,height,images):
        self.images = []
        for image in images:
            self.image.append(pygame.image.load(image))

    def setImage(self,image):
        self.image = image

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
    def __init__(self,name,weakness,strength,rap,defence,lethality):
        self.health = 100
        self.name = name
        self.weakness = weakness
        self.strength = strength
        self.rapTxt = rap
        self.defence = defence
        self.lethality = lethality

    def damage(self,damage):
        self.health -= damage

def createPlayer(name):
    match name:
        case "Flash":
            user = Player(name,'cold','hot','',0.5,1.5)
        case "Buzz":
            user = Player(name,'anxiety','nature','',1.5,0.5)
        case "Sensor":
            user = Player(name,'parent','brainrot','',1,1)
    return user

def randomTip(loadTips):
    return loadTips[random.randint(0,len(loadTips)-1)]
    




def gameLoop():
        
    base_font = pygame.font.Font(None, 32)

    colour_active = pygame.Color('lightskyblue3')
    colour_passive = pygame.Color('chartreuse4')

    #state 1
    gameIDInput = Button(140,32,colour_passive,'',base_font)
    createGame = Button(140,32,colour_passive,'Create new game!',base_font)
    joinGame = Button(140,32,colour_passive,'Join game with code!',base_font)
    #state2
    char1 = CharSelect(-200,0,100,100,'barry.png','miku.png','Flash')
    char2 = CharSelect(0,0,100,100,'barry.png','miku.png','Buzz')
    char3 = CharSelect(200,0,100,100,'barry.png','miku.png','Sensor')
    selectTxt = Button(140,32,(255,255,255),'SELECT YOUR FIGHTER!',base_font)
    #state 3
    loadTxt = Button(140,32,(255,255,255),randomTip(loadTips),base_font)
    #state 4
    rapInput = Button(140,32,colour_passive,'',base_font)
    attack = Button(140,32,colour_passive,'',base_font)

    active = False
    gameRun = True
    state = 1

    while gameRun:
        dt = clock.tick(30)
        if state == 1:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    gameRun = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if gameIDInput.rect.collidepoint(event.pos):
                            active = True
                    else: 
                            active = False
                    
                if createGame.clicked(event):
                    state += 1 #create a game
                elif joinGame.clicked(event):
                    state += 1 #join a game

                if (event.type == pygame.KEYDOWN) and active:
                    
                    if event.key == pygame.K_BACKSPACE: 

                            # get text input from 0 to -1 i.e. end. 
                            gameIDInput.text = gameIDInput.text[:-1] 

                    # Unicode standard is used for string 
                    # formation 
                    else: 
                            gameIDInput.text += event.unicode
            
            # it will set background color of screen 
            screen.fill((0,0,0))

            if active: 
                    gameIDInput.setColour(colour_active)
            else: 
                    gameIDInput.setColour(colour_passive)

            gameIDInput.draw(screen,(0,0))
            createGame.draw(screen,(-100,0))
            joinGame.draw(screen,(100,0))
            
            # display.flip() will update only a portion of the 
            # screen to updated, not full area
        elif state == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameRun = False

                if char1.clicked(event,screen):
                    player1 = createPlayer(char1.name)
                    state += 1
                elif char2.clicked(event,screen):
                    player1 = createPlayer(char2.name)
                    state += 1
                elif char3.clicked(event,screen):
                    player1 = createPlayer(char3.name)
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

            if pygame.time.get_ticks() - loadTxt.lastClicked > 50000:
                loadTxt.lastClicked = pygame.time.get_ticks()
                loadTxt.setText(randomTip(loadTips))
                state += 1 #this is load area wait for players.
                player2 = createPlayer('Sensor')

            loadTxt.draw(screen,(0,0))
        elif state == 4:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    gameRun = False

            screen.fill((0,0,0))
                

                
        pygame.display.flip()

gameLoop()
