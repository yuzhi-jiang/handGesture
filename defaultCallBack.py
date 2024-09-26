import concurrent

import webHookAction
from ActionCallBack import IActionCallBack

all_gesture_dict = {
    "切换卧室灯": [0, 4],
    "调大音量": [8, 1]
}
#all_gesture_dict 的值中最大长度
max_len = max(len(vals) for vals in all_gesture_dict.values())

def isAllContains(list1, list2):
    return all(item in list2 for item in list1)

class DeFalutCallBack(IActionCallBack):
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    def getGesture(self, actions):
        # actions中有值如 1,2
        # 匹配all_gesture_dict中的每个key，如果value列表中包含actions，则返回key
        for key, vals in all_gesture_dict.items():  # 使用items()方法遍历字典
            if( len(actions)==len(vals) and vals==actions):
                return key
            if len(actions)-3>=len(vals) and isAllContains(vals, actions[-(len(vals)+3):]):  # 检查actions中的所有值是否在vals中
                return key  # 返回匹配的key
        return None  # 如果没有匹配，返回None

    def doAction(self, actions):
        print(actions)
        gesture = self.getGesture(actions)
        if gesture:
            print('识别到手势:', gesture)

            self.executor.submit(webHookAction.send_gesture,gesture)
            return True
        elif len(actions)>max_len+5:
            return True
        else:
            print("未识别手势")
        return False

if __name__ == '__main__':
    a=[1,2,0,1,4]
    #取最后2个元素
    print(a[-2:])

    handler = DeFalutCallBack()
    result = handler.getGesture(a)  # 传入一个动作列表
    print(result)  # 输出: 切换灯光

    # result = handler.getGesture([8,1])  # 传入一个动作列表
    # print(result)  # 输出: 调大音量