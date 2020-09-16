import cv2
import numpy as np

board = cv2.imread('1.jpg')
hsv = cv2.cvtColor(board, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
w, h = board.shape[::-2]
pieceH = w/5
pieceW = h/5

lowerLG = np.array([30, 100, 130])
upperLG = np.array([100, 255, 180])
LGmask = cv2.inRange(hsv, lowerLG, upperLG)
LGres = cv2.bitwise_and(board, board, mask=LGmask)

cv2.imshow('board', board)
cv2.imshow('hsv', hsv)
cv2.imshow('LGmask', LGmask)
cv2.imshow('LGres', LGres)

cv2.waitKey(0)