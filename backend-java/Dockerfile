FROM openjdk:17-ea-jdk-slim

WORKDIR /app

ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar

COPY db /app/db
COPY entrypoint.sh /app/

# Set the ENTRYPOINT for running the entrypoint.sh script
ENTRYPOINT ["java","-jar","/app/app.jar"]