# ⚡ INFRAS-CLOUD Deployment Guide v1.0.0
## Atmospheric Infrasound & Severe Weather Acoustic Signatures

**DOI**: 10.5281/zenodo.18952438  
**Repository**: github.com/gitdeeper9/infrascloud  
**Web**: infrascloud.netlify.app

---

## 📋 Deployment Overview

This guide covers deployment options for INFRAS-CLOUD monitoring stations across different environments.

### Deployment Architectures

| Architecture | Use Case | Resources | Detection Range |
|-------------|----------|-----------|-----------------|
| **Single Station** | Local severe weather monitoring | 1 server | 280 km (tornado) |
| **3-Station Triangle** | Regional network (minimal) | 3 servers | 1,000 km |
| **Full Array (4-8)** | Operational IMS-style network | 4-8 servers | 4,200+ km |
| **Cloud-Based** | Global monitoring network | Auto-scaling | 12,000 km |

---

## 🏗️ Architecture Components

```

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Microbarometer │────▶│  Digitizer      │────▶│  Local Storage  │
│  Array (4-8)    │     │  (Centaur)      │     │  (MiniSEED)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
│                       │                       │
└───────────────────────┼───────────────────────┘
▼
┌─────────────────┐
│  InfrasProcessor│
│  (Real-time)    │
└─────────────────┘
│
┌────────────────┼────────────────┐
▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ BeamFormer  │  │DuctingAnaly │  │AIEventClass │
│ (f-k)       │  │ (D_str)     │  │ (6-class)   │
└─────────────┘  └─────────────┘  └─────────────┘
│                │                │
└────────────────┼────────────────┘
▼
┌─────────────────┐
│  AISI Composite │
│  (0-1)          │
└─────────────────┘
│
┌────────────────┼────────────────┐
▼                ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Alerts    │  │  Dashboard  │  │  Cloud Sync │
│ (Email/SMS) │  │  (Netlify)  │  │  (Optional) │
└─────────────┘  └─────────────┘  └─────────────┘

```

---

## 🔧 Local Deployment (Single Station)

### 1. Hardware Requirements

```yaml
Minimum Specifications:
  CPU: Intel NUC i5 / 4+ cores
  RAM: 8GB
  Storage: 500GB SSD (for raw data)
  Network: 4G/LTE modem (for remote sites)
  Power: Solar + Battery backup (200W panel, 200Ah battery)
  
Sensor Requirements:
  Microbarometer: MB2005 (CEA/DAM France) or equivalent
    - Frequency response: 0.005-27 Hz
    - Dynamic range: 120 dB
    - Noise floor: < 10⁻³ Pa/√Hz
    - Quantity: 4-8 elements
  
  Digitizer: Nanometrics Centaur or equivalent
    - 24-bit resolution
    - GPS timing: ±100 ns
    - MiniSEED output
  
  Weather Station: Vaisala WXT536 (for α_air correction)
    - Temperature, humidity, pressure, wind
  
  Wind Noise Reduction:
    - Rosette pipe array (72-port, 70 m diameter)
    - Installed at soil depth 0.3 m
    - Reduces wind noise by 20-30 dB at 0.1-5 Hz
```

2. Installation Steps

```bash
# 1. Prepare the system
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip docker.io docker-compose git

# 2. Clone repository
git clone https://github.com/gitdeeper9/infrascloud.git
cd infrascloud

# 3. Configure environment
cp .env.example .env
nano .env  # Edit with your station details

# 4. Install Python package
pip install --upgrade pip
pip install infrascloud

# Or install from source
pip install -e .

# 5. Configure USB permissions for microbarometers
sudo cp config/udev/99-infrascloud.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules

# 6. Test sensors
python -m infrascloud.cli.test_sensors --all

# 7. Initialize database
python -m infrascloud.cli.init_db

# 8. Start services
docker-compose -f docker-compose.dev.yml up -d

# 9. Verify deployment
curl http://localhost:5000/health
python -m infrascloud.cli.verify_deployment
```

3. Station Configuration Example

```yaml
# config/station.yaml
station:
  id: "IS42_AZORES_01"
  name: "Azores Infrasound Array"
  latitude: 38.5
  longitude: -28.5
  elevation: 100
  network: "IMS"
  deployment_date: "2026-03-11"

sensors:
  microbarometer_array:
    enabled: true
    elements: 8
    base_port: "/dev/ttyUSB"
    baudrate: 115200
    sample_rate: 20
    spacing: 2000  # meters (2 km)
    geometry: "octagonal"
    calibration_file: "config/calibration/mb2005_2026.json"
  
  digitizer:
    enabled: true
    type: "centaur"
    ip: "192.168.1.100"
    port: 5000
    sample_rate: 20
    channels: 8
  
  weather_station:
    enabled: true
    type: "vaisala_wxt536"
    port: "/dev/ttyUSB8"
    baudrate: 19200
    interval: 60

processing:
  wavelet:
    fs: 20
    fmin: 0.001
    fmax: 20
    omega0: 6
    window_length: 60  # seconds
  
  beamforming:
    weighting: "dolph-chebyshev"
    window_length: 256  # seconds
    overlap: 0.75
    theta_resolution: 1  # degrees
    v_ph_range: [300, 360]  # m/s
  
  detection:
    coherence_threshold: 0.60
    min_frequency_bins: 3
    integration_window: 60  # seconds
  
  aisi:
    update_interval: 60  # seconds
    critical_threshold: 0.80
    elevated_threshold: 0.55

storage:
  data_dir: "/data/infrascloud"
  raw_dir: "/data/infrascloud/raw"
  processed_dir: "/data/infrascloud/processed"
  backup_dir: "/data/infrascloud/backup"
  retention_days: 365
  format: "miniseed"

network:
  sync_interval: 3600  # seconds
  cloud_endpoint: "https://api.infrascloud.netlify.app"
  use_4g: true

alerts:
  enabled: true
  check_interval: 300  # seconds
  channels:
    email:
      enabled: true
      recipients: ["operator@infrascloud.org"]
      smtp_server: "smtp.gmail.com"
      smtp_port: 587
    slack:
      enabled: false
      webhook: "https://hooks.slack.com/services/xxx"
    sms:
      enabled: false
```

---

🌐 Multi-Station Network (3-Station Triangle)

Network Architecture

```
                    ┌─────────────────────────────────────┐
                    │         Regional Hub                 │
                    │    (TimescaleDB + Processing)        │
                    └─────────────────────────────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │   Station 1     │     │   Station 2     │     │   Station 3     │
    │   Array A       │     │   Array B       │     │   Array C       │
    │   (4 elements)  │     │   (4 elements)  │     │   (4 elements)  │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
              │                       │                       │
              ▼                       ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │   MB2005 x4     │     │   MB2005 x4     │     │   MB2005 x4     │
    │   Centaur       │     │   Centaur       │     │   Centaur       │
    └─────────────────┘     └─────────────────┘     └─────────────────┘
```

Station Spacing Requirements

Configuration Inter-station Distance Source Localization Accuracy
Minimum Triangle 50-100 km ±50 km at 500 km range
Regional Network 100-500 km ±20 km at 1,000 km range
Continental 500-2,000 km ±100 km at 5,000 km range
Global (IMS) 2,000+ km ±150 km at 10,000 km range

Hub Configuration

```yaml
# config/hub.yaml
hub:
  id: "EUROPE_HUB_01"
  region: "europe"
  endpoints:
    api: "https://api.infrascloud.net"
    websocket: "wss://ws.infrascloud.net"

database:
  type: "timescaledb"
  host: "timescaledb.infrascloud.net"
  port: 5432
  name: "infrascloud"
  user: "infrauser"
  password: "${DB_PASSWORD}"
  pool_size: 50
  
  timescale:
    chunk_interval: "7 days"
    retention_period: "10 years"
    compression: true

stations:
  - id: "IS42_AZORES"
    latitude: 38.5
    longitude: -28.5
    sync_interval: 300
    priority: 1
    
  - id: "IS26_GERMANY"
    latitude: 48.5
    longitude: 9.5
    sync_interval: 300
    priority: 1
    
  - id: "IS48_TUNISIA"
    latitude: 36.5
    longitude: 10.5
    sync_interval: 300
    priority: 1

beamforming:
  enabled: true
  network_type: "triangle"
  min_stations: 3
  processing_interval: 300  # seconds
  
  source_localization:
    method: "grid_search"
    grid_resolution: 0.5  # degrees
    max_range: 6000  # km
    min_intersection_angle: 30  # degrees

alerts:
  lsi_critical: 0.80
  lsi_elevated: 0.55
  tornado_precursor: true
  cyclone_intensification: true
```

---

☁️ Cloud Deployment

AWS CloudFormation Template

```yaml
# cloudformation/infrascloud.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'INFRAS-CLOUD Cloud Infrastructure'

Parameters:
  EnvironmentName:
    Type: String
    Default: production
    AllowedValues: [development, staging, production]
  
  DBPassword:
    Type: String
    NoEcho: true

Resources:
  # VPC
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsSupport: true
      EnableDnsHostnames: true
      Tags:
        - Key: Name
          Value: !Sub ${EnvironmentName}-vpc

  # RDS TimescaleDB
  TimescaleDB:
    Type: AWS::RDS::DBInstance
    Properties:
      Engine: postgres
      EngineVersion: '15.3'
      DBInstanceClass: db.r5.2xlarge
      AllocatedStorage: 1000
      StorageEncrypted: true
      DBName: infrascloud
      MasterUsername: infraadmin
      MasterUserPassword: !Ref DBPassword
      BackupRetentionPeriod: 30
      MultiAZ: true
      EnableCloudwatchLogsExports: ['postgresql']

  # ECS Cluster for Processing
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub ${EnvironmentName}-cluster
      ClusterSettings:
        - Name: containerInsights
          Value: enabled

  # S3 Bucket for Raw Data
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub infrascloud-${EnvironmentName}-${AWS::AccountId}
      LifecycleConfiguration:
        Rules:
          - Id: ArchiveOldData
            Status: Enabled
            Transitions:
              - TransitionInDays: 90
                StorageClass: GLACIER
            ExpirationInDays: 3650

  # CloudWatch Alarms
  LSICriticalAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub ${EnvironmentName}-aisi-critical
      ComparisonOperator: GreaterThanThreshold
      EvaluationPeriods: 2
      MetricName: AISI
      Namespace: INFRAS-CLOUD
      Period: 3600
      Statistic: Maximum
      Threshold: 0.80
      AlarmActions: [!Ref AlertTopic]

  # SNS Topic for Alerts
  AlertTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub ${EnvironmentName}-aisi-alerts
```

Deployment Script

```bash
#!/bin/bash
# deploy_aws.sh

echo "Deploying INFRAS-CLOUD to AWS..."

ENVIRONMENT=${1:-production}
STACK_NAME="infrascloud-${ENVIRONMENT}"
REGION="us-west-2"

# Generate random password
DB_PASSWORD=$(openssl rand -base64 32)

# Deploy CloudFormation
aws cloudformation deploy \
  --template-file cloudformation/infrascloud.yaml \
  --stack-name ${STACK_NAME} \
  --region ${REGION} \
  --parameter-overrides \
    EnvironmentName=${ENVIRONMENT} \
    DBPassword=${DB_PASSWORD} \
  --capabilities CAPABILITY_IAM

echo "Deployment complete!"
echo "DB Password: ${DB_PASSWORD} (save this securely)"
```

---

📡 Edge Computing Deployment

Raspberry Pi Field Station

```bash
#!/bin/bash
# setup_edge_station.sh

echo "⚡ Setting up INFRAS-CLOUD Edge Station on Raspberry Pi"

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv git \
  libatlas-base-dev libhdf5-dev

# Configure USB permissions for MB2005
cat << EOF | sudo tee /etc/udev/rules.d/99-infrascloud.rules
# MB2005 Microbarometer
SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", SYMLINK+="mb2005", MODE="0666"
# Paros 2200A
SUBSYSTEM=="tty", ATTRS{idVendor}=="067b", ATTRS{idProduct}=="2303", SYMLINK+="paros", MODE="0666"
