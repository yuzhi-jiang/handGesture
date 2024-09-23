import array
from Cv2Camera import Cv2Camera
class Camera:
    def __init__(self) -> None:
        self.camera = Cv2Camera()
    def getImage(self) -> (bool, array):
        return self.camera.getImage()
    def showImage(self, array) -> None:
        self.camera.showImage(array)
if __name__ == "__main__":
    camera = Camera()
    _,img_array = camera.getImage()
    # frame = cv2.flip(img_array, 1)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    camera.showImage(img_array)
    camera.close()