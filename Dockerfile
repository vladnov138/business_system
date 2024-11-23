FROM python:3.12 as base

RUN pip3 install typing-extensions --upgrade
RUN pip3 install pyrtf3
RUN pip3 install -U connexion[flask]
RUN pip3 install -U connexion[swagger-ui]
RUN pip3 install -U connexion[uvicorn]
RUN pip3 install -U flask-restplus
RUN pip3 install -U Flask
RUN pip3 install -U matplotlib
RUN pip3 install -U pandas

COPY ./src ./src
COPY ./resources ./resources
COPY ./main.py ./main.py
COPY ./swagger.yaml ./swagger.yaml

CMD ["python3", "main.py"]