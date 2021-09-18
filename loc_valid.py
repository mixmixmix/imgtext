import cv2 as cv
import numpy as np
import glob
import pandas as pd

xx = 0
yy = 0
point_name = ""
mode_arrange = True
pa = (0,0)
pb = (0,0)
dx=0
dy=0
f_loc_x = 0
f_loc_y = 0
M = np.zeros([2,3])
h = 0
w = 0
cX = 0
cY = 0

def onmouse(event, x, y, flags, param):
    global pa, pb, dx, dy, point_name, f_loc_x, f_loc_y, M, outputfilename, cX, cY, h, w
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

        degrot = - np.degrees(np.arctan2(dx,dy))
        M = cv.getRotationMatrix2D((cX, cY), degrot, 1.0)
        pap = np.dot(M,[pa[0],pa[1],1])
        pbp = np.dot(M,[pb[0],pb[1],1])
        dxp = pbp[0] - pap[0]
        dyp = pbp[1] - pap[1]

        fw = np.sqrt(dxp**2 +  dyp**2)
        print(f'pap is {pap}')
        print(f'pbp is {pbp}')
        print(f'xx is {xx}')
        print(f'yy is {yy}')
        fx = fw * xx
        fy = fw * yy
        print(f'fw xx is {fx}')
        print(f'fw yy is {fy}')

        lx = int(fw * xx + pap[0])
        ly = int(fw * yy + pap[1])

        cv.circle(frame,(lx,ly), 5, (0,0,255), 1)

inputfilename = './input/flowmeterlocs21.csv'

flocs = pd.read_csv(inputfilename)

cv.namedWindow('current_frame', cv.WINDOW_GUI_EXPANDED)

for ind, val in flocs.iterrows():
    print(val)
    lname = val['loc_name']
    xx = val['loc_x']
    yy = val['loc_y']
    dt = val['datetime']


    fname = f'input/fmeter_locs/{lname}.png'
    print(fname)
    frame = cv.imread(fname)
    (h, w) = frame.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    cv.putText(frame, dt,  (300,100), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (0,240,240), 1);


    cv.setMouseCallback("current_frame", onmouse, param = None)
    cv.imshow('current_frame',frame)
    k = cv.waitKey(0)
    cv.imshow('current_frame',frame)
    k = cv.waitKey(0)
    if k ==  ord('q'):
        print('bye?')
        break

cv.destroyAllWindows()
