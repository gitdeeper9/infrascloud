# ⚡ INFRAS-CLOUD Installation Guide v1.0.0
## Atmospheric Infrasound & Severe Weather Acoustic Signatures

**DOI**: 10.5281/zenodo.18952438  
**Repository**: github.com/gitdeeper9/infrascloud  
**Web**: infrascloud.netlify.app

---

## 📋 System Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04+, Debian 11+, macOS 12+, Windows 10/11 (WSL2)
- **RAM**: 8 GB
- **Storage**: 20 GB free space
- **Python**: 3.9 - 3.11
- **CPU**: 4+ cores

### Recommended Requirements
- **RAM**: 16+ GB
- **Storage**: 50+ GB SSD
- **CPU**: 8+ cores
- **Python**: 3.10
- **GPU**: CUDA-compatible (optional, for AIEventClassifier)

### Sensor Requirements
- **MB2005 Microbarometer**: USB 2.0+ (4-8 units for array)
- **Paros 2200A**: Serial/USB adapter
- **Nanometrics Centaur**: Ethernet connection
- **Vaisala WXT536**: Serial/USB adapter

---

## 🚀 Quick Installation (5 minutes)

### 1. Install via pip (Recommended)

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install INFRAS-CLOUD
pip install --upgrade pip
pip install infrascloud

# Verify installation
python -c "import infrascloud; print(infrascloud.__version__)"
# Should output: 1.0.0
```

2. Quick Test

```bash
# Download sample data
infrascloud-download-sample --output ./sample_data

# Process sample data
infrascloud-process --input ./sample_data --output ./results

# View results
infrascloud-view --input ./results/aisi.csv
```

3. Start Web Dashboard

```bash
# Start local server
infrascloud-serve --host 127.0.0.1 --port 5000

# Open browser: http://127.0.0.1:5000
```

---

📦 Installation Methods

Method A: pip Install (Production)

```bash
# Basic installation
pip install infrascloud

# With all optional dependencies
pip install infrascloud[all]

# With specific extras
pip install infrascloud[ml]      # Machine learning support
pip install infrascloud[gpu]     # GPU acceleration
pip install infrascloud[sensors] # Sensor drivers
pip install infrascloud[docs]    # Documentation tools
pip install infrascloud[dev]     # Development tools
```

Method B: From Source (Development)

```bash
# Clone repository
git clone https://github.com/gitdeeper9/infrascloud.git
cd infrascloud

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v
```

Method C: Docker (Containerized)

```bash
# Pull from Docker Hub
docker pull gitdeeper9/infrascloud:latest

# Run container
docker run -d \
  --name infrascloud \
  -p 5000:5000 \
  -v $(pwd)/data:/data \
  -v $(pwd)/config:/app/config \
  gitdeeper9/infrascloud:latest

# Or build locally
docker build -t infrascloud:latest .
docker-compose up -d
```

Method D: Conda (Alternative)

```bash
# Create conda environment
conda create -n infrascloud python=3.10
conda activate infrascloud

# Install from conda-forge (once available)
conda install -c conda-forge infrascloud

# Or install via pip in conda
pip install infrascloud
```

---

🔧 Detailed Installation Steps

Step 1: System Dependencies

Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y \
  python3-pip \
  python3-dev \
  python3-venv \
  git \
  build-essential \
  libhdf5-dev \
  libnetcdf-dev \
  libfftw3-dev \
  libusb-1.0-0-dev \
  libatlas-base-dev \
  gfortran
```

macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install \
  python@3.10 \
  git \
  hdf5 \
  netcdf \
  fftw \
  libusb \
  openblas
```

Windows (WSL2)

```powershell
# In PowerShell (Admin)
wsl --install -d Ubuntu

# Then follow Ubuntu instructions in WSL terminal
```

Step 2: Python Environment

```bash
# Create virtual environment
python3 -m venv ~/venv/infrascloud
source ~/venv/infrascloud/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

Step 3: Install INFRAS-CLOUD

```bash
# Core installation
pip install infrascloud

# Verify installation
python -c "
import infrascloud
print(f'INFRAS-CLOUD version: {infrascloud.__version__}')
print(f'Core modules: {infrascloud.__modules__}')
"
```

Step 4: Configure Environment

```bash
# Create configuration directory
mkdir -p ~/.infrascloud

# Download example configuration
curl -o ~/.infrascloud/config.yaml \
  https://raw.githubusercontent.com/gitdeeper9/infrascloud/main/config/config.yaml

# Edit configuration
nano ~/.infrascloud/config.yaml
```

Step 5: Test Installation

```bash
# Run diagnostic
infrascloud-diagnostic --all

# Expected output:
# ✅ Python version: 3.10.x
# ✅ Core modules: installed
# ✅ NumPy: 1.24.x
# ✅ SciPy: 1.10.x
# ✅ ObsPy: 1.4.x
# ✅ Database: connected (if configured)
# ✅ Sensors: detected (if connected)
```

---

🐳 Docker Installation Details

Docker Compose (Full Stack)

```yaml
# docker-compose.yml
version: '3.8'

services:
  infrascloud:
    image: gitdeeper9/infrascloud:latest
    container_name: infrascloud
    ports:
      - "5000:5000"
    volumes:
      - ./data:/data
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - STATION_ID=IS42
      - DB_HOST=timescaledb
      - DB_NAME=infrascloud
      - DB_USER=infrauser
      - DB_PASSWORD=${DB_PASSWORD}
    depends_on:
      - timescaledb
      - redis
    restart: unless-stopped

  timescaledb:
    image: timescale/timescaledb:latest-pg15
    container_name: timescaledb
    environment:
      - POSTGRES_DB=infrascloud
      - POSTGRES_USER=infrauser
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - ./redis_data:/data
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - ./grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus_data:/prometheus
    restart: unless-stopped
```

Start Docker Stack

```bash
# Set environment variables
export DB_PASSWORD=$(openssl rand -base64 32)
export GRAFANA_PASSWORD=admin

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Access services:
# - Web UI: http://localhost:5000
# - Grafana: http://localhost:3000 (admin/admin)
# - Prometheus: http://localhost:9090
```

---

🌐 Web Dashboard Installation

Local Development

```bash
# Install with web extras
pip install infrascloud[web]

# Start development server
infrascloud-serve --debug --host 127.0.0.1 --port 5000
```

Production with Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Start production server
gunicorn -w 4 -b 0.0.0.0:8000 infrascloud.web.app:app
```

Netlify Deployment (Static Dashboard)

```bash
# Build static files
infrascloud-build-static --output ./build

# Deploy with Netlify CLI
npm install -g netlify-cli
netlify deploy --prod --dir=build --site=infrascloud
```

---

🔌 Sensor Driver Installation

MB2005 Microbarometer

```bash
# Install sensor drivers
pip install infrascloud[sensors]

# Test connection
infrascloud-test-sensor --type mb2005 --port /dev/ttyUSB0

# Check data stream
infrascloud-monitor --sensor mb2005 --duration 60

# Calibrate
infrascloud-calibrate --sensor mb2005 --method absolute
```

USB Permission Setup

```bash
# Create udev rules
sudo cat > /etc/udev/rules.d/99-infrascloud.rules << 'EOF'
# MB2005 Microbarometer (FTDI)
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", SYMLINK+="mb2005_%n", MODE="0666"
# Paros 2200A
SUBSYSTEM=="tty", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", SYMLINK+="paros", MODE="0666"
# Vaisala WXT536
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6015", SYMLINK+="vaisala", MODE="0666"
