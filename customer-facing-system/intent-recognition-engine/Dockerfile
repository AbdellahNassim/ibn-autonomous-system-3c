FROM rasa/rasa:latest-full

# Setting working directory 
WORKDIR /app

# Copy all configurations 
COPY . /app

# Train model 
RUN rasa train

# Run the rasa module and expose API
CMD ["run","--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints-docker.yml"]
