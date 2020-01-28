# -*- coding: utf-8 -*-
import random
import string
import sys
import pygame
from psychopy import visual, event, core
import multiprocessing as mp
import pygame as pg
import pandas as pd
import filterlib as flt
import blink as blk
from pyOpenBCI import OpenBCIGanglion

pygame.init()


def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:
                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()


####################################################
    SYMULACJA_SYGNALU = False
####################################################
    mac_adress = 'd2:b4:11:81:48:ad'
    '''
    4b:fd:a2:17:03:db
    '''
####################################################

    clock = pg.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane_do_symulacji/data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":


    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    #connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')

    ############################################
    # Poniżej należy dodać rozwinięcie programu
    ############################################


    sw,sh = 1280, 760 # ScreenWidth, ScreenHeight
    sc = (sw/2, sh/2) # Shortcut for the center of the screen
    screen = pygame.display.set_mode((sw,sh))
    default_font = pygame.font.SysFont(None, 40) #wielkość i rozmiar liter
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 90)
    done = False

# Assigning all the primary/secondary colors to a dictionary to use more practically
    colors = {"black":(0,0,0), "darkgray":(70,70,70), "gray":(128,128,128), "lightgray":(200,200,200), "white":(255,255,255), "red":(255,0,0),
          "darkred":(128,0,0),"green":(0,255,0),"darkgreen":(0,128,0), "blue":(0,0,255), "navy":(0,0,128), "darkblue":(0,0,128),
          "yellow":(255,255,0), "gold":(255,215,0), "orange":(255,165,0), "lilac":(229,204,255),"lightblue":(135,206,250),"teal":(0,128,128),
          "cyan":(0,255,255), "purple":(150,0,150), "pink":(238,130,238), "brown":(139,69,19), "lightbrown":(222,184,135),"lightgreen":(144,238,144),
          "turquoise":(64,224,208),"beige":(245,245,220),"honeydew":(240,255,240),"lavender":(230,230,250),"crimson":(220,20,60)}

    images = {0:pygame.image.load("empty.png"), 1:pygame.image.load("v1.png"), 2:pygame.image.load("v2.png"),
      3:pygame.image.load("v3.png"),4:pygame.image.load("v4.png"),5:pygame.image.load("v5.png"),6:pygame.image.load("v6.png")}

    alphabet = list(string.ascii_uppercase) # Getting all the letters in the latin alphabet

    class Button(object): # A GENERAL CLASS FOR ALL THE BUTTONS ON THE SCREEN (LETTERS & LANGUAGE BUTTONS)
        def __init__(self, color, pos, width, height, letter, active = False, type = 1, size = 40):
            self.type = type #TYPE 1 IS A LETTER, TYPE 2 IS A LANGUAGE BUTTON
            self.active = active    # A VARIABLE ONLY FOR TYPE 2
            self.clicked = False    # A VARIABLE ONLY FOR TYPE 1
            self.rollOver = False   # A VARIABLE ONLY FOR TYPE 1
            self.size = size
            self.font = pygame.font.SysFont(None, self.size)
            self.color = color
            self.letter = letter
            self.pos = pos
            self.width = width
            self.height = height
            self.subsurface = pygame.Surface((self.width, self.height))         # CREATING A SUBSURFACE TO
            self.subsurface.fill(self.color)                                # GET A RECT (FOR COLLISION)
            self.text = self.font.render(self.letter, True, colors["white"])

        def Draw(self, surface):
            if self.type == 1:
                if self.rollOver:                   # IF A TYPE 1 BUTTON IS UNDER
                    self.subsurface.set_alpha(200)  # THE MOUSE, MAKE IT LESS VIBRANT
                else:
                    self.subsurface.set_alpha(255)
                if not self.clicked:
                    surface.blit(self.subsurface, self.pos)
                    self.subsurface.blit(self.text, (self.width/4,self.height/5))
            if self.type == 2:
                if self.active:                     # IF A TYPE 2 BUTTON IS ACTIVE
                    self.subsurface.set_alpha(255)  # MAKE IT'S COLOR MORE VIBRANT
                else:
                    self.subsurface.set_alpha(100)
                surface.blit(self.subsurface, self.pos)
                self.subsurface.blit(self.text, (self.width / 4, self.height / 5))

    notesArea = pygame.Surface((sw,700))        # CREATING TWO
    notesArea.fill(colors["beige"])         # AREAS WITH DIFFERENT
                                        # COLORS
    buttonArea = pygame.Surface((sw, 100))
    buttonArea.fill(colors["lavender"])

    letters = []
    j = 0   # TO ALIGN THE LETTERS ON THE SCREEN ( VERTICALLY )
    for number, letter in enumerate(alphabet):
        if number > 12: # TO ALIGN THE LETTERS ON THE SCREEN ( HORIZONTALLY )
            number = number - 13
            j = 1
        letters.append(Button(colors["gray"], (70+number*90,140+j*60), 50, 50, letter))

    languageButtons = []
    counter = 0
    errorCount = 0
    slowo = []
    zdanie = ''
# ENGLISH WORDS

    wordsEN = ["NEW YORK", "WASHINGTON","LAS VEGAS", "CALIFORNIA","TEXAS","MEXICO","LONDON","MANCHESTER","BRIGHTON",
           "FLORIDA","ALABAMA","WEST VIRGINIA","ENGLAND","AMERICA","BRAZİL","CHILE","ARGENTINA","AUSTRALIA",
           "TURKEY","ISTANBUL","GREECE","AFRICA","EGYPT","CHINA","JAPAN","JAPANESE",
           "TABLE","PENCIL","NOTEBOOK","LAPTOP","MIRROR","PLASTIC","INTERNET","GAMING CONSOLE","PLAYSTATION",
           "NINTENDO","NINTENDO SWITCH","APPLE","SAMSUNG","TABLET","BRUSH","WATER","PAPER","PAPER TOWEL",
           "FLAG","GEORGE R R MARTIN","LEONARDO DICAPRIO","HARRY POTTER","PYTHON","PYGAME","CARL SAGAN","COSMOS",
           "STEPHEN HAWKING","BRAD PITT","FELIX KJELLBERG","EINSTEIN","WORKOUT","MARIE CURIE","NEUROSCIENCE",
           "ASTRONOMY","METEORITE","STAR","SOLAR SYSTEM","GALAXY","RANCH SAUCE","CHEDDAR SAUCE","BURGER",
           "BURGER KING","MCDONALDS","CARLS JR","DEODORANT","DOSTOYEVSKI","GAME OF THRONES","COUNTRY","DRAGON",
           "LIZARD","MARK ZUCKERBERG","DUMBLEDORE","GANDALF","MAGICIAN","GOOGLE","MICROSOFT","ARTIFICAL INTELLIGENCE",
           "MACHINE LEARNING","HIGHSCHOOL","UNIVERSITY","OXFORD UNIVERSITY","CAMBRIDGE UNIVERSITY","COMPUTER SCIENCE",
           "WINDOWS","LINUX","LEGEND OF ZELDA","SUPER MARIO ODYSSEY","LAST OF US","HEADPHONES","SONIC THE HEDGEHOG",
           "ATTACK ON TITAN","ONE PIECE","TERMINATOR","AVENGERS","APARTMENT","ANGELINA JOLIE","JENNIFER LAWRENCE",
           "CHRIS HEMSWORTH","CHRIS PRATT","STRANGER THINGS","FULLMETAL ALCHEMIST","ASSASSINS CREED","HEARTHSTONE",
           "GABE NEWELL","PHOTOSHOP","VISUAL STUDIO","HANGMAN","XBOX ONE","HOW I MET YOUR MOTHER","DOG", "CAT",
           "DEATH NOTE","NETFLIX AND CHILL","NETFLIX","ANIMATION","KEYBOARD AND MOUSE","CARBON","DIAMOND","MONA LISA",
           "CRISTIANITY","JEWISH","MUSLIM","PRISONER","TWILIGHT","MAGIC","SPRAY","PAINT","GEORGE","JOHN","ADAM","JENNA",
           "MARK","BOW","ARROW","WATER BOTTLE"]

#else:
    currentLanguage = wordsEN
    currentWord = random.randrange(0, len(currentLanguage))

    guessed = []

    lw = 40 # WIDTH OF THE LINE FOR THE LETTERS
    ls = 10 # SPACE BETWEEN THE LINES

    needRestart = False # FOR CONDITIONS IN WHICH YOU NEED TO RESTART THE GAME, LIKE CHANGING THE LANGUAGE
    winCount = 0
    pointCount = 0
    spaceCount = 0  # COUNTING HOW MANY SPACES A WORD HAS, IT'LL BE IMPORTANT WHEN CHECKING-
    for letter in currentLanguage[currentWord]: # - IF YOU GUESSED THE WORD COMPLETELY.
        if letter == " ":
            spaceCount += 1
    print(len(wordsEN))
#print(len(wordsTR))
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEMOTION:
                for button in letters: # CHECK IF MOUSE IS ON ANY BUTTONS, BUTTON POS GOT BY CALLING GET_RECT()
                    currentRect = button.subsurface.get_rect(topleft = (button.pos[0], button.pos[1]))
                    if currentRect.collidepoint(pg.mouse.get_pos()): # IF COLLIDING WITH MOUSE CURSOR
                        button.rollOver = True      # ONLY HIGHLIGHT A BUTTON IF YOU ARE
                    else:                           # ON IT AND IF YOU AREN'T, STOP HIGHLIGHTING
                        button.rollOver = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: # LEFT MOUSE BUTTON / LEFT CLICK
                    for button in letters:
                        if button.rollOver == True and button.clicked == False: # IF YOU ARE ON THE BUTTON AND IF
                                                                                # THE BUTTON ISN'T CLICKED STILL,
                            button.clicked = True                               # ONLY THEN IT'S CLICKABLE.
                            guessed.append(button.letter)
                            noError = False
                            for letter in currentLanguage[currentWord]:
                                if button.letter == letter:
                                    noError = True
                            if errorCount < 6 and not noError: # IF THAT LETTER ISN'T IN THE WORD, IF NOERROR == FALSE,
                                errorCount += 1                # UP THE ERROR COUNT BY ONE


        if blink.value == 1:
            slowo+=alphabet[counter - 1]
            print(slowo)
            for slowo in slowo:
                guessed.append(slowo)
                noError = False
                for letter in currentLanguage[currentWord]:
                    if slowo == letter:
                        noError = True
                if errorCount < 6 and not noError: # IF THAT LETTER ISN'T IN THE WORD, IF NOERROR == FALSE,
                    errorCount += 1                # UP THE ERROR COUNT BY ONE
                    slowo = list(slowo)
                    slowo.remove(slowo[0])
            blink.value=0

        screen.fill(colors["white"])        # BG COLOR THAT WE WON'T SEE
        screen.blit(notesArea, (0,0))       # TOP PART
        screen.blit(buttonArea, (0, 700))   # BOTTOM PART

        text = font.render(alphabet[counter], True, (0, 128, 0))
        screen.blit(text,
            (100 - text.get_width() // 2, 100 - text.get_height() // 2))
        screen.blit(images[errorCount], (sc[0]-images[errorCount].get_rect().width/2, sc[1]-images[errorCount].get_rect().height/2+70))
    # ^^ THE HANGMAN PICTURES

        for letter in letters:              # DRAWING
            letter.Draw(screen)             # THE BUTTONS
                                        # TO THE

        stats_font = pg.font.SysFont(None, 25, False, True)  # A FONT FOR THE STATS
        winCountText = stats_font.render("TOTAL WINS       : " + str(winCount), True, colors["black"])
        pointCountText = stats_font.render("TOTAL POINTS   : " + str(pointCount), True, colors["black"])
        screen.blit(winCountText, (30, 300))
        screen.blit(pointCountText, (30, 330))

        totalShown = 0  # TOTAL LETTERS SHOWN AT THE BOTTOM PART
        if not needRestart:
            for i,letter in enumerate(currentLanguage[currentWord]):
                text = default_font.render(letter, True, colors["black"])
                posX = (1280 - len(currentLanguage[currentWord]) * (lw + ls))/2 + i * (lw + ls)
                posY = 740
                if letter != " ":
                    pygame.draw.rect(screen, colors["black"], (posX, posY, lw, 3))
                else:
                    pygame.draw.rect(screen, colors["lavender"], (posX, posY, lw, 3))
                if letter in guessed:
                    totalShown += 1
                    screen.blit(text, (posX+lw/3, posY-30))

        pygame.display.update() # UPDATING THE SCREEN AT THIS POINT, ANYTHIGN AFTER THIS WON'T BE SEEN UNTIL
                        # A NEW FRAME STARTS OR I MANUALLY UPDATE IT AGAIN, WHICH I DO AT LINE 239 AND 258

        final_font = pygame.font.SysFont(None, 80)
        lose_text = final_font.render("YOU LOSE", True, colors["darkred"])
        win_text = final_font.render("YOU GUESSED IT", True, colors["darkgreen"])


        if errorCount >= 6 or needRestart:  # IF A RESTART CONDITION IS MET
            if not needRestart:    # But if that condition is not by changing languages: lose.
                screen.blit(lose_text, (500,380))
                pygame.display.update()
                pygame.time.wait(1000)
            guessed.clear() #       RESETTING EVERYTHING            #
            pointCount = 0                                          #
            errorCount = 0                                          #
            winCount = 0                                            #
            for letter in letters:                                  #
                letter.clicked = False                              #
            currentWord = random.randrange(0, len(currentLanguage)) #
            spaceCount = 0                                          #
            for letter in currentLanguage[currentWord]:             #
                if letter == " ":                                   #
                    spaceCount += 1                                 #
            needRestart = False                                     #
            pygame.time.wait(1000)                                      #

        if totalShown == len(currentLanguage[currentWord]) - spaceCount: # IF IT'S A WIN CONDITION
#        sounds["win"].play()
            screen.blit(win_text, (380, 380))
            pygame.display.update()
            pygame.time.wait(1000)
            guessed.clear()
            pointCount += 600 + winCount*10 - errorCount * 100 # POINTS SYSTEM, GAIN FEWER POINTS IF YOU HAD MORE ERRORS
            errorCount = 0
            winCount+=1

            for letter in letters:
                letter.clicked = False
            currentWord = random.randrange(0, len(currentLanguage))
            spaceCount = 0
            for letter in currentLanguage[currentWord]:
                if letter == " ":
                    spaceCount += 1

            pg.time.wait(1000)

        pygame.display.flip() # potrzebne, żeby zielone literki się zmieniały
        clock.tick(2)
        counter=counter+1
        if counter == len(alphabet):
            counter = 0

    '''
        win = visual.Window([400,400])
        message = visual.TextStim(win, text='init')


        message.autoDraw = True
        win.flip()
        core.wait(2.0)

        cnt_blinks = 0
        '''
    '''
        while True:

            print('BLINK!')
            blink.value = 0

                cnt_blinks +=1
                message.setText(str(cnt_blinks))

            win.flip()
            if 'escape' in event.getKeys():
                print('quitting')
                quit_program.set()
                if quit_program.is_set():
                    break
    '''

    # Zakończenie podprocesów
    proc_blink_det.join()
