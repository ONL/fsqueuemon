FROM python:2

WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

ENTRYPOINT ["python", "queuemon.py"]
