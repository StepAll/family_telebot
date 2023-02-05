FROM python:3.10-slim-bullseye

WORKDIR /family_telebot

RUN pip install google-api-python-client
RUN pip install oauth2client
RUN pip install google-auth-httplib2

RUN pip install Pillow
RUN pip install pytelegrambotapi

RUN pip install python-dotenv

COPY family-telebot-key.json .
COPY family_telebot2.py .

RUN apt-get update -y
RUN apt-get install -y fonts-dejavu-core


CMD ["python", "family_telebot.py"]

# ----- push to docker hub
# cd family_telebot
# docker login --username=stepall
# pass *******
# docker build . -t stepall/family_telebot:latest
# `


# ---- start from docker hub
# docker run stepall/family_telebot
