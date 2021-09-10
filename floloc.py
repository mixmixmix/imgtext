import cv2 as cv

def onmouse(event, x, y, flags, param):
    if(event == cv.EVENT_LBUTTONDOWN):
        print(f'x:{x},y:{y}')

frame = cv.imread('input/fmeter_locs/a.png')
# frame = cv.imread('test.png')

cv.namedWindow('current_frame', cv.WINDOW_GUI_EXPANDED)
(h, w) = frame.shape[:2]
(cX, cY) = (w // 2, h // 2)

cv.setMouseCallback("current_frame", onmouse, param = None)
cv.imshow('current_frame',frame)
k = cv.waitKey(0)
cv.destroyAllWindows()

#pa x:534,y:194
#pb x:539,y:637
#pa = x:488,y:237
#pb = x:641,y:657
dx = 5
dy = 637 - 194
#alpha = -beta
#tg(alpha) = dx/dy
degrot = - np.degrees(np.arctan2(dx,dy))

M = cv.getRotationMatrix2D((cX, cY), degrot, 1.0)
rotated = cv.warpAffine(frame, M, (w, h))

cv.namedWindow('current_frame')
cv.setMouseCallback("current_frame", onmouse, param = None)
cv.imshow('current_frame',rotated)

#pa, pb, fl
# x:534,y:192
#x:535,y:636
#x:1131,y:371
flume_width = 636-192
f_loc_x = (1131-535)/flume_width
f_loc_y = (371-192)/flume_width

k = cv.waitKey(0)
cv.destroyAllWindows()
