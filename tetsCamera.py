#
# import cv2
# import numpy as np
# from picamera2 import Picamera2
#
# # 初始化 PiCamera2
# picamera2 = Picamera2()
# picamera2.configure(picamera2.create_preview_configuration())
#
# # 启动摄像头
# picamera2.start()
#
# # 捕获图像
# image_data = picamera2.capture_array()
# picamera2.stop()
#
# # 将捕获的图像数据转换为 OpenCV 格式
# # image_data 是一个 NumPy 数组，默认是 RGB 格式
# # OpenCV 使用 BGR 格式，因此需要转换
# image_bgr = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
#
# # 显示图像
# cv2.imshow("Captured Image", image_bgr)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# # 保存图像
# cv2.imwrite("captured_image.jpg", image_bgr)