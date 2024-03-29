FROM python:3

RUN mkdir -p /opt/src/authentication
WORKDIR /opt/src/authentication
ENV TZ=Europe/Belgrade
COPY authentication/application.py ./application.py
COPY authentication/configuration.py ./configuration.py
COPY authentication/models.py ./models.py
COPY authentication/requirements.txt ./requirements.txt
COPY authentication/adminDecorator.py ./adminDecorator.py

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./application.py"]