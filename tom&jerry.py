#tom & jerry game
import pygame,sys,random
from pygame.locals import*

FPS=30
WINDOWWIDTH=600
WINDOWHEIGHT=600
WHITE=(255,255,255)
DARKGRAY=(40,40,40)
BGCOLOR=(WHITE)
MOUSEMINSIZE=10
MOUSEMAXSIZE=60
MOUSEMINSPEED=1
MOUSEMAXSPEED=8
NEWMOUSERATE=6
CATMOVERATE=5
TEXTCOLOR=(255,0,0)

def checkForKeyPress():
    if len(pygame.event.get(QUIT))>0:
        terminate()
    keyUpEvents=pygame.event.get(KEYUP)
    if len(keyUpEvents)==0:
       return None
    if keyUpEvents[0].key==K_ESCAPE:
        terminate()
    return keyUpEvents[0].key
    
def Presskey():
    #render is used to used to write any string in a window in python
    pressKeySurf=BASICFONT.render('press a key to play',True,WHITE)
    pressKeyEsc=BASICFONT.render('press escape key to exit',True,WHITE)
    #get_rect() is used to reserve a rectangle to write in pygame window
    pressKeyRect=pressKeySurf.get_rect()
    pressKeyRec=pressKeyEsc.get_rect()
    pressKeyRect.topright=(WINDOWWIDTH-200,WINDOWHEIGHT-30)
    pressKeyRec.topright=(WINDOWWIDTH-200,WINDOWHEIGHT-50)
    #blit is used to merge a rectangle or figure with a image
    DISPLAYSURF.blit(pressKeySurf,pressKeyRect)
    DISPLAYSURF.blit(pressKeyEsc,pressKeyRec)
def terminate():#to terminate the game
    pygame.quit()
    sys.exit()
def catHitRat(catRect,rats):
    s=0
    for r in rats:
        if catRect.colliderect(r['rect']):
            s+=1
        elif r['rect'].left > WINDOWWIDTH:
            s-=1
        elif s==0:
            break
    return s

def main():    
#set up pygame,the window,and the mouse cursor
  global FPSCLOCK,DISPLAYSURF,BASICFONT
  pygame.init()
  FPSCLOCK=pygame.time.Clock()
  DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
  BASICFONT=pygame.font.SysFont(None,48)
  pygame.display.set_caption('TOM & JERRY')
  pygame.mouse.set_visible(True)
  showStartScreen()
  while True:
      rungame()
      #showGameOverScreen()
      
def showStartScreen():
    flipImage=pygame.image.load('flip.png')
    flipRect=flipImage.get_rect()
    flipRect.center=(WINDOWWIDTH/2,WINDOWHEIGHT/2)
    while True:
        #DISPLAYSURF.fill(BGCOLOR)
        Presskey()
        if checkForKeyPress():
            pygame.event.get()
            return
        DISPLAYSURF.blit(flipImage, flipRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def rungame():
    catImage=pygame.image.load('cat.png')
    catRect=catImage.get_rect()
    ratImage=pygame.image.load('mouse.png')
    #gameOverSound = pygame.mixer.Sound('CHIMES.wav')
    pygame.mixer.music.load('background.mid')
    while True:
        rats=[]
        score=0
        catRect.topleft=(100,WINDOWHEIGHT/2)
        moveLeft=moveRight=moveUp=moveDown=False
        ratcount=0
        pygame.mixer.music.play(-1,0.0)
        while True:
            score+=1
            for event in pygame.event.get():
              if event.type==QUIT:
                    terminate()
              if event.type==KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
              if event.type == KEYUP:
                if event.key == K_ESCAPE:
                        terminate()
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
              if event.type == MOUSEMOTION:
                # If the mouse moves, move the cat where the cursor is.
                catRect.move_ip(event.pos[0] - catRect.centerx, event.pos[1] - catRect.centery)
            ratcount+=1
            if ratcount == NEWMOUSERATE:
                 ratcount=0
                 ratSize=random.randint(MOUSEMINSIZE,MOUSEMAXSIZE)
                 newRat = {'rect': pygame.Rect(0-ratSize, random.randint(0,WINDOWHEIGHT-ratSize), ratSize, ratSize),
                          'speed': random.randint(MOUSEMINSPEED, MOUSEMAXSPEED),
                          'surface':pygame.transform.scale(ratImage, (ratSize, ratSize)),
                          }
                 rats.append(newRat)
            if moveLeft and catRect.left > 0:
              catRect.move_ip(-1 * CATMOVERATE, 0)
            if moveRight and catRect.right < WINDOWWIDTH:
              catRect.move_ip(CATMOVERATE, 0)
            if moveUp and catRect.top > 0:
              catRect.move_ip(0, -1 * CATMOVERATE)
            if moveDown and catRect.bottom < WINDOWHEIGHT:
              catRect.move_ip(0, CATMOVERATE)
            pygame.mouse.set_pos(catRect.centerx, catRect.centery)
            for r in rats:
                           r['rect'].move_ip(r['speed'],0)
            #for r in rats[:]:
                           #if r['rect'].left > WINDOWWIDTH:
                             #rats.remove(r)
            DISPLAYSURF.fill(BGCOLOR)
            drawText('Score: %s' % (score), BASICFONT, DISPLAYSURF, 10, 0)                
            DISPLAYSURF.blit(catImage, catRect)
            for r in rats:
              DISPLAYSURF.blit(r['surface'], r['rect'])                 
            pygame.display.update()
            score=catHitRat(catRect,rats)
            if score<=1:
               break
            mainClock.tick(FPS)
        pygame.mixer.music.stop()                 
        pygame.display.update()
        checkForKeyPress()
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
if __name__=='__main__':
    #calling main function
    main()
