FROM python:3.10-slim-bullseye

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update -y
RUN apt-get install -y fonts-dejavu-core

COPY julia_phrases_telebot.py /app/
# COPY parse_kassir_vc_proton.py /app/

COPY start.sh .

CMD ["bash", "start.sh"]
