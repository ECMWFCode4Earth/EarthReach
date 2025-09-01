# Setting Up Production-Ready VLLM Inference Server

To setup this private LLM inference server, you will need:

- To have access to a linux machine
- Docker and docker compose installed
- A domain name pointing towards your linux machine's public IP address (configured with Cloudflare for DNS and SSL)
- A Cloudflare account with API access for DNS challenges

## Installation

We provide a helper script `setup.sh` to facilitate the configuration. Please review it before using it.

Please set the right values for the environment variables in a `vllm/.env` file (see `.env.example`):

- `DOMAIN`: Your domain name (e.g., api.yourdomain.com)
- `CF_DNS_TOKEN`: Cloudflare API token with DNS permissions
- `CF_ACME_EMAIL`: Email address for Let's Encrypt certificates
- `CF_IPS`: Cloudflare IP ranges for proxy protocol
- `TRAEFIK_ROOT_DIR`: Directory for Traefik configuration and certificates
- `HF_CACHE_DIR`: Directory for Hugging Face model cache
- `MODEL_NAME`: The model to serve (e.g., "google/gemma-3-4b-it")
- `MODEL_DIR_PATH`: Full path to the downloaded model directory
- `HF_HUB_TOKEN`: Hugging Face Hub token for model access
- `VLLM_SERVER_API_KEY`: API key for accessing the VLLM server
- `VLLM_PORT`: Port for the VLLM server (default: 8000)

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

### Traefik

```sh
# Create necessary Traefik directories
mkdir -p $TRAEFIK_ROOT_DIR/traefik/cert

# Set proper permissions for the certificate storage
chmod 600 $TRAEFIK_ROOT_DIR/traefik/cert
```

### Cloudflare Configuration

This setup uses Cloudflare for DNS management and SSL certificate provisioning via DNS challenges. You'll need:

1. **Domain Configuration**: Your domain must be managed by Cloudflare
2. **API Token**: Create a Cloudflare API token with the following permissions:
   - Zone:Zone:Read
   - Zone:DNS:Edit
   - Zone:Zone Settings:Read
3. **Trusted IPs**: Configure Cloudflare's IP ranges for proxy protocol (set in CF_IPS environment variable)

## Usage

Try requesting the server with:

```sh
curl https://$DOMAIN/v1/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $VLLM_SERVER_API_KEY" \
    -d '{
        "model": "$MODEL_NAME",
        "prompt": "What's the weather like in Bologna ?",
        "max_tokens": 20,
        "temperature": 0.1
    }'
```

Note: Make sure to enable the Traefik labels in your docker-compose.yaml by uncommenting the labels section for the vllm-server service before running `docker compose up -d`.
