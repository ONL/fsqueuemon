FROM python:latest

RUN pip install -r requirements.txt
RUN python setup.py install

ENTRYPOINT ["/usr/bin/python", "queuemon.py"]
