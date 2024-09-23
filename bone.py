import cv2
import mediapipe as mp

from Cv2Camera import Cv2Camera
from camera import Camera
class BoneDetector:
    def __init__(self, static_image_mode=False,
                        max_num_hands=2,
                        model_complexity=0,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5,
                        ) -> None:
        """
        手部识别初始化函数。

        参数:
            static_image_mode (bool): 是否处理静态图片，默认为False。
            max_num_hands (int): 最多检测的手数，默认为2。
            model_complexity (int): 模型复杂度，默认为0。
            min_detection_confidence (float): 检测置信度阈值，默认为0.5。
            min_tracking_confidence (float): 跟踪置信度阈值，默认为0.5。

        返回:
            None
        """
        # 导入手部识别模块
        self.mp_hands = mp.solutions.hands
        # 初始化手部识别对象
        self.hands = self.mp_hands.Hands(static_image_mode=static_image_mode,
                                        max_num_hands=max_num_hands,
                                        model_complexity=model_complexity,
                                        min_detection_confidence=min_detection_confidence,
                                        min_tracking_confidence=min_tracking_confidence)
        # 导入绘制工具模块
        self.mp_drawing = mp.solutions.drawing_utils
        # 导入绘制样式模块
        self.mp_drawing_styles = mp.solutions.drawing_styles
        # 初始化识别结果变量
        self.results = None


    def drawBone(self, image):
        """
        在图像上绘制手部骨骼结构。

        参数:
        image (numpy.ndarray): 输入的BGR图像。

        返回:
        numpy.ndarray: 绘制了手部骨骼结构的RGB图像。
        """
        # 禁止图像原始数据被修改，提高处理效率
        image.flags.writeable = False
        # 将图像从BGR颜色空间转换为RGB颜色空间，以便与mediapipe兼容
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 使用mediapipe Hands模型处理图像，检测手部关键点
        self.results = self.hands.process(image)
        # 重新允许图像数据被修改，准备后续可能的图像操作
        image.flags.writeable = True
        # 将图像从RGB颜色空间转换回BGR颜色空间，以便使用OpenCV进行绘制
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        # 如果检测到手部关键点
        if self.results.multi_hand_landmarks:
            # 遍历每一只手的关键点
            for hand_landmarks in self.results.multi_hand_landmarks:
                # 在图像上绘制手部骨骼结构
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
        # 返回处理后的图像
        return image

    def drawBox(self, image) -> list:
        """
        在图像中绘制手部边界框。

        参数:
        img (numpy.ndarray): 输入的图像，格式为BGR。

        返回:
        list: 包含所有检测到的手的边界框坐标列表，每个边界框的坐标为(xmin, ymin, boxW, boxH)。
        """
        bboxs = []
        image_height, image_width, _ = image.shape

        if not self.results.multi_hand_landmarks:
            return bboxs

        index = 0
        for hand_landmarks in self.results.multi_hand_landmarks:
            xList, yList = [], []
            for _, lm in enumerate(hand_landmarks.landmark):
                xList.append(int(lm.x * image_width))
                yList.append(int(lm.y * image_height))

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            boxW, boxH = xmax - xmin, ymax - ymin
            bbox = xmin, ymin, boxW, boxH

            try:
                hand_type = self.results.multi_handedness[index].classification[0].label
            except IndexError:
                hand_type = "Unknown"

            cv2.rectangle(image,
                          (bbox[0] - 25, bbox[1] - 25),
                          (bbox[0] + bbox[2] + 25, bbox[1] + bbox[3] + 25),
                          (0, 255, 0),
                          1)

            cv2.putText(image,
                        f"number: {index}, hand: {hand_type}",
                        (xmin - 25, ymin - 20),
                        cv2.FONT_HERSHEY_PLAIN,
                        1,
                        (0, 0, 255),
                        1)

            index += 1
            bboxs.append(bbox)

        return bboxs


# 主程序入口
if __name__ == '__main__':
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    # 检查摄像头是否成功打开
    if not cap.isOpened():
        print("无法打开摄像头，请检查设备连接！")
        exit()
    # 创建摄像头对象，用于后续获取图像数据
    camera = Cv2Camera()
    # 创建骨骼检测器对象
    detector = BoneDetector()
    print("按下esc键退出")
    # 循环读取摄像头的帧，直到摄像头关闭或检测到退出条件
    while True:
        # 从摄像头对象中获取图像数组
        isOpen,array = camera.getImage()
        if not isOpen:
            break
        # 翻转图像，用于镜像显示
        frame = cv2.flip(array, 1)
        # 在图像上绘制检测到的骨骼
        frame = detector.drawBone(frame)
        # 在图像上绘制检测到的骨骼框
        detector.drawBox(frame)
        # 显示处理后的图像
        cv2.imshow('MediaPipe bone', frame)
        # 检测是否按下esc键，按下则退出循环
        if cv2.waitKey(50) & 0xFF == 27:
            break
