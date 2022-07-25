FROM python:3.8-alpine

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Updating pip 
RUN pip install --upgrade pip


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 80

ENTRYPOINT ["python3",  "app.py"]
