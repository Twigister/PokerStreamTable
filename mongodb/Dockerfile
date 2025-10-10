FROM mongo:8

# Copy configuration and keyfile into the container
COPY mongod.conf /etc/mongo/mongod.conf
COPY keyfile /data/config/keyfile
COPY init.sh /docker-entrypoint-initdb.d/init.sh

RUN chmod 400 /data/config/keyfile && \
    chown mongodb:mongodb /data/config/keyfile && \
    chmod +x /docker-entrypoint-initdb.d/init.sh

# Environment variables (For standalone build)
ENV MONGO_INITDB_ROOT_USERNAME=admin \
    MONGO_INITDB_ROOT_PASSWORD=rootpass \
    MONGO_REPLICA_SET_NAME=rs0

# Expose default MongoDB port
EXPOSE 27017

ENTRYPOINT ["bash", "/docker-entrypoint-initdb.d/init.sh"]
