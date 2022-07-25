FROM python:3.8-slim

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Updating pip 
RUN pip install --upgrade pip


# Installing needed dependencies 
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev 



COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


# setting env variable of the port 
ENV DATA_MANAGER_MANO_PORT=6001

EXPOSE 6001

# setting env variable of the port 
ENV DATA_MANAGER_INTERNAL_PORT=80

EXPOSE 80

ENTRYPOINT [ "./start.sh" ]
