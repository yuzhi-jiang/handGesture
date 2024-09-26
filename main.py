import time

from Cv2Camera import Cv2Camera
from defaultCallBack import DeFalutCallBack
from handGesture import Gesture

if __name__ == '__main__':
    # 调用gesture

    # myCamera = Cv2Camera() 使用cv2获取摄像头
    myCamera = Cv2Camera()
    anctionHandler= DeFalutCallBack()
    # 调用piCamera 树莓派5无法使用cv2拍照 需使用piCamera2
    # myCamera = PiCamera()
    ges = Gesture(myCamera,anctionHandler)

    # 收集数据
    # ges.collectData()
    # print("马上开始微调")
    # 等待5秒
    # time.sleep(5)
    # print("开始训练微调")
    # 训练
    # ges.FineTuning(50)
    # 评估
    ges.evaluation()