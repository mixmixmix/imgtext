import cv2 as cv

def onmouse(event, x, y, flags, param):
    if(event == cv.EVENT_LBUTTONDOWN):
        print(f'x:{x},y:{y}')


# #dig size 64x40
clock_loc = [12,22,115,167]

# frame = cv.imread('input/frame145440.png')
# sx, sy = 40, 64
# dx, dy, ds = 592, 230, 8 #depending on distance space between numbers differ a bit
# degrot=1

#ds=3
#frame = cv.imread('input/frame14.png')
#sx, sy = 45, 70
#dx, dy = 512, 300
#degrot=3

#ds=1
#frame = cv.imread('input/frame14.png')
#sx, sy = 60, 80
#dx, dy = 471, 376
#degrot=0
"""
frame = cv.imread('input/21a.png')
sx, sy = 30, 40
dx, dy = 995, 385
degrot=-1.7

frame = cv.imread('input/21b.png')
sx, sy = 21, 35
dx, dy = 1105, 404
degrot=0

frame = cv.imread('input/21g.png')
sx, sy = 19, 28
dx, dy = 620, 276
degrot=-3

frame = cv.imread('input/21f.png')
sx, sy = 17, 26
dx, dy = 619, 275
degrot=-2.4

frame = cv.imread('input/21e.png')
sx, sy = 18, 28
dx, dy = 623, 276
degrot=-2.4

frame = cv.imread('input/21d.png')
sx, sy = 20, 28
dx, dy = 633, 280
degrot=-2.7

frame = cv.imread('input/21c.png')
sx, sy = 23, 36
dx, dy = 973, 417
degrot=-1.6
"""

frame = cv.imread('input/5oct.png')
sx, sy = 60, 80
dx, dy = 630, 402
degrot=-1.6


dig1 = [dy,dy+sy,dx,dx+sx]
dig2 = [dy,dy+sy,dx+sx,dx+2*sx]


n = 0
(h, w) = frame.shape[:2]

#get clock
frame_clock = frame[clock_loc[0]:clock_loc[1],clock_loc[2]:clock_loc[3]].copy()

#rotate to get flow digits nice
(cX, cY) = (w // 2, h // 2)
M = cv.getRotationMatrix2D((cX, cY), degrot, 1.0)
rotated = cv.warpAffine(frame, M, (w, h))


frame_dig1 = rotated[dig1[0]:dig1[1],dig1[2]:dig1[3]]
frame_dig2 = rotated[dig2[0]:dig2[1],dig2[2]:dig2[3]]
#x:595,y:233
#x:635,y:297
#x:636,y:230
#x:677,y:295

cv.namedWindow('current_frame')
cv.namedWindow('current_dig1')
cv.moveWindow('current_dig1', 120,120)
cv.namedWindow('current_dig2')
cv.moveWindow('current_dig2', 180,120)
# cv.namedWindow('current_clock')

cv.setMouseCallback("current_frame", onmouse, param = None)
cv.imshow('current_frame',rotated)
# cv.imshow('current_clock',frame_clock)
cv.imshow('current_dig1',frame_dig1)
cv.imshow('current_dig2',frame_dig2)

result = cv.matchTemplate(frame_dig1, frame_dig2, cv.TM_SQDIFF)
print(result)
cv.imwrite(f'dig1.png',frame_dig1)
cv.imwrite(f'dig2.png',frame_dig2)
n = n+1

k = cv.waitKey(0)
cv.destroyAllWindows()
