





FROM ubuntu:18.04

RUN apt-get update -y && apt-get install -y build-essential cmake \
libsm6 libxext6 libxrender-dev \
python3 python3-pip python3-dev

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY . /app
ENTRYPOINT ["python3"]
#CMD ["web.py"]

CMD ["python", "train_model.py"]
CMD ["python", "facial_req.py"]
