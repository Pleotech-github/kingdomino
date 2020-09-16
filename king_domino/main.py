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

def rasterize(picture):
    cards = []
    for i in range(1, 6):
        for j in range(1, 6):
            card1 = picture[(j - 1) * 100:(j - 1) * 100 + 100, (i - 1) * 100:(i - 1) * 100 + 100]
            cards.append(card1)

    for i in range(0, 25):
        cv2.imshow("Card" + str(i + 1), cards[i])

cv2.imshow('board', board)
cv2.imshow('hsv', hsv)
cv2.imshow('LGmask', LGmask)
cv2.imshow('LGres', LGres)
cv2.imshow('LBmask', LBmask)
cv2.imshow('LBres', LBres)

cv2.waitKey(0)
