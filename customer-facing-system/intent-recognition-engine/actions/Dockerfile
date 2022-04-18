FROM rasa/rasa-sdk:latest

# Setting the working Directory 
WORKDIR /app

# COPY requirements 
COPY ../requirements.txt /app/

# Install dependencies 
RUN pip install --verbose -r requirements

# Expose the port 
EXPOSE 5055
# Launch the actions server 
CMD ["rasa","run", "actions"]