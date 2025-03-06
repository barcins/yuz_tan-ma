import cv2




def video_kaydet():

    vid = cv2.VideoCapture(0)
    w = int(vid.get(3))
    h = int(vid.get(4))
    size = (w, h)
    result = cv2.VideoWriter('record.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 24, size)
    while True:
        ret, frame_video = vid.read()
        if ret == True:
            result.write(frame_video)
            cv2. imshow('frame_video' , frame_video)
            kInp = cv2. waitKey(1)
            if kInp == ord('s'):
                break
        else:
            break
    vid. release()
    result.release()
    cv2.destroyAllWindows()

video_kaydet()