#Norika Upadhyaya
#Emojicrush.py
#In this game, an 8x8 board will be filled with emojis. Users will be able to swipe in order to get matches of 3,4 or 5 in a row as well as in an L-shaped or T-shaped.
#If they get a match, they will get points with 3 in a row worth 50, 4 in a row and L-shaped and T-shaped matches worth 250, 5 in a row worth 500.
#Each level also has its own goal that must be achieved in order to complete the level
#level 1 - score 1500 points in 30 moves
#level 2 - score 2500 points in under one minute
#level 3 - get the cherry to the bottom in 30 moves
#level 4 - clear all red cells in 30 moves
#Additionally, there is also a main menu as well as a how to play screen and clicking the X in the top left takes user to the previous screen.
from pygame import*
from os import environ
from random import*
from filledRect import roundedRect#makes rectangles with rounded corners for aesthetic reasons

init()
inf = display.Info()
cen=(inf.current_w-1000)/2 #finds the x coordinate so that the screen can be centered (this is how much distance there'll be from the left and right corner of computer screen to the left and right corner (respectively)of the paint program screen)
environ['SDL_VIDEO_WINDOW_POS'] = '%d,25'%cen 
display.set_caption("Emoji Crush")
screen = display.set_mode((1000,700))
display.set_icon(image.load("images/emojis/emoji1.png"))#icon will show in the corner

emojis = [image.load("images/emojis/emoji"+str(i+1)+".png") for i in range(6)]#list of all emojis
board = [[choice(emojis) for j in range(8)] for i in range(8)]#randomly generated list where emojis will be on the board
boardRect = [[Rect(i*66+45,j*66+140,66,66) for j in range(8)] for i in range(8)]#creates a Rect object for each emoji on the board

#background images
mainBG = image.load("images/mainBG.jpg")
HTPbg = image.load("images/HTP_bg.png")
levelsBG = image.load("images/levelsbg.png")
gameBG = image.load("images/gameBG.png")
title = image.load("images/title.png")

#font
font.init()
font30 = font.Font("Cooper Black Regular.ttf",30)
font120 = font.Font("Cooper Black Regular.ttf",120)

def drawboard():#displays emojis and cell backgrounds on the board
    for i in range(len(board)):
        for j in range(len(board[i])):
            if level == 4:
                if (i,j) in red:
                    roundedRect(screen,(i*66+45,j*66+140,64,64),(115,0,0),0.5)#makes some cell backgrounds red
                else:
                    roundedRect(screen,(i*66+45,j*66+140,64,64),(74,141,202),0.5)#other cell backgrounds are the normal blue
            else:
                roundedRect(screen,(i*66+45,j*66+140,64,64),(74,141,202),0.5)#cell backgrounds
            screen.blit(board[i][j],(i*66+46,j*66+141))#displays all emojis on the board
            
def swipe():#this function 
    startingi = (sx-46)//66 #board starts at (46,141) and each cell has a width and height of 66px
    startingj = (sy-141)//66
    endingi = (ex-46)//66
    endingj = (ey-141)//66
    
    if startingi<0 or startingi>=8 or startingj<0 or startingj>=8 or endingi<0 or endingi>=8 or endingj<0 or endingj>=8:
        startingi = 0#if it's not on the board, then it makes sure startingi==endingi in not True
        endingi = 7
        startingj = 0
        endingj = 7

    start = board[startingi][startingj]
    end = board[endingi][endingj]
    
    if startingi == endingi:#if in the same row
        if startingj == endingj-1 or startingj == endingj+1:#checks if starting and ending are next to each other
            board[startingi][startingj] = end#the emoji on the start changes to the emoji on the end and vise versa
            board[endingi][endingj] = start
            
            drawboard() #shows the swipe but will revert back if it does not result in a match
            time.wait(50) #there will be a slight delay
            
            if checkMatch():
                move()#if it is a match, the user will have used up one move

                if level == 3:#if the cherry was swiped, the i position would change
                    global cherryi,cherryj
                    if board[cherryi][cherryj] == start:
                        cherryi = startingi
                        cherryj = startingj
                    elif board[cherryi][cherryj] == end:
                        cherryi = endingi
                        cherryj = endingj
            else:
                board[startingi][startingj] = start
                board[endingi][endingj] = end
                
    if startingj == endingj:#if in the same column
        if startingi == endingi-1 or startingi == endingi+1:
            board[startingi][startingj] = end
            board[endingi][endingj] = start
            
            drawboard()
            time.wait(50)
            
            if checkMatch():
                move()

                if level == 3:
                    if board[cherryi][cherryj] == start:
                        cherryi = endingi
                        cherryj = endingj
                    elif board[cherryi][cherryj] == end:
                        cherryi = startingi
                        cherryj = startingj
            else:
                board[startingi][startingj] = start
                board[endingi][endingj] = end

def checkMatch():#checks if and what kind of matches the emojis make and gives points based on that
    for i in range(4):
       for j in range(8):
           if board[i][j] == board[i+1][j] and board[i+1][j] == board[i+2][j] and board[i+2][j] == board[i+3][j] and board[i+3][j] == board[i+4][j]:#horizontal five
               for k in range(j,0,-1):#emojis fall
                   board[i][k] = board[i][k-1]
                   board[i+1][k] = board[i+1][k-1]
                   board[i+2][k] = board[i+2][k-1]
                   board[i+3][k] = board[i+3][k-1]
                   board[i+3][k] = board[i+4][k-1]
                   
               board[i][0] = choice(emojis)#new random emojis come out the top
               board[i+1][0] = choice(emojis)
               board[i+2][0] = choice(emojis)
               board[i+3][0] = choice(emojis)
               board[i+4][0] = choice(emojis)
 
               if level == 3:
                    global cherryj
                    if i == cherryi or i+1 == cherryi or i+2 == cherryi or i+3 == cherryi or i+4 == cherryi:
                        if j>cherryj:
                            cherryj += 1#cherry will fall if emojis are matched under it

               if level == 4:
                   for m in range(5):
                       if (i+m,j) in red:
                           red.remove((i+m,j))#red cell goes away if emojis are matched on top of it
                           point(50)
               
               point(500)
               return True
    for i in range(8):
        for j in range(4):
            if board[i][j] == board[i][j+1] and board[i][j+1] == board[i][j+2] and board[i][j+2] == board[i][j+3] and board[i][j+3] == board[i][j+4]:#vertical five
                for k in range(j,0,-1):
                    board[i][k] = board[i][k-5]
                    board[i][k+1] = board[i][k-4]
                    board[i][k+2] = board[i][k-3]
                    board[i][k+3] = board[i][k-2]
                    board[i][k+4] = board[i][k-1]
                    
                board[i][0] = choice(emojis)
                board[i][1] = choice(emojis)
                board[i][2] = choice(emojis)
                board[i][3] = choice(emojis)
                board[i][5] = choice(emojis)

                if level == 3:
                    if i == cherryi:
                        if j>cherryj:
                            cherryj += 5

                if level == 4:
                   for m in range(5):
                       if (i,j+m) in red:
                           red.remove((i,j+m))
                           point(50)

                point(500)
                return True
    for i in range(5):
       for j in range(8):
           if board[i][j] == board[i+1][j] and board[i+1][j] == board[i+2][j] and board[i+2][j] == board[i+3][j]:#horizontal four
               for k in range(j,0,-1):
                   board[i][k] = board[i][k-1]
                   board[i+1][k] = board[i+1][k-1]
                   board[i+2][k] = board[i+2][k-1]
                   board[i+3][k] = board[i+3][k-1]
                   
               board[i][0] = choice(emojis)
               board[i+1][0] = choice(emojis)
               board[i+2][0] = choice(emojis)
               board[i+3][0] = choice(emojis)

               if level == 3:
                    if i == cherryi or i+1 == cherryi or i+2 == cherryi or i+3 == cherryi or i+4 == cherryi:
                        if j>cherryj:
                            cherryj += 1

               if level == 4:
                  for m in range(4):
                      if (i+m,j) in red:
                          red.remove((i+m,j))
                          point(50)
               
               point(250)
               return True
    for i in range(8):
       for j in range(5):
           if board[i][j] == board[i][j+1] and board[i][j+1] == board[i][j+2] and board[i][j+2] == board[i][j+3]:#vertical four
               for k in range(j,0,-1):
                   board[i][k] = board[i][k-4]
                   board[i][k+1] = board[i][k-3]
                   board[i][k+2] = board[i][k-2]
                   board[i][k+3] = board[i][k-1]
                   
               board[i][0] = choice(emojis)
               board[i][1] = choice(emojis)
               board[i][2] = choice(emojis)
               board[i][3] = choice(emojis)

               if level == 3:
                    if i == cherryi:
                        if j>cherryj:
                            cherryj += 4

               if level == 4:
                  for m in range(4):
                      if (i,j+m) in red:
                          red.remove((i,j+m))
                          point(50)
               
               point(250)
               return True
    for i in range(6):
        for j in range(6):
            if board[i][j] == board[i+1][j] and board[i+1][j] == board[i+2][j]:#L-shaped matches(top)
                for m in range(3):
                    if board[i+m][j] == board[i+m][j+1] and board[i+m][j+1] == board[i+m][j+2]:
                        for k in range(j,0,-1):
                            board[i][k] = board[i][k-1]
                            board[i+1][k] = board[i+1][k-1]
                            board[i+2][k] = board[i+2][k-1]
                            
                            board[i+m][k+1] = board[i+m][k-2]
                            board[i+m][k+2] = board[i+m][k-1]

                        board[i][0] = choice(emojis)
                        board[i+1][0] = choice(emojis)
                        board[i+2][0] = choice(emojis)
                        
                        board[i+m][1] = choice(emojis)
                        board[i+m][2] = choice(emojis)

                        if level == 3:
                            if i == cherryi or i+1 == cherryi or i+3 == cherryi:
                                if j>cherryj:
                                    cherryj += 1
                            if i+m == cherryi:
                                if j>cherryj:
                                    cherryj +=2

                        if level == 4:
                            if (i+m,j) in red:
                                red.remove((i+m,j))
                                point(50)
                        
                        point(250)
                        return True

            elif board[i][j+1] == board[i+1][j+1] and board[i+1][j+1] == board[i+2][j+1]:#L-shaped matches(middle)
                for m in range(3):
                    if board[i+m][j] == board[i+m][j+1] and board[i+m][j+1] == board[i+m][j+2]:
                        for k in range(j+1,0,-1):
                            board[i][k] = board[i][k-1]
                            board[i+1][k] = board[i+1][k-1]
                            board[i+2][k] = board[i+2][k-1]
                            
                            board[i+m][k] = board[i+m][k-3]
                            board[i+m][k+1] = board[i+m][k-2]

                        board[i][0] = choice(emojis)
                        board[i+1][0] = choice(emojis)
                        board[i+2][0] = choice(emojis)
                        
                        board[i+m][1] = choice(emojis)
                        board[i+m][2] = choice(emojis)

                        if level == 3:
                            if i == cherryi or i+1 == cherryi or i+3 == cherryi:
                                if j>cherryj:
                                    cherryj += 1
                            if i+m == cherryi:
                                if j>cherryj:
                                    cherryj +=2

                        if level == 4:
                            if (i+m,j+1) in red:
                                red.remove((i+m,j+1))
                                point(50)
                        
                        point(250)
                        return True

            elif board[i][j+2] == board[i+1][j+2] and board[i+1][j+2] == board[i+2][j+2]:#L-shaped matches(bottom)
                for m in range(3):
                    if board[i+m][j] == board[i+m][j+1] and board[i+m][j+1] == board[i+m][j+2]:
                        for k in range(j+1,0,-1):
                            board[i][k] = board[i][k-1]
                            board[i+1][k] = board[i+1][k-1]
                            board[i+2][k] = board[i+2][k-1]
                            
                            board[i+m][k-1] = board[i+m][k-3]
                            board[i+m][k] = board[i+m][k-2]

                        board[i][0] = choice(emojis)
                        board[i+1][0] = choice(emojis)
                        board[i+2][0] = choice(emojis)
                        
                        board[i+m][1] = choice(emojis)
                        board[i+m][2] = choice(emojis)

                        if level == 3:
                            if i == cherryi or i+1 == cherryi or i+3 == cherryi:
                                if j>cherryj:
                                    cherryj += 1
                            if i+m == cherryi:
                                if j>cherryj:
                                    cherryj +=2

                        if level == 4:
                            if (i+m,j+2) in red:
                                red.remove((i+m,j+2))
                                point(50)
                        
                        point(250)
                        return True                    
    for i in range(6):
        for j in range(8):
            if board[i][j] == board[i+1][j] and board[i+1][j] == board[i+2][j]:#horizontal three
                for k in range(j,0,-1):
                    board[i][k] = board[i][k-1]
                    board[i+1][k] = board[i+1][k-1]
                    board[i+2][k] = board[i+2][k-1]
                    
                board[i][0] = choice(emojis)
                board[i+1][0] = choice(emojis)
                board[i+2][0] = choice(emojis)

                if level == 3:
                    if i == cherryi or i+1 == cherryi or i+3 == cherryi:
                        if j>cherryj:
                            cherryj += 1

                if level == 4:
                   for m in range(3):
                       if (i+m,j) in red:
                           red.remove((i+m,j))
                           point(50)

                point(50)
                return True
    for i in range(8):
        for j in range(6):
            if board[i][j] == board[i][j+1] and board[i][j+1] == board[i][j+2]:#vertical three
                for k in range(j,0,-1):
                    board[i][k] = board[i][k-3]
                    board[i][k+1] = board[i][k-2]
                    board[i][k+2] = board[i][k-1]
                    
                board[i][0] = choice(emojis)
                board[i][1] = choice(emojis)
                board[i][2] = choice(emojis)

                if level == 3:
                    if i == cherryi:
                        if j>cherryj:
                            cherryj += 3

                if level == 4:
                   for m in range(3):
                       if (i,j+m) in red:
                           red.remove((i,j+m))
                           point(50)

                point(50)
                return True
    return False

points = 0
def point(increase):#how much to increase the points
    global points
    points+=increase

moves = 30
def move():#will remove 1 from number of moves left every time a user makes a move
    global moves
    moves -= 1
    if moves <= 0:#if user runs out of moves, gameover screen is displayed
        global gamemode
        gamemode = 5

def win():#screen that shows if user beats a level
    screen.fill((74,141,202))
    screen.blit(font120.render("Congratulations",True,(255,255,255)),(0,100))
    screen.blit(font30.render("You reached the goal!",True,(255,255,255)),(328,300))
    screen.blit(font30.render("You earned "+str(points)+" points!",True,(255,255,255)),(320,382))#shows how many points user got that round
    global gamemode,level

    menuRect = Rect(200,475,250,85)#Rect object for main menu button
    draw.ellipse(screen,(255,255,255),menuRect,5)
    screen.blit(font30.render("Main Menu",True,(255,255,255)),(235,500))
    if menuRect.collidepoint(mx,my):#if user hovers over button, it will be highlighted in gray
        draw.ellipse(screen,(111,111,111),menuRect,5)
        screen.blit(font30.render("Main Menu",True,(111,111,111)),(235,500))
        if mb[0] == 1:#if user clicks main menu button, it will go to main menu screen
            reset()
            gamemode = 0

    nextLevel = Rect(550,475,250,85)#Rect object for next level button
    draw.ellipse(screen,(255,255,255),nextLevel,5)
    screen.blit(font30.render("Next Level",True,(255,255,255)),(590,500))
    if nextLevel.collidepoint(mx,my):
        draw.ellipse(screen,(111,111,111),nextLevel,5)
        screen.blit(font30.render("Next Level",True,(111,111,111)),(590,500))
        if mb[0] == 1:#if user clicks next level button, it will go one level up
            if level == 4:#if it is the last level, it will go to the levels screen
                gamemode = 1
            else:
                level+=1
                reset()
                gamemode = 2

def gameOver():#screen that shows when user doesn't complete the goal within the move/time limit
    screen.fill((74,141,202))
    screen.blit(font120.render("You ran out of",True,(0,0,0)),(65,100))
    if level == 2:#if level two, the user ran out of time, otherwise they ran out of moves
        screen.blit(font120.render("time!",True,(0,0,0)),(345,250))
    else:
        screen.blit(font120.render("moves!",True,(0,0,0)),(295,250))
    global gamemode
    
    retry = Rect(200,475,250,85)#Rect object for retry button
    screen.blit(font30.render("Retry",True,(0,0,0)),(275,500))
    draw.ellipse(screen,(0,0,0),retry,5)
    if retry.collidepoint(mx,my):
        screen.blit(font30.render("Retry",True,(111,111,111)),(275,500))
        draw.ellipse(screen,(111,111,111),retry,5)
        if mb[0] == 1:#the user will be able to retry the level in order to complete it
            reset()
            gamemode = 2

    Exit = Rect(550,475,250,85)#Rect object for exit button
    screen.blit(font30.render("Exit",True,(0,0,0)),(640,500))
    draw.ellipse(screen,(0,0,0),Exit,5)
    if Exit.collidepoint(mx,my):
        screen.blit(font30.render("Exit",True,(111,111,111)),(640,500))
        draw.ellipse(screen,(111,111,111),Exit,5)
        if mb[0] == 1:#will take user to main menu
            reset()
            gamemode = 0

def reset():#resets all variables in order to make a new game
    global moves,points,board
    moves = 30
    points = 0
    board = [[choice(emojis) for j in range(8)] for i in range(8)]

    global initTime,cherryi,cherryj,red
    if level == 2:
        initTime = time.get_ticks()#gets what time the level started in order to calculate how much time there is left on the timer

    if level == 3:
        cherryi = randint(0,7)#keeps track of the location of the cherry on the board
        cherryj = 0
        board[cherryi][cherryj] = image.load("images/emojis/cherry.png")#replaces emojis with a cherry at the top of the board with a randomized x-coordinate

    if level == 4:#makes all the proper cell background red again in case user got rid of some in the previous round
        red = [(0,3),(0,4),(0,5),(0,6),(0,7),(1,4),(1,5),(1,6),(1,7),(2,5),(2,6),(2,7),(3,6),(3,7),(4,6),(4,7),(5,5),(5,6),(5,7),(6,4),(6,5),(6,6),(6,7),(7,3),(7,4),(7,5),(7,6),(7,7)]

def sideBar():#what displays on the sidebar
    if level == 2:#on level 2, displays timer, otherwise displays moves left
        screen.blit(font30.render("Time:",True,(255,255,255)),(752,70))
        screen.blit(font120.render(str(timer),True,(255,255,255)),(728,70))
    else:
        screen.blit(font30.render("Moves:",True,(255,255,255)),(752,70))
        screen.blit(font120.render(str(moves),True,(255,255,255)),(728,70))
        
    screen.blit(font30.render("Points:",True,(255,255,255)),(665,350))
    screen.blit(font30.render(str(points),True,(255,255,255)),(775,350))#shows user how many points they have
    progress = int((points/maxpoints)*270)#270px is how long the progress bar is, maxpoints is how many points you need to fill it up for that level
    if progress<30:#if it is under 30, the progress bar is too narrow
        progress = 30
    if progress>270:#if it goes over 270, it surpasses the progress bar
        progress = 270
    roundedRect(screen,(660,400,280,40),(0,0,0),1)
    roundedRect(screen,(665,405,270,30),(74,141,202),1)#to make an outline
    roundedRect(screen,(665,405,progress,30),(0,100,0),1)

def levelselect():#where user can select a level
    screen.blit(levelsBG,(0,0))
    global gamemode,level

    level1Rect = Rect(153,61,272,248)
    if level1Rect.collidepoint(mx,my):
        roundedRect(screen,level1Rect,(111,111,111),0.2)#fills rectangle to show which level user is hovering on
        screen.blit(font120.render("1",True,(0,0,0)),(250,110))#highlights which level the user is hovering over
        if mb[0] == 1:
            level = 1#goes to whichever level the user clicked on
            gamemode = 2#goes to the playing screen
            
    level2Rect = Rect(583,59,272,248)
    if level2Rect.collidepoint(mx,my):
        roundedRect(screen,level2Rect,(111,111,111),0.2)
        screen.blit(font120.render("2",True,(0,0,0)),(680,110))
        if mb[0] == 1:
            global initTime
            initTime = time.get_ticks()#gets what time the level started in order to calculate how much time there is left on the timer
            level = 2
            gamemode = 2
            
    level3Rect = Rect(151,375,269,257)
    if level3Rect.collidepoint(mx,my):
        roundedRect(screen,level3Rect,(111,111,111),0.2)
        screen.blit(font120.render("3",True,(0,0,0)),(250,425))
        if mb[0] == 1:
            global cherryi,cherryj
            cherryi = randint(0,7)#keeps track of the location of the cherry on the board
            cherryj = 0
            board[cherryi][cherryj] = image.load("images/emojis/cherry.png")
            level = 3
            gamemode = 2
    
    level4Rect = Rect(582,376,269,257)
    if level4Rect.collidepoint(mx,my):
        roundedRect(screen,level4Rect,(111,111,111),0.2)
        screen.blit(font120.render("4",True,(0,0,0)),(680,425))
        if mb[0] == 1:
            global red#indices of the red cells
            red = [(0,3),(0,4),(0,5),(0,6),(0,7),(1,4),(1,5),(1,6),(1,7),(2,5),(2,6),(2,7),(3,6),(3,7),(4,6),(4,7),(5,5),(5,6),(5,7),(6,4),(6,5),(6,6),(6,7),(7,3),(7,4),(7,5),(7,6),(7,7)]
            level = 4
            gamemode = 2

def playing():#runs all the functions required during gameplay
    screen.blit(gameBG,(0,0))
    screen.blit(title,(45,35))#displays title on the top

    if level == 1:#runs appropriate level function
        level1()
    elif level == 2:
        level2()
    elif level == 3:
        level3()
    elif level == 4:
        level4()
        
    drawboard()
    swipe()
    checkMatch()
    sideBar()

def level1():
    global maxpoints,gamemode,points
    maxpoints = 1500#the progress bar will be full when user reaches 1500 points
    screen.blit(font30.render("Get 1500 points",True,(255,255,255)),(665,250))#displays goal on sidebar
    
    if points>1500:#if user attains 1500 points, winning screen is displayed
        points += moves*50#user gets 50 additional points for each move they did not use
        gamemode = 4
        
def level2():
    global maxpoints,gamemode,points,timer,initTime
    maxpoints = 2500#the progress bar will be full when user reaches 1500 points
    moves = 1#so that the moves don't interfere
    timer = (60000 - (time.get_ticks() - initTime))//1000#countdown from 60 seconds, shows only seconds without milliseconds
    screen.blit(font30.render("Get 2500 points",True,(255,255,255)),(665,250))
    
    if points>2500:#if user attains 2500 points, winning screen is displayed
        points += timer*25#user get 25 additional points for each second they didn't use
        gamemode = 4

    if timer<=0:#if the timer runs out, game over screen is displayed
        gamemode = 5

def level3():
    global maxpoints,gamemode,points,cherryi,cherryj
    maxpoints = 7500#the progress bar will be full when user reaches 7500 points
    screen.blit(font30.render("Get the cherry",True,(255,255,255)),(665,250))
    screen.blit(font30.render("to the bottom",True,(255,255,255)),(665,280))

    if cherryj >= 7:#if the cherry reaches the bottom, winning screen is displayed
        points += moves*50
        gamemode = 4

def level4():
    global maxpoints,gamemode,points
    maxpoints = 10000#the progress bar will be full when user reaches 10000 points
    screen.blit(font30.render("Clear all red cells",True,(255,255,255)),(660,250))
    
    if len(red) == 0:#if there are no red cells left, winning screen is displayed
        points += moves*50
        gamemode = 4

def mainMenu():#main menu screen
    screen.blit(mainBG,(0,0))
    global gamemode

    #displays options
    playingRect = Rect(180,585,250,90)
    draw.ellipse(screen,(255,255,255),playingRect,5)
    screen.blit(font30.render("Play",True,(255,255,255)),(270,615))
    HTPRect = Rect(595,585,250,90)
    draw.ellipse(screen,(255,255,255),HTPRect,5)
    screen.blit(font30.render("How to play",True,(255,255,255)),(625,615))

    global move,enter,mode
        
    if mode == "play":
        draw.ellipse(screen,(111,111,111),playingRect,5)#highlights whichever option user has chose with their arrow keys
        screen.blit(font30.render("Play",True,(111,111,111)),(270,615))
        draw.ellipse(screen,(255,255,255),HTPRect,5)#unhighlights the option that is not chosen
        screen.blit(font30.render("How to play",True,(255,255,255)),(625,615))
    
    elif mode == "HTP":
        draw.ellipse(screen,(111,111,111),HTPRect,5)
        screen.blit(font30.render("How to play",True,(111,111,111)),(625,615))
        draw.ellipse(screen,(255,255,255),playingRect,5)
        screen.blit(font30.render("Play",True,(255,255,255)),(270,615))
            
    if enter:
        if mode == "play":#if user presses enter key, it will go to the screen they chose
            gamemode = 1
        elif mode == "HTP":
            gamemode = 3

def HTP():
    screen.blit(HTPbg,(0,0))

gamemode = 0

sx,sy = (0,0)
ex,ey = (0,0)
enter = False#whether or not the user has pressed the enter key in the main menu
mode = "play"#main menu starts at play, user can then change it
running = True
while running:
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN:
           if e.button == 1:#left click
               sx,sy = e.pos
        if e.type == MOUSEBUTTONUP:
            ex,ey = e.pos
            sx,sy =(0,0)#sets sx,sy to (0,0) so that swipe() stops moving the emojis
            
        if e.type == KEYDOWN:
            if e.key == K_RIGHT:#if the right arrow is pressed, the "how to play" option will be highlighted
                mode = "HTP"
            if e.key == K_LEFT:#if the left arrow is pressed, the "play" option will be highlighted
                mode = "play"
            if e.key == K_RETURN:#if enter is pressed, the screen will change to the highlighted option
                enter = True
                
        if e.type == KEYUP:
            if e.key == K_RETURN:#if the enter key is unpressed, the enter key won't be True anymore
                enter = False
                
        if e.type == QUIT:#if the x is clicked
            if gamemode == 3:#if the screen is at how to play, it will go to the main menu 
                gamemode = 0
            elif gamemode == 0 or gamemode == 4 or gamemode == 5:#if at the main menu, game over screen, or winning screen, the game will exit
                running = False
            else:#otherwise it will change to the previous screen
                gamemode -=1
                reset()
                
    mx,my = mouse.get_pos()#x and y coordinates of the mouse
    mb = mouse.get_pressed()#checks whether mouse has clicked
#----------------------------
    if gamemode == 0:#checks what the gamemode is and runs the appropriate function
        mainMenu()
    elif gamemode == 1:
        levelselect()
    elif gamemode == 2:
        playing()
    elif gamemode == 3:
        HTP()
    elif gamemode == 4:
        win()
    elif gamemode == 5:
        gameOver()

    print(mx,my)
#----------------------------
    display.flip()
quit()
