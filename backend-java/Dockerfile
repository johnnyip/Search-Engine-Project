FROM openjdk:17-ea-jdk-slim

# Set the working directory
WORKDIR /app

ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar

# Copy the db folder into the /app/db directory inside the container
COPY ./db_init /app/db_init
COPY ./db /app/db
COPY ./_files /app/_files

# Copy the entrypoint.sh script into the container
COPY entrypoint.sh /app/

# Set the ENTRYPOINT for running the entrypoint.sh script
ENTRYPOINT ["./entrypoint.sh"]
