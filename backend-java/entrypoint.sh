#!/bin/sh

# Copy the db folder contents from the container to the host folder
cp -R /app/db/* /host/db/

# Start the Java application
exec java -jar app.jar