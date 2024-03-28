telegram bot for my family group

Run with Dockerfile

```bash
# вывести неиспользуемые контейнеры
docker images --filter dangling=true -q

# удалить неиспользуемые контейнеры
docker rmi `docker images --filter dangling=true -q`
```

```bash

cd family_telebot
docker build . -t family_telebot && docker rmi `docker images --filter dangling=true -q` 

docker run -i --env-file=.env --restart unless-stopped --name family_telebot family_telebot
docker stop family_telebot && docker rm family_telebot 

docker exec -it family_telebot bash







docker run --rm -i --env-file=.env --name family_telebot family_telebot



----- push to docker hub
cd family_telebot
docker login --username=stepall
pass *******
docker build . -t stepall/family_telebot:latest

```