FROM openjdk:8-jdk-alpine

ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar

# Copy the "lib" folder and its .jar files into the Docker image
COPY lib /lib

# Add the .jar files from the "lib" folder to the classpath when running the application
ENTRYPOINT ["java", "-cp", "/app.jar:/lib/*", "org.springframework.boot.loader.JarLauncher"]
