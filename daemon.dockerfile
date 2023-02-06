FROM python:3

RUN mkdir -p /opt/src/daemon
WORKDIR /opt/src/daemon

COPY admin/daemon.py ./daemon.py
COPY admin/configuration.py ./configuration.py
COPY admin/models.py ./models.py
COPY admin/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./daemon.py"]