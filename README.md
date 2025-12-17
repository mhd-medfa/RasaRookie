# 💰 Al-Mdfaa Financial Services Chatbot

A bilingual (Arabic/English) AI-powered customer service chatbot for financial services, built with Rasa and featuring a modern ChatGPT-like interface.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8-green.svg)
![Rasa](https://img.shields.io/badge/rasa-3.2.2-purple.svg)

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Running the Chatbot](#running-the-chatbot)
- [Training the Model](#training-the-model)
- [Testing](#testing)
- [User Interfaces](#user-interfaces)
- [Troubleshooting](#troubleshooting)
- [Customization](#customization)
- [License](#license)

---

## ✨ Features

### 🤖 Chatbot Capabilities
- **Bilingual Support**: Seamless Arabic and English conversation
- **Intelligent Intent Detection**: 13+ pre-trained intents for financial services
- **Auto Language Detection**: Automatically responds in user's language
- **Entity Extraction**: Recognizes currencies, amounts, branch names, and countries
- **Financial Services**: Transfer status, branch locations, fees, exchange rates, and more

### 🎨 User Interfaces
- **Terminal Interface**: Simple command-line interaction
- **Streamlit Web App**: Modern, responsive web interface
- **Standalone HTML**: Beautiful ChatGPT-like interface that works offline
- **RTL Support**: Proper right-to-left rendering for Arabic text

### 🏗️ Technical Features
- Custom action server with language detection
- Rule-based and ML-powered conversation management
- Fallback handling for unknown queries
- Session management and conversation history
- RESTful API endpoints

---

## 🏛️ Architecture

```
┌─────────────────┐
│  User Interface │  (Terminal / Streamlit / HTML)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Rasa Server   │  (NLU + Dialogue Management)
│   Port: 5005    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Action Server  │  (Custom Actions + Language Detection)
│   Port: 5055    │
└─────────────────┘
```

**Technology Stack:**
- **Rasa 3.2.2**: Open-source conversational AI framework
- **Python 3.8**: Core programming language (3.8 required, 3.10+ not supported)
- **Streamlit**: Web UI framework
- **TensorFlow 2.7.4**: Machine learning backend
- **DIETClassifier**: Intent classification and entity recognition

---

## 📦 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ / Debian 10+ / Linux Mint 20+
- **Python**: 3.8 (Rasa 3.2.2 doesn't support 3.10+)
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 2GB free space

### Required Tools
```bash
sudo apt-get update
sudo apt-get install -y python3.8 python3-pip python3-venv virtualenv git
```

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/mhd-medfa/RasaRookie.git
cd RasaRookie
git checkout develop
```

### Step 2: Create Virtual Environment

```bash
virtualenv venv
source venv/bin/activate
```

> **Note for Fish shell users**: Use `source venv/bin/activate.fish` instead.

### Step 3: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 4: Install Rasa

```bash
pip install rasa==3.2.2 --use-deprecated=legacy-resolver
```

This will take a few minutes and show some dependency warnings — these are expected.

### Step 5: Fix Dependency Conflicts

After the main installation, fix the known conflicts:

```bash
# Fix websockets version (required for Sanic compatibility)
pip install websockets==10.4

# Fix numpy version (required for training)
pip install numpy==1.21.6

# Fix protobuf version
pip install protobuf==3.20.3
```

### Step 6: Install Streamlit (Optional - for web interface)

If you want to use the Streamlit web interface, install it in a separate environment to avoid conflicts:

```bash
# For the web interface, you can either:
# Option A: Use the standalone HTML file (recommended, no extra install needed)
# Option B: Install Streamlit and accept the dependency warnings
pip install streamlit requests
```

### Step 7: Set Environment Variables

```bash
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONWARNINGS="ignore"
```

To make these permanent, add them to your `~/.bashrc`:

```bash
echo 'export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python' >> ~/.bashrc
echo 'export PYTHONWARNINGS="ignore"' >> ~/.bashrc
source ~/.bashrc
```

---

## 📁 Project Structure

```
RasaRookie/
├── actions/
│   ├── __init__.py              # Makes actions a Python package
│   └── actions.py               # Custom actions with language detection
├── data/
│   ├── nlu.yml                  # Training data for intent classification
│   ├── rules.yml                # Conversation rules
│   └── stories.yml              # Conversation stories
├── models/                      # Trained models (auto-generated)
├── config.yml                   # Rasa NLU and Core configuration
├── domain.yml                   # Bot's domain (intents, entities, responses)
├── endpoints.yml                # Action server and other endpoints
├── credentials.yml              # Channel credentials (optional)
├── app.py                       # Streamlit web interface
├── chatbot.html                 # Standalone HTML interface
└── README.md                    # This file
```

---

## 🎓 Training the Model

Before running the chatbot for the first time, you need to train the model:

```bash
cd RasaRookie
source venv/bin/activate
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONWARNINGS="ignore"

rasa train
```

**Training time:** 2-5 minutes depending on hardware.

You'll see some deprecation warnings — these are normal and don't affect functionality.

---

## 🏃 Running the Chatbot

### Method 1: Terminal Interface (Simplest)

**Terminal 1 - Start Action Server:**
```bash
cd RasaRookie
source venv/bin/activate
rasa run actions
```

**Terminal 2 - Start Chat:**
```bash
cd RasaRookie
source venv/bin/activate
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
rasa shell
```

Test it:
```
Your input -> مرحبا
Your input -> أين الفروع؟
Your input -> hello
Your input -> what are your fees?
```
---

### Method 2: Streamlit Web Interface

**Terminal 1 - Start Action Server:**
```bash
cd RasaRookie
source venv/bin/activate
rasa run actions
```

**Terminal 2 - Start Rasa API Server:**
```bash
cd RasaRookie
source venv/bin/activate
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
rasa run --enable-api --cors "*"
```

**Terminal 3 - Start Streamlit:**
```bash
cd RasaRookie
source venv/bin/activate
streamlit run app.py --server.port 8501
```

**Access:** Open browser to `http://localhost:8501`

---

## 🧪 Testing

### Test NLU Only

```bash
rasa shell nlu
```

Example:
```
Your input -> مرحبا
{
  "intent": {"name": "greet", "confidence": 0.98},
  "entities": [],
  "text": "مرحبا"
}
```

### Validate Configuration

```bash
rasa data validate
```

---

## 🔧 Troubleshooting

### Issue: `cannot import name 'CLOSED' from 'websockets.connection'`

**Solution:**
```bash
pip install websockets==10.4
```

---

### Issue: `ValueError: setting an array element with a sequence` during training

**Solution:**
```bash
pip install numpy==1.21.6
```

---

### Issue: `TypeError: Descriptors cannot be created directly`

**Solution:**
```bash
pip install protobuf==3.20.3
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
```

---

## 🎨 Customization

### Adding New Intents

1. Add training examples in `data/nlu.yml`:
```yaml
- intent: refund_request
  examples: |
    - I want a refund
    - ابي استرجع فلوسي
    - refund my money
```

2. Add intent to `domain.yml`:
```yaml
intents:
  - refund_request
```

3. Add responses in `domain.yml`:
```yaml
responses:
  utter_refund_en:
    - text: "To request a refund, please contact support..."
  utter_refund_ar:
    - text: "لطلب استرجاع، يرجى التواصل مع الدعم..."
```

4. Add rule in `data/rules.yml`:
```yaml
- rule: Handle refund request
  steps:
    - intent: refund_request
    - action: action_respond_with_language
```

5. Update `actions/actions.py`:
```python
INTENT_RESPONSES = {
    # ... existing intents ...
    'refund_request': 'utter_refund',
}
```

6. Retrain:
```bash
rasa train
```

---

## 📝 Supported Intents

| Intent | Arabic Examples | English Examples |
|--------|-----------------|------------------|
| `greet` | مرحبا، السلام عليكم | hello, hi |
| `goodbye` | مع السلامة، باي | goodbye, bye |
| `transfer_status` | وين صارت الحوالة | where is my transfer |
| `branch_locations` | وين الفروع | where are your branches |
| `working_hours` | شو ساعات العمل | what are your hours |
| `fees_inquiry` | كم العمولة | what are your fees |
| `exchange_rates` | سعر الصرف | exchange rate |
| `how_to_send` | كيف ارسل حوالة | how to send money |
| `how_to_receive` | كيف استلم حوالة | how to receive money |
| `required_documents` | شو الاوراق | what documents needed |
| `complaint` | عندي شكوى | I have a complaint |
| `speak_to_human` | بدي احكي مع موظف | speak to agent |
| `services_list` | شو خدماتكم | what services |

---

## 📄 License

This project is licensed under the MIT License.
