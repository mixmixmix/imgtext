import cv2 as cv

def onmouse(event, x, y, flags, param):
    if(event == cv.EVENT_LBUTTONDOWN):
        print(f'x:{x},y:{y}')

n = 0
frame = cv.imread('frame.png')
(h, w) = frame.shape[:2]

#get clock
clock_loc = [12,22,115,167]
frame_clock = frame[clock_loc[0]:clock_loc[1],clock_loc[2]:clock_loc[3]].copy()

#rotate to get flow digits nice
(cX, cY) = (w // 2, h // 2)
M = cv.getRotationMatrix2D((cX, cY), 1, 1.0)
rotated = cv.warpAffine(frame, M, (w, h))

flow_loc = [234,303,590,684]
dig1 = [233,297,595,635]
dig2 = [230,295,636,677]

frame_flow = rotated[flow_loc[0]:flow_loc[1],flow_loc[2]:flow_loc[3]]
frame_dig1 = rotated[dig1[0]:dig1[1],dig1[2]:dig1[3]]
frame_dig2 = rotated[dig2[0]:dig2[1],dig2[2]:dig2[3]]
#x:595,y:233
#x:635,y:297
#x:636,y:230
#x:677,y:295

cv.namedWindow('current_frame')
cv.namedWindow('current_flow')
cv.namedWindow('current_dig1')
cv.namedWindow('current_dig2')
cv.namedWindow('current_clock')

cv.setMouseCallback("current_frame", onmouse, param = None)
cv.imshow('current_frame',rotated)
cv.imshow('current_clock',frame_clock)
cv.imshow('current_dig1',frame_dig1)
cv.imshow('current_dig2',frame_dig2)

cv.imwrite(f'dig{n}.png',frame_dig1)
n = n+1

k = cv.waitKey(0)
cv.destroyAllWindows()
