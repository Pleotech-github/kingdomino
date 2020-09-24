import cv2
import numpy as np


board = cv2.imread('1.jpg')
hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
w, h = board.shape[::-2]
pieceH = w / 5
pieceW = h / 5

lowerLG = np.array([35, 100, 130])
upperLG = np.array([95, 255, 180])

LGmask = cv2.inRange(hsv, lowerLG, upperLG)
LGres = cv2.bitwise_and(board, board, mask=LGmask)

# - CC Blue color
lowerLB = np.array([65, 140, 80])
upperLB = np.array([250, 255, 255])

LBmask = cv2.inRange(hsv, lowerLB, upperLB)
LBres = cv2.bitwise_and(board, board, mask=LBmask)

#Dark green (forest)
lowerDG = np.array([25, 25, 15])
upperDG = np.array([70, 170, 70])

DGmask = cv2.inRange(hsv, lowerDG, upperDG)
DGres = cv2.bitwise_and(board, board, mask=DGmask)

#Yellow (fields)
lowerYL = np.array([25, 170, 170])
upperYL = np.array([30, 255, 255])

YLmask = cv2.inRange(hsv, lowerYL, upperYL)
YLres = cv2.bitwise_and(board, board, mask=YLmask)

#Grey?
lowerGR = np.array([15, 0, 60])
upperGR = np.array([30, 145, 160])

GRmask = cv2.inRange(hsv, lowerGR, upperGR)
GRres = cv2.bitwise_and(board, board, mask=GRmask)

rows, cols = (5,5)
cardArray = [[0]*cols]*rows

greenCards = []
blueCards = []
darkGreenCards = []
yellowCards = []

class Score:
    def __init__(self, card, score):
        self.card = card
        self.score = score

cards = []

def countScore2(color, cardAr):
    groupMax = 1
    scoreArray = np.zeros((5, 5))
    first = True
    sorted = False
    for i in range(0,5):
        for j in range(0,5):
            if cardAr[i][j] != 0:
                if first == True:
                    scoreArray[i][j] = 1
                    first = False
                    continue
                sorted = False
                for a in range(0,5):
                    for b in range(0,5):
                        if cardAr[a][b] != 0:
                            #print("a-i: " + str(abs(a - i)))
                            #print("b-j:" + str(abs(b-j)))
                            if a-i == 0 and abs(b-j) == 1:
                                if scoreArray[a][b] == 0:
                                    scoreArray[i][j] = groupMax
                                    scoreArray[a][b] = groupMax
                                    print("PLUSA" + str(groupMax))
                                else:
                                    scoreArray[i][j] = scoreArray[a][b]
                                sorted = True
                                print("A")
                                break
                            elif b-j == 0 and abs(a-i) == 1:
                                if scoreArray[a][b] == 0:
                                    scoreArray[i][j] = groupMax
                                    scoreArray[a][b] = groupMax
                                    print("PLUSB")
                                else:
                                    scoreArray[i][j] = scoreArray[a][b]
                                    print("ELSE")
                                sorted = True
                                print("B")
                                break
                            else:
                                groupMax+=1
                                print("END")
                if sorted == False:
                    print("D")
                    print("a-i: " + str(abs(a - i)))
                    print("b-j:" + str(abs(b-j)))
                    groupMax += 1
                    scoreArray[i][j] = groupMax
    print(scoreArray)

def countScore3(color, cardAr):
    groupMax = 1
    scoreArray = np.zeros((5, 5))
    first = True
    tempI = 0
    tempJ = 0
    for i in range(0,5):
        for j in range(0,5):
            if cardAr[i][j] != 0:
                if first == True:
                    scoreArray[i][j] = 1
                    first = False
                    continue

                oI = i
                oJ = j
                
                while(True):
                    if i < 4 and j < 4 and j > 0:
                        if cardAr[i+1][j] != 0:
                            tempI = i+1
                            tempJ = j
                            scoreArray[i][j] = groupMax
                            scoreArray[tempI][tempJ] = groupMax
                        if cardAr[i][j+1] != 0:
                            pass
                        if cardAr[i][j-1] != 0:
                            pass
                    elif i == 4:
                        if cardAr[i][j+1] != 0:
                            pass
                    elif j == 4:
                        if cardAr[i+1][j] != 0:
                            pass
                        if cardAr[i][j-1] != 0:
                            pass
                    elif j == 0:
                        if cardAr[i][j-1] != 0:
                            pass
                    else:
                        break
                    pass
                groupMax += 1
    pass

cardArray1 = np.zeros((5,5))

def rasterize(picture, cardAr, color):

    sc = Score(color,0)

    for i in range(1, 6):
        for j in range(1, 6):
            card = picture[(j - 1) * 100:(j - 1) * 100 + 100, (i - 1) * 100:(i - 1) * 100 + 100]
            cards.append(card)

            result = cv2.mean(card)
            if result[1] > 10.0:
                cardArray1[i - 1][j - 1] = 1
                #cardAr.append(cards[i])
                cv2.imshow("Card " + str(i + 1), card)
    print(cardArray1)
    countScore2("b", cardArray1)



                    #tempAr = np.array([group,i-1,j-1])
                    #scoreAr = np.append(scoreAr, tempAr, axis=0)


rasterize(LGres, greenCards, "b")

#rasterize(LBres, blueCards)

#rasterize(DGres, darkGreenCards)

#rasterize(GRres, yellowCards)

cv2.imshow('board', board)
cv2.imshow('hsv', hsv)
#cv2.imshow('LGmask', LGmask)
#cv2.imshow('LGres', LGres)
#cv2.imshow('LBmask', LBmask)
#cv2.imshow('LBres', LBres)
#v2.imshow('DGmask',DGmask)
#cv2.imshow('DGres', DGres)
#cv2.imshow('YLres', YLres)
cv2.imshow('GRres', GRres)

cv2.waitKey(0)
