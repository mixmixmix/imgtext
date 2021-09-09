import cv2 as cv

#find out if we "reached" next second by analysing the clock display changes
# fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
# using absolute difference

fname='./input/TEST-23Mar-2021-145440.avi'

ctime = datetime.datetime(2021,3,23,14,54,40)

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
    clock_loc = [12,22,115,167]
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
        print(ctime.strftime("%Y-%m-%d %H:%M:%S"))

    # cover_str = "{0:.2f}".format(coverage)
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

    cv.imwrite(f'./output/dig{n}.png',frame_dig1)
    n = n+1
    cv.imwrite(f'./output/dig{n}.png',frame_dig2)
    n = n+1

    key = cv.waitKey(0)
    if key == ord('q'):
        print("quit")
        break

cap.release()
cv.destroyAllWindows()
