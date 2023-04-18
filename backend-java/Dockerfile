FROM openjdk:17-ea-jdk-slim

ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
COPY db/* db/

ENTRYPOINT ["java","-jar","/app.jar"]