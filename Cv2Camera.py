import cv2
import time
from ICamera import ICamera  # 确保正确导入

class Cv2Camera(ICamera):
    """摄像头类"""

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("无法打开摄像头，请检查设备连接！")
            exit()
        time.sleep(1)  # 等待摄像头准备

    def getImage(self):
        return self.cap.read()


    def close(self):
        # 关闭摄像头（如果需要）
        self.cap.release()  # 释放资源

if __name__ == "__main__":
    cv2Camer = Cv2Camera()
    flag, img = cv2Camer.getImage()
    cv2Camer.showImage(img)
