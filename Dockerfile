FROM python:3

WORKDIR /yuztanima

COPY . /yuztanima

RUN apt-get update

RUN python -m pip install --upgrade pip

RUN pip install --user  imutils











RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT ["python3", "train_model.py"]
ENTRYPOINT ["python3", "facial_req.py"]

