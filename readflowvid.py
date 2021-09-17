import cv2 as cv
import datetime
import numpy as np


def mkMatchTemplate(img1, img2):
    no_pixels = img1.shape[0] * img1.shape[1]
    img1_gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    img1_bin = cv.threshold(img1_gray, 0, 1, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

    img2_gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    img2_bin = cv.threshold(img2_gray, 0, 1, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

    fgmask = cv.absdiff(img1_bin,img2_bin)
    ones = cv.countNonZero(fgmask)
    percdiff = 100 * (ones/no_pixels)
    return percdiff

#find out if we "reached" next second by analysing the clock display changes
# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
# using absolute difference

#manual settings of each video yanked from readflowIMG program

# ctime = datetime.datetime(2021,3,23,14,54,40)
# fname='./input/TEST-23Mar-2021-145440.avi'
# setname = '145440'
# dx, dy, ds = 592, 230, 5
# degrot=1

#ctime = datetime.datetime(2021,3,23,15,24,40)
#fname='./input/TEST-23Mar-2021-152440.avi'
#setname = '152440'
#sx, sy = 45, 70
#dx, dy, ds = 515, 300, 3
#degrot=3

# ctime = datetime.datetime(2021,9,14,12,30,37)
# fname='/mnt/three/flowprofile/TEST-14Sep-2021-123037.avi'
# setname = '14sep'
# sx, sy = 60, 80
# dx, dy, ds = 471, 376, 1
# degrot=0


ctime = datetime.datetime(2021,9,14,13,13,36)
fname='/mnt/three/flowprofile/TEST-14Sep-2021-131336.avi'
setname = '14sep2'
sx, sy = 60, 80
dx, dy, ds = 406, 253, 1
degrot=1


outputfilename = f'./output/{setname}.csv'

dd = f'./input/{setname}/'
d1_0 = cv.imread(f'{dd}d1_0.png')
d1_1 = cv.imread(f'{dd}d1_1.png')
d1_2 = cv.imread(f'{dd}d1_2.png')
d2_0 = cv.imread(f'{dd}d2_0.png')
d2_1 = cv.imread(f'{dd}d2_1.png')
d2_2 = cv.imread(f'{dd}d2_2.png')
d2_3 = cv.imread(f'{dd}d2_3.png')
d2_4 = cv.imread(f'{dd}d2_4.png')
d2_5 = cv.imread(f'{dd}d2_5.png')
d2_6 = cv.imread(f'{dd}d2_6.png')
d2_7 = cv.imread(f'{dd}d2_7.png')
d2_8 = cv.imread(f'{dd}d2_8.png')
d2_9 = cv.imread(f'{dd}d2_9.png')

d1_t = [d1_0,d1_1, d1_2]
d2_t = [d2_0, d2_1, d2_2, d2_3,d2_4,d2_5,d2_6,d2_7,d2_8,d2_9]

# d1_t = []
# d2_t = []

with open(outputfilename, 'a') as f:
    f.write('date,flow_v\n')

clock_loc = [12,22,115,167]
dig1 = [dy,dy+sy,dx,dx+sx]
dig2 = [dy,dy+sy,dx+sx,dx+2*sx]


cap = cv.VideoCapture(fname)

if (cap.isOpened() == False):
    print("Error opening video stream or file\n")



ret, frame = cap.read()
iterator = 1

(h, w) = frame.shape[:2]


n = 0
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == False:
        break

    # frame = cv.imread('frame.png')
    #get clock
    frame_clock = frame[clock_loc[0]:clock_loc[1],clock_loc[2]:clock_loc[3]].copy()
    no_pixels = frame_clock.shape[0] * frame_clock.shape[1]
    clock_gray = cv.cvtColor(frame_clock, cv.COLOR_BGR2GRAY)
    clock_bin = cv.threshold(clock_gray, 128, 1, cv.THRESH_BINARY)[1] #for some reason it is returning a tuple...
    if n == 0: #first frame
        clock_prev = clock_bin
    fgmask = cv.absdiff(clock_bin,clock_prev)
    clock_prev = clock_bin
    ones = cv.countNonZero(fgmask)
    coverage = 100 * (ones/no_pixels)
    if coverage > 0.2:
        ctime = ctime + datetime.timedelta(0,1)
        # print(ctime.strftime("%Y-%m-%d %H:%M:%S"))

    # cover_str = "{0:.2f}".format(coverage)
    #rotate to get flow digits nice
    (cX, cY) = (w // 2, h // 2)
    M = cv.getRotationMatrix2D((cX, cY), degrot, 1.0)
    rotated = cv.warpAffine(frame, M, (w, h))


    # frame_flow = rotated[flow_loc[0]:flow_loc[1],flow_loc[2]:flow_loc[3]]
    frame_dig1 = rotated[dig1[0]:dig1[1],dig1[2]:dig1[3]]
    frame_dig2 = rotated[dig2[0]:dig2[1],dig2[2]:dig2[3]]
    #x:595,y:233
    #x:635,y:297
    #x:636,y:230
    #x:677,y:295
    res1 = []
    for dt in d1_t:
        result = mkMatchTemplate(frame_dig1, dt)
        res1.append(result)
    # print()
    res2 = []

    for dt in d2_t:
        result = mkMatchTemplate(frame_dig2, dt)
        res2.append(result)

    ### ###
    #tmp HACK some numbers do not display:
    di = np.argmin(np.array(res2))

    #154042
    # if di == 6:
    #     di = 8
    # if di == 5:
    #     di = 7
    # if id == 4:
    #     di = 6
    # if di == 3:
    #     di = 4
    # if di == 2:
    #     di = 3

    flow_v = 10 * np.argmin(np.array(res1)) + di

    with open(outputfilename, 'a') as f:
        f.write( ctime.strftime("%Y-%m-%d %H:%M:%S") + ',' + str(flow_v) + '\n')

    ### ### 

    # cv.namedWindow('current_frame')
    # cv.namedWindow('current_dig1')
    # cv.namedWindow('current_dig2')
    # cv.namedWindow('current_clock')

    # cv.imshow('current_frame',rotated)
    # cv.imshow('current_clock',frame_clock)
    # cv.imshow('current_dig1',frame_dig1)
    # cv.imshow('current_dig2',frame_dig2)

    cv.imwrite(f'./output/{setname}/dig1_{n}.png',frame_dig1)
    n = n+1
    cv.imwrite(f'./output/{setname}/dig2_{n}.png',frame_dig2)
    n = n+1

    key = cv.waitKey(2)
    if key == ord('q'):
        print("quit")
        break

cap.release()
cv.destroyAllWindows()
