'''
FROM python:3

WORKDIR /yuztanima

COPY . /yuztanima

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
#RUN apt-get update && apt-get install -y python3-opencv
#RUN pip install opencv-python
RUN apt-get update && apt-get install -y --no-install-recommends \
    libopencv-dev \
    python3-opencv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN python -m pip install --upgrade pip

RUN pip install --user  imutils

RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT ["python3", "train_model.py"]
ENTRYPOINT ["python3", "facial_req.py"]










FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-numpy \
    python3-scipy \
    python3-pandas \
    python3-matplotlib \
    python3-sklearn \
    python3-opencv \
    python3-pil \  
    libraspberrypi-bin \    



WORKDIR /usr/src/app

RUN wget http://node-arm.herokuapp.com/node_latest_armhf.deb 
RUN sudo dpkg -i node_latest_armhf.deb

COPY package*.json ./
RUN npm install

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install --user  imutils
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "train_model.py"]
ENTRYPOINT ["python3", "facial_req.py"]
'''
