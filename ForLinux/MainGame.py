# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 08:41:18 2016

author: TomZhou
"""

import pygame
from pygame.locals import *
from sys import exit
import random
from math import *
import time

Font=""
UI=""
Window=""
MapPreview=""

WindowWidth=300
WindowHeight=300

BoardWidth=20
BoardHeight=20
AreaHeight=36
AreaWidth=36
HomeNum=2

Home1=""
Home2=""
Home3=""
Home4=""
Map=""

MINNUM=-1000000
dx=(-1,1,1,0,-1,-1,-1,0,1,0)
dy=(-1,0,1,1,1,0,-1,-1,-1,0)

Red=(220, 10, 10)
Blue=(70, 130, 180)
Gold=(218, 165, 32)
Purple=(150, 32, 220)
Green=(50, 205, 50)
Grey=(60, 60, 60)
Yellow=(208,148,22)
Black=(4,4,4)

StartButtonInfo=()
QuitButtonInfo=()
HelpButtonInfo=()
WidthAddButtonInfo=()
WidthSubstractButtonInfo=()
HeightAddButtonInfo=()
HeightSubstractButtonInfo=()
HomeNumAddButtonInfo=()
HomeNumSubstractButtonInfo=()
GenButtonInfo=()
BackButtonInfo=()
ACButtonInfo=()
NewButtonInfo=()
LoadButtonInfo=()
Count=1

##########BoardArea##############################
class BoardArea:
    def __init__(self):
        self.Name=""
        self.Empty=True
        self.Mount=False
        self.Water=False
        self.Height=MINNUM
        self.Belong=0
        self.Border=True
        self.FlagPlace=False

    def MoveToHere(self, OldHeight, ID):
        if Name == "Hell":
            return "CONNOT"
        elif Empty == False:
            if Belong == ID:#You cannot kill your own army
                return "WRONGPOS"
            elif Name == "Castle":
                Belong=ID
                Empty=False
                return "SUCCEED"
            elif Water == True:
                if OldHeight < Height and OldHeight < 0:#If from water to water (Go up)
                    if Height-OldHeight <= 5:
                        Belong=ID
                        Empty=False
                        return "SUCCEED"
                    else:
                        return "TOOQUICKUP"#This means your lungs cannot bear it!
                elif Height > OldHeight and OldHeight < 0:#If from water to water (Go Down)
                    if OldHeight-Height <= 5:
                        Belong=ID
                        Empty=False
                        return "SUCCEED"
                    else:
                        return "TOOQUICKDOWN"#This ALSO means your lungs cannot bear it!
                else:#If from mountain to water
                    if Height >=-5:#Means you can jump and survive.
                        Belong=ID
                        Empty=False
                        return "SUCCEED"
                    else:
                        return "TOODEEPWATER"
            elif Mount == True:
                if OldHeight >= Height:#If from mountain to mountain (Go Down)
                    if OldHeight-Height <= 5:
                        Belong=ID
                        Empty=False
                        return "SUCCEED"
                    else:
                        return "TOODEEPDOWN"#This means your legs cannot bear it!
                elif OldHeight <= Height and OldHeight >= 0:#If from mountain to mountain (Go Up)
                    if Height-OldHeight <= 5:
                        Belong=ID
                        Empty=False
                        return "SUCCEED"
                    else:
                        return "TOOHIGHUP"#This means you cannot climb up
                elif OldHeight < 0:#If from Water to mountain
                    if Height > 5 and OldHeight >= -5:
                        return "TOOHIGHUP"#This means although you can swim to the
                    #top of water, you cannot climb up.
                    elif Height <= 5 and OldHeight < -5:
                        return "TOODEEPTOSWIM"#This means although the moutain isn't
                    #high, you cannot swim to the top of the water
                    elif Height <=5 and OldHeight >=-5:
                        Belong=ID
                        Empty=False
                        return "SUCCEED"
                    else:
                        return "MOUNTTOOHIGHWATERTOODEEP"
                elif Name == "Home" and ID != Belong:
                    Belong=ID
                    Empty=False
                    return "WIN"
                else:
                    return "ERROR"

##########CreateButton##############################
def CreateButton((Left, Top, Width, Height, BackGroundColor, StrColor),#Notice that this is a tuple
                 Caption, CaptionFont, CaptionHeight,
                 Window, Language):
    
    Cap=CaptionFont.render(Caption,
                    True,
                    (StrColor))

    pygame.draw.rect(Window,
                     BackGroundColor,
                     (Left,Top,Width,Height),
                     0)
    if Language == "Chinese":
        CapLen=(len(Caption)/2)*CaptionHeight
    elif Language == "English":
        CapLen=len(Caption)*CaptionHeight
    else:
        print "Error!"
        
    CapLeft=Left+(Width-CapLen)//2
    CapTop=Top+(Height-CaptionHeight)//2
    Window.blit(Cap, (CapLeft, CapTop))

##########ButtonPressed##############################
def ButtonPressed((Left, Top, Width, Height), MousePos):
    if MousePos[0] > Left and MousePos[1] > Top and MousePos[0] < Left+Width and MousePos[1] < Top+Height:
        return True
    
def InitBoard(CastleNum,HellNum,HomeNum):

    rand1=0
    rand2=0
    rand3=0

    Board=[[] for i in range(BoardHeight+2)]

    for i in range(BoardHeight+2):
        for j in range(BoardWidth+2):
            tmp=BoardArea()
            Board[i].append(tmp)
    for i in range(1, BoardHeight+1):
        for j in range(1, BoardWidth+1):
            Board[i][j].Border=False #This was set to True in the class BoardArea

    #There should be at least 2 players, so the program creates 2 places for home at first
    #And then it decides if it should add some
    for i in range(1,10):#From 1 to 9
            Board[2+dx[i]][2+dy[i]].Name="Home"
            Board[2+dx[i]][2+dy[i]].Belong=1
            Board[2+dx[i]][2+dy[i]].Empty=False

            if 2+dx[i] == 1 and 2+dy[i] == 1:
                Board[2+dx[i]][2+dy[i]].FlagPlace=True
    for i in range(1,10):#From 1 to 9
            Board[BoardHeight-1+dx[i] ][BoardWidth-1+dy[i]].Name="Home"
            Board[BoardHeight-1+dx[i]][BoardWidth-1+dy[i]].Belong=2
            Board[BoardHeight-1+dx[i]][BoardWidth-1+dy[i]].Empty=False

            if BoardHeight-1+dx[i] == BoardHeight-2 and BoardWidth-1+dy[i] == BoardWidth-2:
                Board[BoardHeight-1+dx[i]][BoardWidth-1+dy[i]].FlagPlace=True

    if HomeNum == 3:
        for i in range(1,10):#From 1 to 9
            Board[BoardHeight-1+dx[i]][2+dy[i]].Name="Home"
            Board[BoardHeight-1+dx[i]][2+dy[i]].Belong=3
            Board[BoardHeight-1+dx[i]][2+dy[i]].Empty=False

            if BoardHeight-1+dx[i] == BoardHeight-2 and 2+dy[i] == 1:
                Board[BoardHeight-1+dx[i]][2+dy[i]].FlagPlace=True
    if HomeNum == 4:
        for i in range(1,10):#From 1 to 9
            Board[BoardHeight-1+dx[i]][2+dy[i]].Name="Home"
            Board[BoardHeight-1+dx[i]][2+dy[i]].Belong=3
            Board[BoardHeight-1+dx[i]][2+dy[i]].Empty=False

            if BoardHeight-1+dx[i] == BoardHeight-2 and 2+dy[i] == 1:
                Board[BoardHeight-1+dx[i]][2+dy[i]].FlagPlace=True
        for i in range(1,10):#From 1 to 9
            Board[2+dx[i]][BoardWidth-1+dy[i]].Name="Home"
            Board[2+dx[i]][BoardWidth-1+dy[i]].Belong=4
            Board[2+dx[i]][BoardWidth-1+dy[i]].Empty=False

            if 2+dx[i] == 1 and BoardWidth-1+dy[i] == BoardWidth-2:
                Board[2+dx[i]][BoardWidth-1+dy[i]].FlagPlace=True
                
    #create Board
    for i in range(1,BoardHeight+1):
        for j in range(1,BoardWidth+1):
            rand1=random.randint(1,2)
            rand2=random.randint(-5,14)
            rand3=random.randint(-4,10)

            if rand1 == 1 and rand2 > 10 and rand3 < 2 and Board[i][j].Empty and CastleNum > 0:
                Board[i][j].Name="Castle"
                Board[i][j].Empty=False
                CastleNum-=1
                continue

            if Board[i][j].Empty and rand1>1 and rand2 < 3 and rand3 >8 and HellNum > 0:
                Board[i][j].Name="Hell"
                Board[i][j].Empty=False
                HellNum-=1
                continue

            Board[i][j].Height=int((rand1*rand2+rand3)/2-3)
            Board[i][j].Empty=False
            if Board[i][j].Height>=0:
                Board[i][j].Mount=True
            else:
                Board[i][j].Water=True
    print "Done"
    return Board

##########PrintBoard##############################
def PrintBoard(Board,Window):
    global Font
    Font=pygame.font.SysFont("msyh",32)
    
    Left=5
    Top=5

    TextSurfaceList=[]
    for i in range(0,41):
        TextSurfaceList.append(1)
        tmp=Font.render(str(i-20),
                        True,
                        (12,13,19))
        TextSurfaceList[i]=tmp

    tmp=Font.render("[X]", False, (150,20,20))
    TextSurfaceList.append(tmp)
    tmp=Font.render("{^}", True, (128,60,10))
    TextSurfaceList.append(tmp)
    tmp=Font.render("#", False, (140,13,13))
    TextSurfaceList.append(tmp)
    tmp=Font.render("  ", False, (140,13,13))
    TextSurfaceList.append(tmp)
        
    Window.fill(pygame.Color(255,255,255))
    
    for i in range(1, BoardHeight+1):
        for j in range(1, BoardWidth+1):
            if Board[i][j].FlagPlace == True:
                if Board[i][j].Belong == 1:
                    Window.blit(Home1, (Left,Top))
                elif Board[i][j].Belong == 2:
                    Window.blit(Home2, (Left,Top))
                elif Board[i][j].Belong == 3:
                    Window.blit(Home3, (Left,Top))
                else:
                    Window.blit(Home4, (Left,Top))

                pygame.draw.rect(Window,
                                 pygame.Color(150,120,140),
                                 (Left,Top,AreaWidth,AreaHeight),
                                 2)
            elif Board[i][j].Name == "Hell":
                pygame.draw.rect(Window,
                                 pygame.Color(160,50,20),
                                 (Left,Top,AreaWidth,AreaHeight),
                                 0)
                Window.blit(TextSurfaceList[41], (Left+3, Top+4))
            elif Board[i][j].Name == "Castle":
                pygame.draw.rect(Window,
                                 pygame.Color(160,100,40),
                                 (Left,Top,AreaWidth,AreaHeight),
                                 0)
                Window.blit(TextSurfaceList[42], (Left+3, Top+4))
            elif Board[i][j].Name== "Home":
                pygame.draw.rect(Window,
                                 pygame.Color(150,120,140),
                                 (Left,Top,AreaWidth,AreaHeight),
                                 2)
            else:
                if Board[i][j].Height >= 10:
                    pygame.draw.rect(Window,
                                 pygame.Color(40,120,30),
                                 (Left,Top,AreaWidth,AreaHeight),
                                 0)
                elif Board[i][j].Height >= 5 and Board[i][j].Height < 10:
                    pygame.draw.rect(Window,
                                 pygame.Color(80,175,55),
                                 (Left,Top,AreaWidth,AreaHeight),
                                 0)
                elif Board[i][j].Height >= 0 and Board[i][j].Height < 5:
                    pygame.draw.rect(Window,
                                 pygame.Color(100,220,90),
                                 (Left,Top,AreaWidth,AreaHeight),
                                 0)
                elif Board[i][j].Height >= -4 and Board[i][j].Height < 0:
                    pygame.draw.rect(Window,
                                 pygame.Color(30,250,250),
                                 (Left,Top,AreaWidth,AreaHeight),
                                 0)
                elif Board[i][j].Height >= -8 and Board[i][j].Height < -4:
                    pygame.draw.rect(Window,
                                 pygame.Color(20,229,240),
                                 (Left,Top,AreaWidth,AreaHeight),
                                 0)
                else:
                    pygame.draw.rect(Window,
                                 pygame.Color(30,180,180),
                                 (Left,Top,AreaWidth,AreaHeight),
                                 0)
                Window.blit(TextSurfaceList[Board[i][j].Height+20], (Left+3, Top+4))

            Left+=AreaWidth+1


        Left=5
        Top+=AreaHeight+1
    
    Left=5
    Top=5

#def MoveChess(FromX, FromY, ToX, ToY)
    
##########InitGame##############################
def InitGame():
    #Init pygame...Create windows...etc
    pygame.init()

    UI=pygame.display.set_mode((500,400))
    #Load pictures for home
    global Home1
    global Home2
    global Home3
    global Home4
    Home1=pygame.image.load("flag_1.png").convert()
    Home2=pygame.image.load("flag_2.png").convert()
    Home3=pygame.image.load("flag_3.png").convert()
    Home4=pygame.image.load("flag_4.png").convert()

    global Font
    Font=pygame.font.SysFont("msyh",35)
    
##########MapPreview##############################
def ShowMapPreviewWindow():
    global MapPreview
    global BackButtonInfo
    global ACButtonInfo
    global NewButtonInfo
    global LoadButtonInfo
    global Count
    
    ACButtonInfo=(WindowWidth//3-80, WindowHeight-50, 100, 45, Green, Gold)
    BackButtonInfo=((WindowWidth//3)*2-110, WindowHeight-50, 120, 45, Grey, Red)
    NewButtonInfo=(WindowWidth-130, WindowHeight-50, 90, 45, Red, Blue)
    LoadButtonInfo=(150, 100, 200, 52, Black, Red)
    
    while True:
        NewFlag=False

        MapPreview=pygame.display.set_mode((WindowWidth-60, WindowHeight-80))
        pygame.display.set_caption("                              M a p    P r e v i e w")
        global Font
        Font=pygame.font.SysFont("msyh", 40)
        CreateButton(LoadButtonInfo,
                                 "Loading......", Font, 13,
                                 MapPreview, "English")
        pygame.display.update()
        Font=pygame.font.SysFont("msyh", 35)
        
        Board=InitBoard(CastleNum, HellNum, HomeNum)
        PrintBoard(Board, MapPreview)

        pygame.image.save(MapPreview, "Map.png")
        Map=pygame.image.load("Map.png")
        Saved=False

        MapPreview=pygame.display.set_mode((WindowWidth, WindowHeight))
        MapPreview.fill(Purple)
        
        while True:
            if NewFlag:
                break

            clock=pygame.time.Clock()
            FPS=clock.tick(25)

            MapPreview.blit(Map, (25, 20))
            
            CreateButton(NewButtonInfo,
                                 "N e w", Font, 14,
                                 MapPreview, "English")
            CreateButton(BackButtonInfo,
                                 "Go Back", Font, 13,
                                 MapPreview, "English")
            CreateButton(ACButtonInfo,
                                 "Accept", Font, 15,
                                 MapPreview, "English")
              
            MousePos=pygame.mouse.get_pos()
            MousePressed=pygame.mouse.get_pressed()
                
            for Area in ACButtonInfo, BackButtonInfo, NewButtonInfo:
                if ButtonPressed(Area[:4], MousePos):
                            pygame.draw.rect(MapPreview,
                                             Area[4],
                                             (Area[0]-4,Area[1]-4,Area[2]+7,Area[3]+7),
                                             4)
                else:
                            pygame.draw.rect(MapPreview,
                                             Purple,
                                             (Area[0]-4,Area[1]-4,Area[2]+7,Area[3]+7),
                                             4)

            if MousePressed[0]:
                if ButtonPressed(NewButtonInfo[:4], MousePos):
                    time.sleep(0.12)
                    NewFlag=True
                if ButtonPressed(BackButtonInfo[:4], MousePos):
                    time.sleep(0.1)
                    return
                if ButtonPressed(ACButtonInfo[:4], MousePos):
                    if not Saved:
                        FileNameForSaving="Map"+str(Count)+".png"
                        pygame.image.save(Map, FileNameForSaving)
                        Count+=1
                        Saved=True
                    
                #if ButtonPressed(ACButtonInfo[:4], MousePos):
               
            for Event in pygame.event.get():
                if Event.type == QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update()
            pygame.display.update((25, BoardWidth*AreaWidth, 20, BoardHeight*AreaHeight))


    
##########GameUI##############################
def GameUI():
    global UI
    global CastleNum
    global HellNum
    global BoardHeight
    global BoardWidth
    global HomeNum

    #Default Values
    HellNum=8
    CastleNum=10
    HomeNum=2
    BoardHeight=13
    BoardWidth=16

    global StartButtonInfo, QuitButtonInfo, HelpButtonInfo
    global GenButtonInfo, BackButtonInfo
    global WidthAddButtonInfo, WidthSubstractButtonInfo, HeightAddButtonInfo, HeightSubstractButtonInfo
    
    StartButtonInfo=(150, 80, 200, 40, Gold, Black)
    HelpButtonInfo=(150, 150, 200, 40, Purple, Black)
    QuitButtonInfo=(150, 220, 200, 40, Green, Red)
    GenButtonInfo=(110, 320, 140, 40, Gold, Black)
    BackButtonInfo=(320, 320, 120, 40, Grey, Purple)
    WidthAddButtonInfo=(300, 105, 30, 30, Red, Grey)
    HeightAddButtonInfo=(300, 165, 30, 30, Red, Grey)
    HomeNumAddButtonInfo=(300, 215, 30, 30, Red, Grey)
    
    UI=pygame.display.set_mode((500,400))
    pygame.display.set_caption("                              A u t h o r :  T o m")

    StartFlag=False
    
    while True:

        UI.fill(Grey)
        while True:
            if StartFlag:
                time.sleep(0.4)
                break
            clock=pygame.time.Clock()
            FPS=clock.tick(25)
        
            CreateButton(StartButtonInfo,
                         "Start", Font , 18,
                         UI, "English")
            CreateButton(HelpButtonInfo,
                         "Help", Font, 20,
                         UI, "English")
            CreateButton(QuitButtonInfo,
                         "Quit", Font, 20,
                         UI,"English")

            MousePos=pygame.mouse.get_pos()
            MousePressed=pygame.mouse.get_pressed()
        
            for Area in StartButtonInfo, HelpButtonInfo, QuitButtonInfo:
                if ButtonPressed(Area[:4], MousePos):
                    pygame.draw.rect(UI,
                                     Area[4],
                                     (Area[0]-4,Area[1]-4,Area[2]+7,Area[3]+7),
                                     4)
                else:
                    pygame.draw.rect(UI,
                                     Grey,
                                     (Area[0]-4,Area[1]-4,Area[2]+7,Area[3]+7),
                                     4)
                    
            if MousePressed[0]:
                if ButtonPressed(QuitButtonInfo[:4], MousePos):
                    pygame.quit()
                    exit()
                if ButtonPressed(StartButtonInfo[:4], MousePos):
                    StartFlag=True
                
            for Event in pygame.event.get():
                if Event.type == QUIT:
                    pygame.quit()
                    exit()

            pygame.display.update()

        if StartFlag:
            UI.fill((25,25,8))
            
            while True:
                if not StartFlag:
                    break
                
                clock=pygame.time.Clock()
                FPS=clock.tick(30)
                
                if BoardWidth > 20:
                    BoardWidth=12
                if BoardHeight > 16:
                    BoardHeight=10
                if HomeNum > 4:
                    HomeNum=2
                    
                CreateButton((80, 100, 100, 40, Red, Grey),
                             "Width", Font , 18,
                             UI, "English")
                CreateButton((80 ,155, 100, 40, Red,Grey),
                             "Height", Font, 16,
                             UI, "English")
                CreateButton((80 ,210, 100, 40, Red,Grey),
                             "Homes", Font, 16,
                             UI, "English")
                CreateButton((90, 20, 350, 42, Green, Yellow),
                             "Set The Game Board", Font, 14,
                             UI, "English")
                CreateButton(GenButtonInfo,
                             "Generate",Font, 15,
                             UI, "English")
                CreateButton(BackButtonInfo,
                             "Go Back", Font, 14,
                             UI, "English")
                CreateButton((225, 105, 50, 35, Blue, Purple),
                            str(BoardWidth), Font, 14,
                             UI, "English")
                CreateButton((225, 160, 50, 35, Blue, Purple),
                             str(BoardHeight), Font, 14,
                             UI, "English")
                CreateButton((225, 215, 50, 35, Blue, Purple),
                             str(HomeNum), Font, 14,
                             UI, "English")
                CreateButton(WidthAddButtonInfo,
                             "+", Font, 23,
                             UI, "English")
                CreateButton(HeightAddButtonInfo,
                             "+", Font, 23,
                             UI, "English")
                CreateButton(HomeNumAddButtonInfo,
                             "+", Font, 23,
                             UI, "English")
                
                MousePos=pygame.mouse.get_pos()
                MousePressed=pygame.mouse.get_pressed()
                
                for Area in GenButtonInfo, BackButtonInfo, \
                     WidthAddButtonInfo, HeightAddButtonInfo, HomeNumAddButtonInfo:
                    if ButtonPressed(Area[:4], MousePos):
                        pygame.draw.rect(UI,
                                         Area[4],
                                         (Area[0]-4,Area[1]-4,Area[2]+7,Area[3]+7),
                                         4)
                    else:
                        pygame.draw.rect(UI,
                                         (25, 25, 8),
                                         (Area[0]-4,Area[1]-4,Area[2]+7,Area[3]+7),
                                         4)

                if MousePressed[0]:
                    if ButtonPressed(WidthAddButtonInfo[:4], MousePos):
                        BoardWidth+=1
                        time.sleep(0.12)
                    if ButtonPressed(HeightAddButtonInfo[:4], MousePos):
                        BoardHeight+=1
                        time.sleep(0.12)
                    if ButtonPressed(HomeNumAddButtonInfo[:4], MousePos):
                        HomeNum+=1
                        time.sleep(0.12)
                    if ButtonPressed(BackButtonInfo[:4], MousePos):
                        StartFlag=False
                        time.sleep(0.2)
                    if ButtonPressed(GenButtonInfo[:4], MousePos):
                        global WindowHeight
                        global WindowWidth
    
                        WindowHeight=BoardHeight*AreaHeight+105
                        WindowWidth=BoardWidth*AreaWidth+90
                        
                        ShowMapPreviewWindow()

                        #Reinit
                        UI=pygame.display.set_mode((500,400))
                        pygame.display.set_caption("                              A u t h o r :  T o m")
                        UI.fill((25,25,8))
                        BackButtonInfo=(320, 320, 120, 40, Grey, Purple)
                        
                for Event in pygame.event.get():
                    if Event.type == QUIT:
                        pygame.quit()
                        exit()
                    
                pygame.display.update()
                
'''
def MainGame():
    Window=pygame.display.set_mode((WindowWidth,WindowHeight))
    pygame.display.set_caption("Game Author: Tom")
    Board=InitBoard(CastleNum,HellNum,HomeNum)
'''
##########Main##############################
#A function that controls the whole game
def Main():

    InitGame()

    GameUI()
    #Main loop
    '''
    while True:
        GetEvent(Window)
        PrintBoard(Board, Window)
        clock=pygame.time.Clock()
        FPS=clock.tick(25)
        pygame.display.update()
    '''
Main()
