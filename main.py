from Cv2Camera import Cv2Camera
from handGesture import Gesture

if __name__ == '__main__':
    # 调用gesture

    # myCamera = Cv2Camera() 使用cv2获取摄像头
    myCamera = Cv2Camera()
    # 调用piCamera 树莓派5无法使用cv2拍照 需使用piCamera2
    # myCamera = PiCamera()
    ges = Gesture(myCamera)

    # 收集数据
    # ges.collectData()
    # 训练
    # ges.train()
    # 评估
    ges.evaluation()