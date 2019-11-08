FROM python:2

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "fsqueuemon/queuemon.py"]
