import cv2
from abc import ABCMeta, abstractmethod

class ICamera(metaclass=ABCMeta):
    """ICamera interface"""

    @abstractmethod
    def getImage(self):
        pass

    def showImage(self, array):
        # 使用 OpenCV 显示图像
        cv2.imshow('Camera Feed', array)
        cv2.waitKey(0)  # 按任意键关闭预览窗口
        cv2.destroyWindow('Camera Feed')
