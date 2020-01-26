import pygame
import random
import sys
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
done = False

alfabet='_aąbcćdeęfghijklłmnoópqrsśtuwvzźż'
slowo = []
font = pygame.font.SysFont("comicsansms", 72)

counter = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if button.collidepoint(mouse_pos):
                    # prints current location of mouse
                    print('button was pressed at {0}'.format(mouse_pos))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #działanie spacji; wybór literki
            slowo.append(alfabet[counter - 1])
            print(slowo)
            '''
            counter = 0
            '''


    screen.fill((255, 255, 255))
    text = font.render(alfabet[counter], True, (0, 128, 0))
    screen.blit(text,
        (320 - text.get_width() // 2, 240 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(3)
    counter=counter+1
    if counter == len(alfabet):
        counter = 0
