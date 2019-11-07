FROM python:latest

WORKDIR /root
COPY ./* /root/
RUN pip install -r requirements.txt
RUN python setup.py install

ENTRYPOINT ["/usr/bin/python", "queuemon.py"]
