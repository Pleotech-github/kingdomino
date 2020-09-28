import cv2
import numpy as np


board = cv2.imread('1.jpg')
hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
w, h = board.shape[::-2]
pieceH = w / 5
pieceW = h / 5
visited = []

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




                    #tempAr = np.array([group,i-1,j-1])
                    #scoreAr = np.append(scoreAr, tempAr, axis=0)


# GrassFire algorithmen til at finde sorte pixels,
# som tilhøre en større gruppe af sorte pixels
def grassFire(newX: int, newY: int, groupNumber: int):
    if [newX + 1, newY] not in visited:
        XYArray.append([newX, newY])
        visited.append([newX, newY])

    if cardArray[newX + 1][newY] == 1 and cardArray[[newX + 1][newY]] not in visited:
        grassFire(newX + 1, newY, groupNumber)

    elif cardArray[newX][newY + 1] == 1 and cardArray[[newX][newY + 1]] not in visited:
        grassFire(newX, newY + 1, groupNumber)

    elif cardArray[newX - 1][newY] == 1 and cardArray[[newX - 1][newY]] not in visited:
        grassFire(newX - 1, newY, groupNumber)

    elif cardArray[newX][newY - 1] == 1 and cardArray[[newX][newY - 1]] not in visited:
        grassFire(newX, newY - 1,  groupNumber)

    else:
        index = XYArray.index([newX, newY])
        if index == 0:
            cv2.rectangle(board, (min(XYArray)), (max(XYArray)), (0, 255, 0), 2)
            print(XYArray)
        else:
            index = index - 1
            grassFire(XYArray[index][0], visited[index][1])


# Pixel detection
for i in colorArray:
    groupNumber = 0
    rasterize(DGres, visited)

    for x in range(0, 5):
        for y in range(0, 5):

            if cardArray[x][y] == 1 and [x, y] not in visited:
                XYArray = []
                groupNumber += 1
                grassFire(x, y, groupNumber)
                print('knep mig!')
            else:
                visited.append([x, y])




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
