


1. 创建虚拟环境 如果用的是树莓派5需要继承系统环境
   - python -m venv --system-site-packages venv
2. 安装系统依赖包  如果用的是树莓派5
   - sudo apt install python3-dev libhdf5-dev
   - sudo apt install -y python3-picamera2、
   - sudo apt install libopencv-dev python3-opencv
3. 安装环境包
   - pip3 install scikit-learn
   - pip3 install tensorflow
   - pip3 install mediapipe