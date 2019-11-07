FROM python:2

WORKDIR /app
RUN pip install -r requirements.txt
COPY ./* /app

RUN python setup.py install

ENTRYPOINT ["python", "queuemon.py"]
