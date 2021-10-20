import cv2 as cv
import numpy as np
import glob

point_name = ""
mode_arrange = True
pa = (0,0)
pb = (0,0)
dx=0
dy=0
f_loc_x = 0
f_loc_y = 0
M = np.zeros([2,3])

def onmouse(event, x, y, flags, param):
    global pa, pb, dx, dy, point_name, f_loc_x, f_loc_y, M, outputfilename

    if mode_arrange:
        if(event == cv.EVENT_LBUTTONDOWN):
            pa = (x,y)
            dx = pb[0]-pa[0]
            dy = pb[1]-pa[1]
            print(f'pa is {pa}')
        if(event == cv.EVENT_RBUTTONDOWN):
            pb = (x,y)
            dx = pb[0]-pa[0]
            dy = pb[1]-pa[1]
            print(f'pb is {pb}')
    else:
        if(event == cv.EVENT_LBUTTONDOWN):

            pap = np.dot(M,[pa[0],pa[1],1])
            pbp = np.dot(M,[pb[0],pb[1],1])
            dxp = pbp[0] - pap[0]
            dyp = pbp[1] - pap[1]

            fw = np.sqrt(dxp**2 +  dyp**2)

            f_loc_x = (x - pap[0]) / fw
            f_loc_y = (y - pap[1]) / fw

            print(f'{point_name}, {f_loc_x},{f_loc_y}')


# outputfilename = './output/newlocs.csv'
# outputfilename = './output/fishlocs.csv'
outputfilename = './output/5octlocs.csv'

with open(outputfilename, 'a') as f:
    f.write('loc_name,loc_x,loc_y,\n')

cv.namedWindow('current_frame', cv.WINDOW_GUI_EXPANDED)
cv.moveWindow('current_frame', 120,120)

# files = glob.glob('input/fmeter_locs/*png')
#files = glob.glob('input/fishloc/*png')
files = glob.glob('input/fmeter5oct/*png')

for fname in files:
    mode_arrange = True
    frame = cv.imread(fname)
    # frame = cv.imread('test.png')
    point_name = fname.split('/')[-1].split('.')[0]

    (h, w) = frame.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    cv.setMouseCallback("current_frame", onmouse, param = None)
    cv.imshow('current_frame',frame)

    k = cv.waitKey(0)
    mode_arrange = False
    print(f'dx and dy is {dx} and {dy}')
    degrot = - np.degrees(np.arctan2(dx,dy))

    M = cv.getRotationMatrix2D((cX, cY), degrot, 1.0)
    rotated = cv.warpAffine(frame, M, (w, h))

    cv.imshow('current_frame',rotated)


    k = cv.waitKey(0)
    if k == ord('q'):
        break

    with open(outputfilename, 'a') as f:
        f.write(f'{point_name}, {f_loc_x},{f_loc_y}\n')

cv.destroyAllWindows()
