FROM python:3.10-slim-bullseye

RUN pip install google-api-python-client oauth2client google-auth-httplib2 Pillow pytelegrambotapi

COPY julia_phrases_telebot.py .

RUN apt-get update -y
RUN apt-get install -y fonts-dejavu-core

CMD ["python", "julia_phrases_telebot.py"]

# ----- push to docker hub
# cd family_telebot
# docker login --username=stepall
# pass *******
# docker build . -t stepall/family_telebot:latest
# `


# ---- start from docker hub
# docker run stepall/family_telebot

# deploy to Fly.io
# https://dev.to/denvercoder1/hosting-a-python-discord-bot-for-free-with-flyio-3k19