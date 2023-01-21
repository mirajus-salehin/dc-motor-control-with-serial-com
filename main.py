import serial
import time
import cv2

action = "forward"
cam = cv2.VideoCapture(2)
ser = serial.Serial('/dev/ttyACM1', 9600,timeout=1)
def take_photo(x:int):
    cap = cv2.VideoCapture(3)
    ret, frame = cap.read()
    cv2.imwrite(str(x) + 'photo.jpg', frame)
    ser.flush()
    ser.write(action.encode())
    cap.release()

if __name__ == "__main__":
    
    
    time.sleep(2)
    print("Sending")
    ret, frame = cam.read()
    for i in range(0,5):
        take_photo(i)
    
    time.sleep(5)
    print("Done")