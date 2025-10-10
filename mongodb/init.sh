#!/bin/bash
set -e

echo "Starting MongoDB standalone for initialization..."
mongod --dbpath /data/db --bind_ip localhost --fork --logpath /var/log/mongodb.log
sleep 5

echo "Creating admin user if missing..."
mongosh admin --quiet --eval "
if (!db.getUser('${MONGO_INITDB_ROOT_USERNAME}')) {
  db.createUser({
    user: '${MONGO_INITDB_ROOT_USERNAME}',
    pwd: '${MONGO_INITDB_ROOT_PASSWORD}',
    roles: [ { role: 'root', db: 'admin' } ]
  });
}
"

echo "Shutting down temporary MongoDB..."
mongod --shutdown --dbpath /data/db

echo "Starting MongoDB with replica set enabled..."
mongod --config /etc/mongo/mongod.conf --fork --logpath /var/log/mongodb.log
sleep 5

echo "Checking replica set status..."
mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin --quiet --eval "
try {
  var status = rs.status();
  print('Replica set already initialized.');
} catch (e) {
  if (e.codeName === 'NotYetInitialized') {
    print('Initializing replica set...');
    rs.initiate({
      _id: '${MONGO_REPLICA_SET_NAME}',
      members: [{ _id: 0, host: 'mongodb:27017' }]
    });
  } else {
    print('Unexpected error checking replica set status: ' + e);
  }
}
"

echo "MongoDB initialized and running with replica set '${MONGO_REPLICA_SET_NAME}'."
exec tail -f /var/log/mongodb.log
