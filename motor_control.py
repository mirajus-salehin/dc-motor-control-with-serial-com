#!/usr/bi/python
from typing import Final
from datetime import datetime
from hashlib import blake2b
from random import choice
from string import ascii_uppercase
from time import sleep
import cv2
import serial
import logging
from lognotes import Process

SERIAL_PORT_NAME: Final[str] = "/dev/ttyACM0"
BAUD_RATE: Final[int] = 9600
BUFFER_TIMEOUT: Final[float] = 0.1
DELAY_INTERVAL: Final[int] = 1
FORWARD_COMMAND_STRING: Final[str] = "forward"
BACKWARD_COMMAND_STRING: Final[str] = "backward"
CAM_PORT: Final[int] = 0
FILE_NAME_START_STRING_LENGTH: Final[int] = 10


class CameraController:
    def __init__(self) -> None:
        try:
            self.camera = cv2.VideoCapture(CAM_PORT)
        except cv2.error:
            logging.error(Process.failed.camera_init)
        else:
            logging.info(Process.success.camera_init)
        self.filename = self.generate_filename()

    def _image_counter(func):
        def wrapper(*args, **kwargs):
            wrapper.counter += 1    # executed every time the wrapped function is called
            return func(*args, **kwargs)
        wrapper.counter = 1         # executed only once in decorator definition time
        return wrapper

    @_image_counter
    def count(self):
        pass

    def generate_filename(self) -> str:
        _today = datetime.now()
        h = blake2b(digest_size=5)
        h.update(self.convert_to_binary(self.random_string()).encode("utf-8"))
        self.count()
        filename = str(self.count.counter) + "-" + str(_today).replace("-", "") + "-" + h.hexdigest() + ".png"
        return filename

    @staticmethod
    def random_string() -> str:
        letters = ascii_uppercase
        result_str = "".join(choice(letters) for i in range(FILE_NAME_START_STRING_LENGTH))
        return result_str

    @staticmethod
    def convert_to_binary(string: str) -> str:
        binary_string = "".join(format(ord(i), "b") for i in string)
        return binary_string

    def take_photo(self) -> None:
        try:
            _, frame = self.camera.read()
            cv2.imwrite(self.filename, frame)
            self.filename = self.generate_filename()
        except cv2.error:
            logging.error(Process.failed.camera_read)
        else:
            logging.info(Process.success.camera_read)

    def cam_release(self) -> None:
        self.camera.release()


class RobotController:
    def __init__(self) -> None:
        try:
            self.arduino = serial.Serial(SERIAL_PORT_NAME, BAUD_RATE, timeout=BUFFER_TIMEOUT)
        except serial.SerialException:
            logging.error(Process.failed.serial_init)
        else:
            logging.info("Ardunio connected via port {SERIAL_PORT_NAME}")

    def forward(self) -> None:
        sleep(DELAY_INTERVAL)
        self.arduino.write(FORWARD_COMMAND_STRING.encode())
        logging.info(Process.success.serial_write)
        self.arduino.flush()
        sleep(DELAY_INTERVAL)

    def backward(self) -> None:
        sleep(DELAY_INTERVAL)
        self.arduino.write(BACKWARD_COMMAND_STRING.encode())
        logging.info(Process.success.serial_write)
        self.arduino.flush()
        sleep(DELAY_INTERVAL)


def main():
    robot_controller = RobotController()
    camera_controller = CameraController()
    while 1:
        camera_controller.take_photo()
        robot_controller.forward()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            camera_controller.cam_release()
            break


if __name__ == "__main__":
    main()
