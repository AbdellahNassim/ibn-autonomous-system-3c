FROM golang:1.18-alpine

WORKDIR /app

# copying the mod and sum files 
COPY go.mod ./
COPY go.sum ./

# Installing dependencies 
RUN go mod download 

# Copying all the files 
COPY *.go ./

# Copying templates also 
COPY ./templates ./templates

# Build the application 
RUN go build -o policy-generator 

ENV POLICY_GENERATOR_PORT 80


EXPOSE 80

# RUNNING the application 
CMD [ "./policy-generator" ]
