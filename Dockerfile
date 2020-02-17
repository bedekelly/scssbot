FROM ubuntu
USER root
RUN mkdir -p /var/cssbot
WORKDIR /var/cssbot

RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y python3 python3-pip chromium-browser
RUN pip3 install libsass
COPY cssbot.py /var/cssbot

RUN python3 cssbot.py
ENTRYPOINT python3 -m http.server