# Setting Up Production-Ready VLLM Inference Server

To setup this private LLM inference server, you will need:

- To have access to a linux machine
- Docker and docker compose installed
- A domain name pointing towards your linux macine's public IP address

## Installation

We provide a helper script `setup.sh` to facilitate the configuration. Please review it before using it.

Please set the right values for the environment variables in a `vllm/.env` file (see `.env.example`).

```sh
chmod +x ./setup.sh
sudo ./setup.sh
```

If you prefer running the commands manually, follow the ones provided below:

### System Update

Start by making sure your server is up to date:

```sh
# Search for updates and apply them
sudo dnf upgrade
```

### Firewall

Let's allow HTTP, HTTPS connections and deny the other types by default.

```sh
# Install firewalld
sudo dnf install firewalld

# Start and enable firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Check status
sudo systemctl status firewalld

# Add HTTP and HTTPS services
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https

# Reload to apply changes
sudo firewall-cmd --reload

# Verify configuration
sudo firewall-cmd --list-all
```

### Nvidia Runtime

Make sure the drivers and NVIDIA CUDA Runtime for your GPU are correctly installed and up-to-date.

Then run the following commands to install the NVIDIA runtime for docker containers:

```sh
# Configure production repository
curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo | \
  sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo

# Install nvidia container toolkit
sudo dnf install -y nvidia-container-toolkit

# Configure the nvidia runtime for docker containers
sudo nvidia-ctk runtime configure --runtime=docker

# Restart docker
sudo systemctl docker restart
```

### Docker

```sh
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
```

### Caddy

```sh
# Create necessary Caddy directories
mkdir -p $CADDY_DATA_DIR $CADDY_CONFIG_DIR

# Copy the Caddyfile to the config directory
cp Caddyfile $CADDY_FILE_PATH
```

## Usage

Try requesting the server with:

```sh
curl https://$DOMAIN/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "$MODEL_NAME",
        "prompt": "What's the weather like in Bologna ?",
        "max_tokens": 20,
        "temperature": 0.1
    }'
```
