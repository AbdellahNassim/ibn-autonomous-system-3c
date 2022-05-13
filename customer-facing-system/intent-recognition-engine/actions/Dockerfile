FROM rasa/rasa-sdk:latest

# Setting the working Directory 
WORKDIR /app

# COPY requirements 
COPY ./requirements.txt /app/




USER root

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev 

# Install requirements 
RUN pip install --verbose -r requirements.txt

# COPY all the working directory containing actions
COPY . /app/

# Expose the port of the custom server 
EXPOSE 5055

# Switch back to user
USER 1001
