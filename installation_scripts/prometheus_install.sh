#!/bin/bash
# Download key signature
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null

# install required package
sudo apt-get install apt-transport-https --yes
# Adding key to the local repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
# installing 
sudo apt-get update
sudo apt-get install helm
