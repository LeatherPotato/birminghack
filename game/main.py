import pygame 

pygame.init() 

clock = pygame.time.Clock() 

# it will display on screen 
screen = pygame.display.set_mode([600, 500])

class TextBox:
    def __init__(self,x,y,width,height,colour,text):
        self.rect = pygame.Rect(x,y,width,height)
        self.colour = colour
        self.text = text

    def setColour(self,colour):
        self.colour = colour

    def clicked(self):
        pass

class Button:
    def __init__(self,x,y,width,height,colour,label):
        self.rect = pygame.Rect(x,y,width,height)
        self.colour = colour
        self.label = label

    def setColour(self,colour):
        self.colour = colour

class Image:
    def __init__(self,x,y,width,height,image):
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.image.load(image)

    def setImage(self,image):
        self.image = image

class CharSelect:
    def __init__(self,x,y,width,height,image):
        self.pos = (x,y)
        self.image = pygame.image.load(image)
        self.scaledImage = pygame.transform.scale(self.image,(width,height))

    def draw(self,surface):
        box = self.scaledImage.get_rect()
        box.center = self.pos
        surface.blit(self.scaledImage,box)

    def clicked(self):
        pass



base_font = pygame.font.Font(None, 32)

colour_active = pygame.Color('lightskyblue3')
colour_passive = pygame.Color('chartreuse4')

gameIDInput = TextBox(200,200,140,32,colour_passive,'')
createGame = Button(200,100,140,32,colour_passive,'Create new game!')
joinGame = Button(200,300,140,32,colour_passive,'Join game with code!')
char1 = CharSelect(200,440,50,50,'barry.png')
char2 = CharSelect(300,440,50,50,'barry.png')
char3 = CharSelect(400,440,50,50,'barry.png')

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

            if (event.type == pygame.KEYDOWN) and active:

                    # Check for backspace 
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

        pygame.draw.rect(screen, gameIDInput.colour, gameIDInput.rect) 

        text_surface = base_font.render(gameIDInput.text, True, (0,0,0)) 
        
        # render at position stated in arguments 
        screen.blit(text_surface, (gameIDInput.rect.x+5, gameIDInput.rect.y+5)) 
        
        # set width of textfield so that text cannot get 
        # outside of user's text input 
        gameIDInput.rect.w = max(100, text_surface.get_width()+10)

        char1.draw(screen)
        char2.draw(screen)
        char3.draw(screen)
        
        # display.flip() will update only a portion of the 
        # screen to updated, not full area
    else:
        pass
    pygame.display.flip()
