FROM rasa/rasa:latest-full

# Setting working directory 
WORKDIR /app

# Copy all configurations 
COPY . /app

USER root 
# Train model 
RUN rasa train

USER 1001
EXPOSE 5005
# Run the rasa module and expose API
CMD ["run","-m", "models", "--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints-docker.yml"]
