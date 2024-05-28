def fact(n):
    return 1 if n==1 or n==0 else n * fact(n-1)

print(fact(5))

import cv2
path = 'media/test_video.mp4'
cap = cv2.VideoCapture(path)

frameWidth = 640
frameHeight = 480
cap.set(3, frameWidth)
cap.set(4, frameHeight)

while True:
    success, img = cap.read()
    if success:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2Lab)
        cv2.imshow('Live', img)
        cv2.imshow('Gray', img_gray)
        
        if cv2.waitKey(10) == ord('q'):
            break
    else:
        break

