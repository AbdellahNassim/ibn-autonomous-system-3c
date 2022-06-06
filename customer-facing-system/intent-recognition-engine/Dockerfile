FROM rasa/rasa:3.1.0-full

# Setting working directory 
WORKDIR /app

# Copy all configurations 
COPY . /app


RUN pip install -r  requirements.txt


USER root 
# Train model 
RUN rasa train



EXPOSE 5005
# Run the rasa module and expose API
CMD ["run","-m", "models", "--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints-docker.yml"]
