FROM python:3.8-slim
RUN apt update && apt install curl ngrep -y 
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt
COPY . /code
