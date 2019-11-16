FROM python:3 
LABEL maintainer="Zygimantas Magelinskas <zygimantelis@gmail.com>"

WORKDIR /app

COPY requirements.txt ./
COPY ./main.py ./main.py

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT python ./main.py
