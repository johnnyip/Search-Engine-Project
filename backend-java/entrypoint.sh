#!/bin/sh

# Copy the db folder contents from the container to the host folder
cp -R /app/db_init/* /app/db/

chmod -R 777 /app/db

# Start the Java application with a relative path to the JAR file
exec java -jar /app/app.jar