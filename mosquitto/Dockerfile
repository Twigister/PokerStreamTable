FROM debian:bullseye

# Mise à jour + installation vsftpd + outils
RUN apt-get update && \
    apt-get install -y mosquitto && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copie de la config MQTT
COPY ./create_mosquitto_file.sh .

RUN chmod +x ./create_mosquitto_file.sh && ./create_mosquitto_file.sh

# Default mosquitto port
EXPOSE 1833

CMD ["mosquitto", "-c", "mosquitto.conf", "-v"]
