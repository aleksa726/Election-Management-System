FROM python:3

RUN mkdir -p /opt/src/user
WORKDIR /opt/src/user

COPY admin/user.py ./user.py
COPY admin/configuration.py ./configuration.py
COPY admin/models.py ./models.py
COPY admin/requirements.txt ./requirements.txt
COPY admin/adminDecorator.py ./adminDecorator.py

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./user.py"]