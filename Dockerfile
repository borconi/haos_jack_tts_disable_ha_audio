FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y espeak mpg123 alsa-utils mosquitto-clients docker.io && \
    pip install gTTS paho-mqtt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY tts-mqtt.py /tts-mqtt.py
COPY init.sh /init.sh

RUN chmod +x /init.sh

ENTRYPOINT ["/init.sh"]
