FROM python:2

WORKDIR /root
COPY ./* /root/
RUN pip install -r requirements.txt
RUN python setup.py install

ENTRYPOINT ["python", "queuemon.py"]
