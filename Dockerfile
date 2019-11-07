FROM python:latest

RUN ls -l && pwd
RUN pip install -r requirements.txt
RUN python setup.py install

ENTRYPOINT ["/usr/bin/python", "queuemon.py"]
