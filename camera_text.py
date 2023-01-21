import cv2
import time

def take_photo(x:int):
    cap = cv2.VideoCapture(3)
    ret, frame = cap.read()
    cv2.imwrite(str(i) + 'photo.jpg', frame)
    cap.release()

if __name__ == '__main__':
    for i in range(0,5):
        take_photo(i)
        time.sleep(2)