FROM python:3.10-slim-bullseye

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update -y
RUN apt-get install -y fonts-dejavu-core

COPY julia_phrases_telebot.py /app/
COPY parse_kassir_vc_proton.py /app/

CMD ["python", "/app/julia_phrases_telebot.py"]



# docker build . -t family_telebot

# docker run --rm -i --env-file=.env --name family_telebot family_telebot

# docker exec -it family_telebot bash
# python /app/parse_kassir_vc_proton.py

# ----- push to docker hub
# cd family_telebot
# docker login --username=stepall
# pass *******
# docker build . -t stepall/family_telebot:latest
