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

lowerDG = np.array([25, 25, 15])
upperDG = np.array([70, 170, 70])

DGmask = cv2.inRange(hsv, lowerDG, upperDG)
DGres = cv2.bitwise_and(board, board, mask=DGmask)

greenCards = []
blueCards = []
darkGreenCards = []

def rasterize(picture, cardAr):
    cards = []
    for i in range(1, 6):
        for j in range(1, 6):
            card = picture[(j - 1) * 100:(j - 1) * 100 + 100, (i - 1) * 100:(i - 1) * 100 + 100]
            cards.append(card)

    for i in range(0, 25):
        result = cv2.mean(cards[i])
        if result[1] > 10.0:
            cardAr.append(cards[i])
            cv2.imshow("Card " + str(i + 1), cards[i])

#rasterize(LGres, greenCards)

#rasterize(LBres, blueCards)

#rasterize(DGres, darkGreenCards)

cv2.imshow('board', board)
cv2.imshow('hsv', hsv)
cv2.imshow('LGmask', LGmask)
cv2.imshow('LGres', LGres)
cv2.imshow('LBmask', LBmask)
cv2.imshow('LBres', LBres)
cv2.imshow('DGmask',DGmask)
cv2.imshow('DGres', DGres)

cv2.waitKey(0)
