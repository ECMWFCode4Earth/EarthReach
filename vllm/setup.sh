#!/bin/bash

# Update system dependencies
sudo dnf upgrade -y

# Install and configure Firewalld
sudo dnf install firewalld -y

# Start and enable firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Add SSH, HTTP and HTTPS services
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https

# Reload to apply changes
sudo firewall-cmd --reload

# Install Docker dependencies (as per https://docs.docker.com/engine/install/rhel/)
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
sudo dnf install -y docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

# Enable and start Docker
sudo systemctl enable --now docker

# Create necessary Caddy directories
mkdir -p $CADDY_DATA_DIR $CADDY_CONFIG_DIR

# Copy the Caddyfile to the config directory
cp ./Caddyfile $CADDY_FILE_PATH

echo "Setup complete! You can now run 'sudo docker compose up -d'"