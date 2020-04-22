FROM fedora

COPY . /opt
WORKDIR /opt/fsqueuemon
RUN dnf upgrade -y && \
    dnf install -y \
      dumb-init \
      python-gunicorn \
      python3-urllib3 \
      python-flask \
      python-flask-babel \
      python-babel \
    && dnf clean all

EXPOSE 8000
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["gunicorn -w 4 -b 0.0.0.0:8000 queuemon:app"]
