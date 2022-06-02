FROM golang:1.18-alpine

WORKDIR /app

# copying the mod and sum files 
COPY go.mod ./
COPY go.sum ./

# Installing dependencies 
RUN go mod download 

# Copying all the files 
COPY *.go ./

# Build the application 
RUN go build -o policy-generator 


EXPOSE 8080

# RUNNING the application 
CMD [ "./policy-generator" ]