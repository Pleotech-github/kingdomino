import cv2
import numpy as np


board = cv2.imread('1.jpg')
hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
w, h = board.shape[::-2]
pieceH = w / 5
pieceW = h / 5
visited = np.zeros((5,5))

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

colorArray = [LGres, LBres, DGres, YLres, GRres]

class Score:
    def __init__(self, card, score):
        self.card = card
        self.score = score

cards = []



cardArray1 = np.zeros((5,5))


def rasterize(picture, cardAr):

    #sc = Score(color,0)

    for i in range(1, 6):
        for j in range(1, 6):
            card = picture[(j - 1) * 100:(j - 1) * 100 + 100, (i - 1) * 100:(i - 1) * 100 + 100]
            cards.append(card)

            result = cv2.mean(card)
            if result[1] > 10.0:
                cardArray1[i - 1][j - 1] = 1
                #cardAr.append(cards[i])
                cv2.imshow("Card " + str(i + 1), card)
    #print(cardArray1)


def grassFrie(x, y, groupSize, XYArray, groupNumber):
    visited[y][x] = 1
    groupSize.append(groupNumber)
    XYArray.append([y, x])
    if x < 4 and visited[y][x + 1] != 1 and cardArray1[y][x + 1] == 1:
        print('hej')
        grassFrie(x + 1, y, groupSize, XYArray, groupNumber)

    elif y < 4 and visited[y + 1][x] != 1 and cardArray1[y + 1][x] == 1:
        print('hej2')
        grassFrie(x, y + 1, groupSize, XYArray, groupNumber)

    elif x > 0 and visited[y][x - 1] != 1 and cardArray1[y][x - 1] == 1:
        print('hej3')
        grassFrie(x - 1, y, groupSize, XYArray, groupNumber)

    elif y > 0 and visited[y - 1][x] != 1 and cardArray1[y - 1][x] == 1:
        print('hej4')
        grassFrie(x, y - 1, groupSize, XYArray, groupNumber)

    else:
        print('hej5')
        rowIndex = XYArray.index([y, x])
        if rowIndex == 0:
            print('done')
        else:
            rowIndex -= 1
            y, x = XYArray[rowIndex]
            print(y)
            print(x)
            grassFrie(x, y, groupSize, XYArray, groupNumber)


def count():
    groupNumber = 0
    groupSize = []
    for rows in range(0, 5):
        for cols in range(0, 5):
            if cardArray1[rows][cols] == 1 and visited[rows][cols] != 1:
                groupNumber += 1
                XYArray = []
                grassFrie(rows, cols, groupSize, XYArray, groupNumber)
            else:
                groupSize.append(0)
                visited[cols][rows] = 1

    print(groupSize)


rasterize(DGres, visited)
count()

#rasterize(LGres, greenCards)

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
cv2.imshow('DGres', DGres)
#cv2.imshow('YLres', YLres)
#cv2.imshow('GRres', GRres)

cv2.waitKey(0)
