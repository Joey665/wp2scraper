# 🚀 WordPress Vulnerability Scanner & Lead Generation System

A fully automated system that discovers vulnerable WordPress business websites, analyzes security risks using AI, and generates qualified leads for cybersecurity services.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Workflow Automation (n8n)](#workflow-automation-n8n)
- [API Keys Required](#api-keys-required)
- [Project Structure](#project-structure)
- [Making Money with This System](#making-money-with-this-system)
- [Troubleshooting](#troubleshooting)
- [Security & Legal](#security--legal)
- [Roadmap](#roadmap)
- [License](#license)

---

## 📖 Overview

This system combines **AI-powered search**, **vulnerability scanning**, and **workflow automation** to:

1. **Discover** WordPress business websites using Serper API (Google Search)
2. **Analyze** security vulnerabilities using Exa.ai AI-powered search
3. **Qualify** leads based on risk scores
4. **Automate** outreach via n8n workflows
5. **Generate** reports for client consultations

The system targets **real businesses** (law firms, medical practices, e-commerce stores, etc.) - not WordPress.org, YouTube, or Wikipedia.

---

## ✨ Features

### 🔍 Discovery
- Serper API integration (2,500 free searches/month)
- Business-only filtering (blocks WordPress.org, YouTube, etc.)
- Industry-specific targeting (legal, medical, finance, real estate, e-commerce)
- Duplicate URL removal

### 🛡️ Vulnerability Analysis
- WordPress detection (checks `/wp-content/`, `/wp-includes/`, `wp-json`)
- Exa.ai AI-powered vulnerability scanning ($130 free credits)
- Risk scoring (0-100)
- CVE detection
- Vulnerability type identification

### 🤖 Automation
- **n8n** workflow integration
- Scheduled scanning (every 6 hours)
- Automated lead qualification
- Email outreach generation
- CSV report generation

### 📊 Output
- JSON results (`scan_results.json`)
- CSV leads (`leads/leads.csv`)
- High-risk lead prioritization
- Vulnerability summaries

---

## 🏗️ Architecture


┌─────────────────────────────────────────────────────────────┐
│                     Azure VM (B2als_v2)                    │
│                         4GB RAM                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                 Docker Container                     │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │                   n8n                         │  │   │
│  │  │  Schedule → Search → Analyze → Filter → Email │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                 Python Scanner                       │   │
│  │  ┌────────────────────────────────────────────────┐  │   │
│  │  │  Serper API → WordPress Check → Exa.ai → CSV  │  │   │
│  │  └────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    ngrok Tunnel                      │   │
│  │         HTTPS → https://your-url.ngrok.io           │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

---

## 📦 Prerequisites

### Hardware Requirements
- **VM:**  (2 vCPUs, 4GB RAM) or equivalent
- **Storage:** 30GB SSD
- **Network:** Outbound internet access

### Software Requirements
- Ubuntu 20.04+ / 22.04 LTS
- Docker & Docker Compose
- Python 3.8+
- Node.js 18+

### API Keys Required
| Service | Purpose | Free Tier |
|---------|---------|-----------|
| [Serper](https://serper.dev) | Google Search API | 2,500 searches/month |
| [Exa.ai](https://exa.ai) | AI-powered search | $130 credits |
| [ngrok](https://ngrok.com) | Secure tunnel | Free (1 tunnel) |

---

## 🚀 Quick Start


# Clone or create the project
mkdir ~/wordpress-scanner && cd ~/wordpress-scanner

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 pandas

# Set up API keys
export SERPER_API_KEY="your_serper_key"
export EXA_API_KEY="your_exa_key"

# Run the scanner
python3 business_scanner.py

# Check results
cat leads/leads.csv


## 📥 Installation

### 1. Clone/Download the Project


mkdir -p ~/wordpress-scanner
cd ~/wordpress-scanner


### 2. Create Virtual Environment


python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 pandas python-dotenv


### 3. Install Docker & n8n


# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Run n8n
docker run -d \
  --name n8n \
  --restart unless-stopped \
  --memory="1.5g" \
  --cpus="1" \
  -p 5678:5678 
  -e N8N_BASIC_AUTH_ACTIVE=true \

  -v n8n_data:/home/node/.n8n \

  n8nio/n8n


### 4. Install ngrok (for remote access)


cd /tmp
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
sudo mv ngrok /usr/local/bin/
ngrok config add-authtoken YOUR_NGROK_TOKEN
nohup ngrok http 5678 &

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file:


# ~/wordpress-scanner/.env
SERPER_API_KEY=your_serper_key_here
EXA_API_KEY=your_exa_key_here
WPSCAN_API_TOKEN=your_wpscan_token_here  # Optional


### API Keys Setup

#### Serper (Required)
1. Go to [serper.dev](https://serper.dev)
2. Sign up (free tier: 2,500 searches/month)
3. Copy your API key

#### Exa.ai (Recommended)
1. Go to [exa.ai](https://exa.ai)
2. Sign up (get $130 free credits)
3. Copy your API key

#### ngrok (For Remote Access)
1. Go to [ngrok.com](https://ngrok.com)
2. Sign up for free account
3. Copy your auth token

---

## 🎯 Usage

### Run the Scanner

```bash
cd ~/wordpress-scanner
source venv/bin/activate

# Business-only scanner (recommended)
python3 business_scanner.py

# Or the original scanner
python3 scanner.py

# Targeted industry scanner
python3 targeted_scanner.py
```

### Check Results


# View CSV leads
cat leads/leads.csv

# View JSON results
cat scan_results.json | python3 -m json.tool

# Count high-risk sites
cat scan_results.json | python3 -c "
import sys, json
sites = json.load(sys.stdin)
high = [s for s in sites if s.get('risk_score', 0) > 60]
print(f'High risk sites: {len(high)}')
"

# View high-risk URLs only
cat scan_results.json | python3 -c "
import sys, json
sites = json.load(sys.stdin)
for s in sites:
    if s.get('risk_score', 0) > 60:
        print(f\"{s['url']} - Risk: {s['risk_score']}/100\")
"
```

### Access n8n Dashboard


# Get ngrok URL
curl -s http://127.0.0.1:4040/api/tunnels | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['tunnels'][0]['public_url'])"

# Open in browser: https://your-url.ngrok.io
`

---

## 🔄 Workflow Automation (n8n)

### Import Workflow

1. Open n8n dashboard (ngrok URL)
2. Login: `admin` / `securepass456`
3. Click **"Import from File"**
4. Upload `complete_workflow.json`
5. Add your API keys in the nodes
6. Click **"Save"** and **"Activate"**

### Workflow Nodes

| Node | Purpose |
|------|---------|
| Schedule Trigger | Runs every 6 hours |
| Serper Search API | Finds WordPress sites |
| Parse WordPress Sites | Filters results |
| Exa.ai Vulnerability Scan | AI-powered analysis |
| Generate Vulnerability Reports | Creates risk scores |
| Filter High Severity Only | Keeps best leads |
| Save to CSV | Stores results |
| Email Alert | Sends notifications |

---

## 🗂️ Project Structure


wordpress-scanner/
├── scanner.py                 # Main scanner
├── business_scanner.py        # Business-only scanner
├── targeted_scanner.py        # Industry-targeted scanner
├── complete_workflow.json     # n8n workflow
├── leads/                     # Lead storage
│   └── leads.csv              # Generated leads
├── reports/                   # Report storage
├── venv/                      # Python virtual environment
├── .env                       # API keys
└── README.md                  # This file


---

## 💰 Making Money with This System

### Business Model

| Service | Price | Description |
|---------|-------|-------------|
| **Security Audit** | $97-$247 | One-time vulnerability report |
| **Security Fix** | $497-$997 | Fix all vulnerabilities |
| **Monthly Retainer** | $197/mo | Ongoing security monitoring |

### Lead Qualification

| Score | Action |
|-------|--------|
| 70-100 | 🔴 High Priority - Email immediately |
| 50-69 | 🟡 Medium Priority - Follow up |
| 30-49 | 🟢 Low Priority - Batch email |
| 0-29 | ⚪ Minimal - Skip |

---

## 🔧 Troubleshooting

### Scanner Not Finding Sites


Check API key
curl -X POST https://google.serper.dev/search \
  -H 'X-API-KEY: YOUR_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"q": "WordPress", "num": 5}'

 Log in to serper.dev/dashboard


### n8n Not Accessible


# Check container
docker ps | grep n8n

# Check logs
docker logs n8n

# Restart
docker restart n8n

# Check ngrok
curl http://127.0.0.1:4040/api/tunnels
```

### Permission Errors

```bash
# Fix Docker permissions
sudo usermod -aG docker $USER
newgrp docker

# Fix file permissions
chmod +x *.py
mkdir -p leads reports
```

### Low Memory

```bash
# Check memory
free -h

# Create swap if needed
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 🛡️ Security & Legal

### Important: Use Responsibly

✅ **DO:**
- Scan sites you own or have permission to test
- Report vulnerabilities responsibly
- Get written consent before scanning
- Follow ethical hacking guidelines

❌ **DON'T:**
- Exploit vulnerabilities you find
- Sell vulnerability data to third parties
- Scan without permission
- Use for malicious purposes

### Legal Disclaimer

This software is for educational and legitimate security testing purposes only. Users are responsible for ensuring they have proper authorization to scan any websites. The authors assume no liability for misuse.

---

## 🗺️ Roadmap

- [x] Basic WordPress detection
- [x] Serper API integration
- [x] Exa.ai vulnerability analysis
- [x] Business-only filtering
- [x] n8n workflow automation
- [x] Lead generation CSV
- [ ] Automated email outreach
- [ ] Vulnerability database integration
- [ ] Client dashboard
- [ ] Automated report generation (PDF)
- [ ] Multi-language support
- [ ] WordPress plugin vulnerability database

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request


---

## ⭐ Support

- Star this repo if you find it useful
- Report issues on GitHub
- Follow for updates

---

## 📞 Contact

**Joseph Bright**
- Cybersecurity Specialist
- WordPress Security Expert

---

## 🙏 Acknowledgments

- [Serper](https://serper.dev) - Google Search API
- [Exa.ai](https://exa.ai) - AI-powered search
- [n8n](https://n8n.io) - Workflow automation
- [ngrok](https://ngrok.com) - Secure tunneling

---

**Built with ❤️ for the cybersecurity community**

---

## Quick Reference Card

```bash
# Start everything
./start_all.sh

# Run scanner
cd ~/wordpress-scanner && python3 business_scanner.py

# Check leads
cat ~/wordpress-scanner/leads/leads.csv

# Access n8n
# Open: https://your-ngrok-url.ngrok.io


# View logs
docker logs n8n

# Stop everything
docker stop n8n
pkill ngrok
```

---

**Happy Scanning!** 🚀🔒
