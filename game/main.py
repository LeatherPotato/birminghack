import pygame 

pygame.init() 

clock = pygame.time.Clock() 

# it will display on screen 
screen = pygame.display.set_mode([600, 500])

class UI:
    def __init__(self,x,y,width,height,colour):
        self.rect = pygame.Rect(x,y,width,height)
        self.colour = colour

    def setColour(colour):
        self.colour = colour

base_font = pygame.font.Font(None, 32) 
gameID = ''
rap = ''

colour_active = pygame.Color('lightskyblue3')
colour_passive = pygame.Color('chartreuse4') 

gameIDInput = UI(200,200,140,32,colour_passive)
createGame = UI(200,100,140,32,colour_passive)
joinGame = UI(200,300,140,32,colour_passive)

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
                            gameID = gameID[:-1] 

                    # Unicode standard is used for string 
                    # formation 
                    else: 
                            gameID += event.unicode
        
        # it will set background color of screen 
        screen.fill((0,0,0))

        if active: 
                gameIDInput.setColour(colour_active)
        else: 
                gameIDInput.setColour(colour_passive)

        pygame.draw.rect(screen, colour, gameIDInput.rect) 

        text_surface = base_font.render(gameID, True, (0,0,0)) 
        
        # render at position stated in arguments 
        screen.blit(text_surface, (gameIDInput.rect.x+5, gameIDInput.rect.y+5)) 
        
        # set width of textfield so that text cannot get 
        # outside of user's text input 
        gameIDInput.rect.w = max(100, text_surface.get_width()+10)
        
        # display.flip() will update only a portion of the 
        # screen to updated, not full area
    else:
        pass
    pygame.display.flip()
