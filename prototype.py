import pygame
import player
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("YuiYui Adventure")
font = pygame.font.SysFont(None, 48)
running = True

 #make a game
# display
colour = "purple"
# display
# character
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    
    #coding game
    #display
    screen.fill(colour)
    

#end process
pygame.quit()