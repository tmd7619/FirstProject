import sys
import cv2
import pyzbar.pyzbar as pyzbar
from threading import Timer
# 카메라로부터 cv2.VideoCapture 객체 생성
flag = 1

def timefunction():
    print('timefunction')
    global flag
    flag = 0
def opencv_mobile(start):
    flag = start
    timeout = 20
    t = Timer(timeout,timefunction)
    t.start()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera open failed!")
        sys.exit()

    # 프레임 해상도 출력
    # print('Frame width:', round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    # print('Frame height:', round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    delay = round(1000/ fps)
    # 매 프레임 처리 및 화면 출력
    check = 0
    while True:
        ret, frame = cap.read()
        #frame = frame[:,:-200]
        if not ret:
            break

        img = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        decoded = pyzbar.decode(img)

        for d in decoded:
            x,y,w,h = d.rect
            barcode_data = d.data.decode("utf-8")
            barcode_type = d.type
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255), 2)
            text = '%s (%s)' % (barcode_data, barcode_type)
            cv2.putText(frame, text, (x,y), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2, cv2.LINE_AA)
            print(text)
            cropping = frame[y:y+h,x:x+w]

            if text =='TRACSE_ID=AIG20200000286598,TRACSE_TME=3,CRSE_TRACSE_SE=C0061,NW_INO=200400649 (QRCODE)':
                check = 1
                break

        cv2.imshow('frame', frame)

        if check == 1:
            cap.release()
            cv2.destroyAllWindows()
            t.cancel()
            return 1

        if cv2.waitKey(delay) == 27 or flag == 0:
            cap.release()
            cv2.destroyAllWindows()
            t.cancel()
            #cv2.imwrite('path', cropping)
            return 0

    cap.release()
    cv2.destroyAllWindows()
    t.cancel()