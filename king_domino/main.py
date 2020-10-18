import cv2
import numpy as np
import math

board = cv2.imread('1.jpg')
tem1 = cv2.imread('grayTemp1.jpg')
tem2 = cv2.imread('grayTemp2.jpg')
tem3 = cv2.imread('grayTemp3.jpg')
tem4 = cv2.imread('grayTemp4.jpg')
tem5 = cv2.imread('blueTem1.jpg')
tem6 = cv2.imread('blueTem2.jpg')
tem7 = cv2.imread('blueTem3.jpg')
tem8 = cv2.imread('blueTem4.jpg')
tem9 = cv2.imread('lGTem1.jpg')
tem10 = cv2.imread('lGTem2.jpg')
tem11 = cv2.imread('lGTem3.jpg')
tem12 = cv2.imread('lGTem4.jpg')

kingTem1 = cv2.imread('kingTem1.jpg')
kingTem2 = cv2.imread('kingTem2.jpg')
kingTem3 = cv2.imread('kingTem3.jpg')
kingTem4 = cv2.imread('kingTem4.jpg')


hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
grayTem1 = cv2.cvtColor(tem1, cv2.COLOR_BGR2GRAY)
grayTem2 = cv2.cvtColor(tem2, cv2.COLOR_BGR2GRAY)
grayTem3 = cv2.cvtColor(tem3, cv2.COLOR_BGR2GRAY)
grayTem4 = cv2.cvtColor(tem4, cv2.COLOR_BGR2GRAY)
grayTem5 = cv2.cvtColor(tem5, cv2.COLOR_BGR2GRAY)
grayTem6 = cv2.cvtColor(tem6, cv2.COLOR_BGR2GRAY)
grayTem7 = cv2.cvtColor(tem7, cv2.COLOR_BGR2GRAY)
grayTem8 = cv2.cvtColor(tem8, cv2.COLOR_BGR2GRAY)
grayTem9 = cv2.cvtColor(tem9, cv2.COLOR_BGR2GRAY)
grayTem10 = cv2.cvtColor(tem10, cv2.COLOR_BGR2GRAY)
grayTem11 = cv2.cvtColor(tem11, cv2.COLOR_BGR2GRAY)
grayTem12 = cv2.cvtColor(tem12, cv2.COLOR_BGR2GRAY)

kingGray1 = cv2.cvtColor(kingTem1, cv2.COLOR_BGR2GRAY)
kingGray2 = cv2.cvtColor(kingTem2, cv2.COLOR_BGR2GRAY)
kingGray3 = cv2.cvtColor(kingTem3, cv2.COLOR_BGR2GRAY)
kingGray4 = cv2.cvtColor(kingTem4, cv2.COLOR_BGR2GRAY)

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

templateArray = [grayTem1, grayTem2, grayTem3, grayTem4, grayTem5, grayTem6, grayTem7, grayTem8, grayTem9, grayTem10,
                 grayTem11, grayTem12]
kingTemArray = [kingGray1, kingGray2, kingGray3, kingGray4]
colorArray = [LGres, LBres, DGres, YLres, GRres]


class Score:
    def __init__(self, card, score):
        self.card = card
        self.score = score
cards = []
cardArray1 = np.zeros((5, 5))
crownArray = np.zeros((5, 5))
pointArray = []

thresholdDistCrown = 15
detectedObjects = []
def notInList(newObject, thresholdDist):
    for detectedObject in detectedObjects:
        if math.hypot(newObject[0]-detectedObject[0], newObject[1]-detectedObject[1]) < thresholdDist:
            return False
    return True



def rasterize(picture, visited):
    for i in range(1, 6):
        for j in range(1, 6):
            card = picture[(j - 1) * 100:(j - 1) * 100 + 100, (i - 1) * 100:(i - 1) * 100 + 100]
            cards.append(card)

            result = cv2.mean(card)
            if result[1] > 10.0:
                cardArray1[j - 1][i - 1] = 1


                crop = board[(j - 1) * 100:(j - 1) * 100 + 100, (i - 1) * 100:(i - 1) * 100 + 100]
                cv2.imwrite('card.png', crop)
                crop = cv2.imread('card.png', cv2.IMREAD_GRAYSCALE)
                crownNumber = 0

                for tem in templateArray:
                    h = tem.shape[0]
                    w = tem.shape[1]
                    res = cv2.matchTemplate(crop, tem, cv2.TM_CCOEFF_NORMED)
                    threshold = 0.7
                    loc = np.where(res >= threshold)

                    for pt in zip(*loc[::-1]):
                        if len(detectedObjects) == 0 or notInList(pt, thresholdDistCrown):
                            cv2.rectangle(board, (pt[0] + (i - 1) * 100, pt[1] + (j - 1) * 100),
                                          (pt[0] + (i - 1) * 100 + w, pt[1] + (j - 1) * 100 + h), (0, 0, 0), 2)
                            detectedObjects.append(pt)
                            crownNumber += 1
                            crownArray[j-1][i-1] = crownNumber

                for tem in kingTemArray:
                    res = cv2.matchTemplate(crop, tem, cv2.TM_CCOEFF_NORMED)
                    cv2.imshow('res', res)
                    threshold = 0.7
                    loc = np.where(res >= threshold)
                    for pt in zip(*loc[::-1]):
                        if notInList(pt, 30):
                            visited[j][i] = 1



    print('farve pladceringer ')
    print(cardArray1)
    print('mængde af kroner ')
    print(crownArray)

    detectedObjects.clear()


def grassFrie(x, y, groupSize, visited, XYArray, groupNumber, append, crownNumber):

    if append == True:
        visited[x][y] = 1
        groupSize.append(groupNumber)
        XYArray.append([y, x])
        crownNumber += int(crownArray[x][y])
    append = True


    if x < 4 and visited[x + 1][y] != 1 and cardArray1[x + 1][y] == 1:
        grassFrie(x + 1, y, groupSize, visited, XYArray, groupNumber, append, crownNumber)

    elif y < 4 and visited[x][y + 1] != 1 and cardArray1[x][y + 1] == 1:
        grassFrie(x, y + 1, groupSize, visited, XYArray, groupNumber, append, crownNumber)

    elif x > 0 and visited[x - 1][y] != 1 and cardArray1[x - 1][y] == 1:
        grassFrie(x - 1, y, groupSize, visited, XYArray, groupNumber, append, crownNumber)

    elif y > 0 and visited[x][y - 1] != 1 and cardArray1[x][y - 1] == 1:
        grassFrie(x, y - 1, groupSize, visited, XYArray, groupNumber, append, crownNumber)

    elif XYArray.index([y, x]) != 0:
        append = False
        rowIndex = XYArray.index([y, x]) - 1
        y, x = XYArray[rowIndex]
        grassFrie(x, y, groupSize, visited, XYArray, groupNumber, append, crownNumber)

    else:
        amount = {j: groupSize.count(j) for j in groupSize}

        points = crownNumber * amount[groupNumber]
        pointArray.append(points)
        print(pointArray)


def count(color):

    img = color
    cv2.imshow('img', img)
    visited = np.zeros((5, 5))
    rasterize(img, visited)
    #cv2.imshow(str(index), img)
    groupSize = []
    groupNumber = 0
    for rows in range(0, 5):
        for cols in range(0, 5):
            if cardArray1[rows][cols] == 1 and visited[rows][cols] != 1:
                groupNumber += 1
                XYArray = []
                append = True
                crownNumber = 0
                grassFrie(rows, cols, groupSize, visited, XYArray, groupNumber, append, crownNumber)
            else:
                visited[rows][cols] = 1


def calPoints():
    finalScore = sum(pointArray)
    print(finalScore)
    return finalScore

allScore = 0

for color in colorArray:
    count(color)
    allScore += calPoints()
    pointArray = []
    cardArray1 = np.zeros((5, 5))

print("Final board score: " + str(allScore))

cv2.imshow('board', board)
#cv2.imshow('hsv', hsv)
#cv2.imshow('LGres', LGres)
#cv2.imshow('LBres', LBres)
#cv2.imshow('DGres', DGres)
#cv2.imshow('YLres', YLres)
#cv2.imshow('GRres', GRres)

cv2.waitKey(0)