FROM python:3.10-slim-bullseye

RUN pip install google-api-python-client oauth2client google-auth-httplib2 Pillow pytelegrambotapi


RUN apt-get update -y
RUN apt-get install -y fonts-dejavu-core

COPY julia_phrases_telebot.py /app/

CMD ["python", "/app/julia_phrases_telebot.py"]



# docker build . -t family_telebot

# docker run --rm -i --env-file=.env --name family_telebot family_telebot


# ----- push to docker hub
# cd family_telebot
# docker login --username=stepall
# pass *******
# docker build . -t stepall/family_telebot:latest
