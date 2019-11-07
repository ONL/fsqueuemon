FROM python:2

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN python setup.py extract_messages

ENTRYPOINT ["python", "queuemon.py"]
