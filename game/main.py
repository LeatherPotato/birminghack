import pygame 

pygame.init() 

clock = pygame.time.Clock()

screen = pygame.display.set_mode([600, 500])

class Button:
    def __init__(self,x,y,width,height,colour,text,font):
        self.rect = pygame.Rect(x,y,width,height)
        self.colour = colour
        self.text = text
        self.font = font
        self.border = 1
        self.lastClicked = -5000

    def setColour(self,colour):
        self.colour = colour

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
        



class Image:
    def __init__(self,x,y,width,height,image):
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.image.load(image)

    def setImage(self,image):
        self.image = image

class CharSelect:
    def __init__(self,x,y,width,height,image,name):
        self.pos = (x,y)
        self.image = pygame.image.load(image)
        self.scaledImage = pygame.transform.scale(self.image,(width,height))
        self.name = name

    def draw(self,surface,select):
        box = self.scaledImage.get_rect()
        box.center = self.pos
        surface.blit(self.scaledImage,box)
        if select == self.name:
            pygame.draw.rect(surface,(255,255,255),box,2)

    def clicked(self,event,select):
        box = self.scaledImage.get_rect()
        box.center = self.pos
        if box.collidepoint(event.pos):
            return self.name
        else:
            return select

class Player:
    def __init__(self,name,weakness,strength,rap,defence):
        self.health = 100
        self.name = name
        self.weakness = weakness
        self.strength = strength
        self.rapTxt = rap
        self.defence = defense



base_font = pygame.font.Font(None, 32)

colour_active = pygame.Color('lightskyblue3')
colour_passive = pygame.Color('chartreuse4')

gameIDInput = Button(200,200,140,32,colour_passive,'',base_font)
createGame = Button(200,100,140,32,colour_passive,'Create new game!',base_font)
joinGame = Button(200,300,140,32,colour_passive,'Join game with code!',base_font)
char1 = CharSelect(200,440,50,50,'barry.png','Flash')
char2 = CharSelect(300,440,50,50,'barry.png','Buzz')
char3 = CharSelect(400,440,50,50,'barry.png','Sensor')
selected = 'Flash'

active = False
gameRun = True
state = True

while gameRun:
    dt = clock.tick(30)
    if state:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameRun = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameIDInput.rect.collidepoint(event.pos):
                        active = True
                else: 
                        active = False

                selected = char1.clicked(event,selected)
                selected = char2.clicked(event,selected)
                selected = char3.clicked(event,selected)
                
            if createGame.clicked(event):
                state = False #create a game
            if joinGame.clicked(event):
                state = False #join a game

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

        char1.draw(screen,selected)
        char2.draw(screen,selected)
        char3.draw(screen,selected)
        
        # display.flip() will update only a portion of the 
        # screen to updated, not full area
    else:
        pass
    pygame.display.flip()
