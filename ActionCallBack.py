from abc import ABCMeta, abstractmethod




class IActionCallBack(metaclass=ABCMeta):

    @abstractmethod
    def getGesture(self, actions):
        pass

    @abstractmethod
    def doAction(self, actions):
        pass