#!/bin/bash

# Update system dependencies
sudo dnf upgrade -y

# Install and configure Firewalld
sudo dnf install firewalld -y

# Start and enable firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Add SSH, HTTP and HTTPS services
# TODO(high): update to only accept requests from cloudflare servers for requests other than SSH
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

# Configure production repository for nvidia-container-toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.repo | \
  sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo

# Install nvidia container toolkit
sudo dnf install -y nvidia-container-toolkit

# Configure the nvidia runtime for docker containers
sudo nvidia-ctk runtime configure --runtime=docker

# Restart docker
sudo systemctl docker restart

# TODO: replace caddy automated configuration with traefik
# Create necessary Caddy directories
mkdir -p $CADDY_DATA_DIR $CADDY_CONFIG_DIR

# Copy the Caddyfile to the config directory
cp ./Caddyfile $CADDY_FILE_PATH

# Install uv python manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create Huggingface cache directory
mkdir -p $HF_CACHE_DIR

# Install HF-CLI and download the model to the cache directory
uv run --with "huggingface_hub[cli]" huggingface-cli login --token $HF_HUB_TOKEN
uv run --with "huggingface_hub[cli]" huggingface-cli download $MODEL_NAME --cache-dir=$HF_CACHE_DIR

echo "Setup complete! You can now run 'sudo docker compose up -d'"
