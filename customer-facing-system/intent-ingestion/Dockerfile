FROM node:16-alpine

#  Set Working Directory 
WORKDIR /app

# Copy package.json to install the dependencies
COPY package.json ./
# COPY package-lock.json ./
# Copy project code to the container 
COPY ./ ./
# Install dependencies 
RUN npm i

EXPOSE 3000
# Launch the react application
CMD ["npm", "run", "start"]
