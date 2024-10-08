import cv2
import keras
import numpy as np
import os

from ActionCallBack import IActionCallBack
from ICamera import ICamera
from bone import BoneDetector
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Flatten
from camera import Camera

# 已经训练的动作
actions = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'good', 'not good', 'ok',
            "sotp"]

class Gesture():
    def __init__(self,myCamera: ICamera, doActionCallBack: IActionCallBack) -> None:
        #已经做的动作 存放下标
        self.doActions = []
        self.doActionCallBack=doActionCallBack
        self.camera = myCamera
        self.action_type = 'static'  # ['static', 'dynamic']
        self.model_name = 'dAction.h5'
        self.data_path = os.path.join('Data', self.action_type)
        self.model_path = os.path.join('Model', self.model_name)
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)
        self.actions = np.array(actions)
        self.label_map = {label: num for num, label in enumerate(self.actions)}

        self.action_num = 300  # 每种动作收集的数据个数
        self.landmark_num = 21 * 3  # 每个动作的数据长度

        self.detector = BoneDetector()
        self.epochs = 1000
        self.test_size = 0.2  # 测试数据比例
        self.pre_action = None
        self.action_index = 0

    def collectData(self):
        """ 收集数据 """

        for action in self.actions:
            lm_data = np.zeros(self.landmark_num).reshape((1, -1))
            # frame_num = lm_data.shape[0] - 1
            for frame_num in range(self.action_num):
                flag, frame = self.getImg()
                frame = cv2.flip(frame, 1)
                if not flag:
                    print("Ignoring empty camera frame.")
                    continue
                frame = self.detector.drawBone(frame)

                if frame_num == 0:
                    cv2.putText(frame, 'Start collection {}'.format(action), (120, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                    cv2.putText(frame, 'Action: {} No.: {}'.format(action, frame_num), (50, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                    # Show to screen
                    cv2.imshow('OpenCV Feed', frame)
                    cv2.waitKey(5000)
                else:
                    cv2.putText(frame, 'Action {} No. {}'.format(action, frame_num), (50, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                    # Show to screen
                    cv2.imshow('OpenCV Feed', frame)

                if self.detector.results.multi_hand_landmarks:
                    tmp = np.array([[res.x, res.y, res.z] for res in
                                    self.detector.results.multi_hand_landmarks[0].landmark]).flatten()
                    tmp.reshape((1, -1))
                    lm_data = np.vstack([lm_data, tmp])

                # frame_num = lm_data.shape[0] - 1
                if cv2.waitKey(50) & 0xFF == 27:
                    break
            npy_path = os.path.join(self.data_path, action)
            print('Action: {}, data_length: {}'.format(action, lm_data.shape))
            np.save(npy_path, lm_data[1:, :])

    def loadDate(self):
        X = np.zeros((1, self.landmark_num))
        y = np.zeros((1,))
        for action in self.actions:
            res = np.load(os.path.join(self.data_path, "{}.npy".format(action)))
            lab = np.zeros((res.shape[0],))
            lab.fill(self.label_map[action])
            X = np.vstack([X, res])
            y = np.hstack([y, lab])
        X, y = X[1:, :], y[1:]
        print(X.shape)
        print(y.shape)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size)
        return X_train, X_test, y_train, y_test

    def getModel(self):
        model = Sequential()
        model.add(Flatten(input_shape=(self.landmark_num,)))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(256, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(len(self.actions), activation='softmax'))
        model.compile(optimizer='Adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def train(self):
        """ 训练过程 """
        X_train, X_test, y_train, y_test = self.loadDate()

        model = self.getModel()

        model.fit(X_train, y_train, epochs=self.epochs)

        test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
        print('\nTest accuracy:{}, loss: {}'.format(test_acc, test_loss))

        model.save(self.model_path)

    # 模型微调，基于当前模型继续训练
    def FineTuning(self,epochs=50):
        # 1. 加载模型
        model = tf.keras.models.load_model(self.model_path)
        # 2. 加载数据
        X_train, X_test, y_train, y_test = self.loadDate()

        optimizer = keras.optimizers.Adam()  # 或者您所用的其他优化器

        # 重新编译模型，使用新创建的优化器
        model.compile(optimizer=optimizer,
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])

        # 3. 微调模型
        history = model.fit(X_train, y_train, epochs=epochs, validation_data=(X_test, y_test))
        test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
        print('\nTest accuracy:{}, loss: {}'.format(test_acc, test_loss))

        model.save(self.model_path)


    def evaluation(self):

        model = tf.keras.models.load_model(self.model_path)

        while True:
            # flag, frame = self.cap.read()

            flag, frame = self.getImg()
            frame = cv2.flip(frame, 1)
            if not flag:
                print("empty camera frame")
                break
            # 1. 获取手部节点数据
            frame = self.detector.drawBone(frame)

            # 2. 使用模型预测动作
            if self.detector.results.multi_hand_landmarks:
                x_train = np.array(
                    [[res.x, res.y, res.z] for res in self.detector.results.multi_hand_landmarks[0].landmark]).flatten()
                x_train = np.reshape(x_train, (1, -1))
                y_pre = model.predict(x_train)
                index=np.argmax(y_pre[0])
                act = self.actions[np.argmax(y_pre[0])]
                if act == self.pre_action:
                    self.action_index += 1
                else:
                    self.pre_action = act
                    self.action_index = 0
                    self.doActions.append(index)
                    self.tryDoActionsCallback()
                cv2.putText(frame, 'Action is: {}, index: {}'.format(act, self.action_index), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3, cv2.LINE_AA)
            cv2.imshow("DAction", frame)

            # frame_num = lm_data.shape[0] - 1
            if cv2.waitKey(50) & 0xFF == 27:
                break


    def tryDoActionsCallback(self):
        flag = self.doActionCallBack.doAction(self.doActions)
        if flag:
            self.doActions.clear()

    def getImg(self):
        flag, img_array = self.camera.getImage()  # 获取图像数组
        return flag, img_array


if __name__ == '__main__':
    ges = Gesture()
    # ges.collectData()
    # ges.train()
    ges.evaluation()
