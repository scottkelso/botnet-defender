#!/usr/bin/env bash

sudo apt-get update

# Requires Yes confirmation
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

# Requires Yes confirmation
sudo apt-get install docker-ce

# Add docker group
sudo groupadd docker
sudo usermod -aG docker $USER
docker run hello-world