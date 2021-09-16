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

ds=1
frame = cv.imread('input/frame14.png')
sx, sy = 60, 80
dx, dy = 471, 376
degrot=0

dig1 = [dy,dy+sy,dx,dx+sx]
dig2 = [dy,dy+sy,dx+sx+ds,dx+ds+2*sx]


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
cv.namedWindow('current_dig2')
cv.namedWindow('current_clock')

cv.setMouseCallback("current_frame", onmouse, param = None)
cv.imshow('current_frame',rotated)
cv.imshow('current_clock',frame_clock)
cv.imshow('current_dig1',frame_dig1)
#cv.imshow('current_dig2',frame_dig2)

result = cv.matchTemplate(frame_dig1, frame_dig2, cv.TM_SQDIFF)
print(result)
cv.imwrite(f'dig1.png',frame_dig1)
cv.imwrite(f'dig2.png',frame_dig2)
n = n+1

k = cv.waitKey(0)
cv.destroyAllWindows()
