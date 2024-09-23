import time

import cv2
from picamera2 import Picamera2

from ICamera import ICamera


class PiCamera(ICamera):
    def __init__(self):
        self.picam2 = Picamera2()  # 创建摄像头对象
        self.picam2.configure(self.picam2.create_preview_configuration())
        self.picam2.start()  # 启动摄像头
        time.sleep(1)

    def getImage(self):
        image_data = self.picam2.capture_array()
        image_bgr = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
        return self.picam2.is_open,image_bgr

    def close(self):
        # 关闭摄像头（如果需要）
        self.picam2.close()  # 关闭摄像头，释放资源
        self.picam2.stop()
