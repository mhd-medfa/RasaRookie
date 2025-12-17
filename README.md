# 💰 Al-Mdfaa Financial Services Chatbot

A bilingual (Arabic/English) AI-powered customer service chatbot for financial services, built with Rasa and featuring a modern ChatGPT-like interface.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Rasa](https://img.shields.io/badge/rasa-3.2.2-purple.svg)

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running the Chatbot](#running-the-chatbot)
- [Training the Model](#training-the-model)
- [Testing](#testing)
- [User Interfaces](#user-interfaces)
- [Troubleshooting](#troubleshooting)
- [Customization](#customization)
- [Contributing](#contributing)
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
- **Python 3.8+**: Core programming language
- **Streamlit**: Web UI framework
- **TensorFlow 2.7.3**: Machine learning backend
- **DIETClassifier**: Intent classification and entity recognition
- **Custom Actions**: Language detection and dynamic responses

---

## 📦 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ / Debian 10+ / Linux Mint 20+
- **Python**: 3.8 or 3.9 (Rasa 3.2.2 doesn't support 3.10+)
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 2GB free space

### Required Tools
```bash
sudo apt-get update
sudo apt-get install -y python3.8 python3-pip python3-venv git
```

---

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
# Create project directory
mkdir -p ~/almdfaa-chatbot
cd ~/almdfaa-chatbot

# If you have the project files, extract them here
# Otherwise, create the directory structure as shown in "Project Structure" section
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3.8 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install Dependencies

```bash
# Install Rasa and dependencies
pip install rasa==3.2.2 --use-deprecated=legacy-resolver

# Install Rasa SDK (for custom actions)
pip install rasa-sdk==3.2.0

# Install Streamlit (for web interface)
pip install streamlit==1.28.0

# Fix protobuf version conflict
pip install protobuf==3.20.3

# Install additional dependencies
pip install requests
```

### Step 4: Set Environment Variables

```bash
# Add to ~/.bashrc or run before starting Rasa
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export PYTHONWARNINGS="ignore"

# Apply changes
source ~/.bashrc
```

---

## 📁 Project Structure

```
rasa-project/
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
├── streamlit_chat.py           # Streamlit web interface
├── rasa_chatbot.html           # Standalone HTML interface
└── README.md                    # This file
```

### Create Required Files

#### 1. Create `actions/__init__.py`
```bash
mkdir -p actions
touch actions/__init__.py
```

#### 2. Create `actions/actions.py`
See the provided `actions.py` file in the project.

#### 3. Create `data/nlu.yml`
See the provided `nlu.yml` file in the project.

#### 4. Create `data/rules.yml`
See the provided `rules.yml` file in the project.

#### 5. Create `data/stories.yml`
See the provided `stories.yml` file in the project.

#### 6. Create `config.yml`
See the provided `config.yml` file in the project.

#### 7. Create `domain.yml`
See the provided `domain.yml` file in the project.

#### 8. Create `endpoints.yml`
```yaml
action_endpoint:
  url: "http://localhost:5055/webhook"
```

---

## ⚙️ Configuration

### NLU Pipeline (config.yml)

The chatbot uses the following NLU pipeline optimized for Arabic and English:

```yaml
pipeline:
  - name: WhitespaceTokenizer          # Tokenization
  - name: RegexFeaturizer              # Pattern matching
  - name: LexicalSyntacticFeaturizer   # Lexical features
  - name: CountVectorsFeaturizer       # Character n-grams (1-4)
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - name: CountVectorsFeaturizer       # Word n-grams (1-2)
    analyzer: word
    min_ngram: 1
    max_ngram: 2
  - name: DIETClassifier               # Intent + Entity classification
    epochs: 100
  - name: EntitySynonymMapper          # Entity normalization
  - name: FallbackClassifier           # Fallback handling
    threshold: 0.4
```

### Policies (config.yml)

```yaml
policies:
  - name: MemoizationPolicy           # Remember exact conversation patterns
  - name: RulePolicy                  # Handle predefined rules
    core_fallback_threshold: 0.4
  - name: TEDPolicy                   # Transformer-based dialogue
    max_history: 5
    epochs: 50
```

### Supported Intents

| Intent | Description | Examples (AR) | Examples (EN) |
|--------|-------------|---------------|---------------|
| `greet` | Greeting | مرحبا، السلام عليكم | hello, hi |
| `goodbye` | Farewell | مع السلامة، باي | goodbye, bye |
| `transfer_status` | Check transfer | وين صارت الحوالة | where is my transfer |
| `branch_locations` | Find branches | وين الفروع | where are your branches |
| `working_hours` | Business hours | شو ساعات العمل | what are your hours |
| `fees_inquiry` | Ask about fees | كم العمولة | what are your fees |
| `exchange_rates` | Currency rates | سعر الصرف | exchange rate |
| `how_to_send` | Send money | كيف ارسل حوالة | how to send money |
| `how_to_receive` | Receive money | كيف استلم حوالة | how to receive money |
| `required_documents` | Needed docs | شو الاوراق | what documents |
| `complaint` | File complaint | عندي شكوى | I have a complaint |
| `speak_to_human` | Agent transfer | بدي احكي مع موظف | speak to agent |
| `services_list` | List services | شو خدماتكم | what services |

---

## 🏃 Running the Chatbot

### Method 1: Terminal Interface (Simplest)

#### Step 1: Start Action Server
```bash
# Terminal 1
cd ~/almdfaa-chatbot/rasa-project
source venv/bin/activate
rasa run actions
```

#### Step 2: Start Interactive Shell
```bash
# Terminal 2
cd ~/almdfaa-chatbot/rasa-project
source venv/bin/activate
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
rasa shell
```

**Test the chatbot:**
```
Your input -> مرحبا
Your input -> أين الفروع؟
Your input -> hello
Your input -> what are your fees?
```

---

### Method 2: Streamlit Web Interface

#### Step 1: Start Action Server
```bash
# Terminal 1
cd ~/almdfaa-chatbot/rasa-project
source venv/bin/activate
rasa run actions
```

#### Step 2: Start Rasa Server with API
```bash
# Terminal 2
cd ~/almdfaa-chatbot/rasa-project
source venv/bin/activate
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
rasa run --enable-api --cors "*" --port 5005
```

#### Step 3: Start Streamlit
```bash
# Terminal 3
cd ~/almdfaa-chatbot/rasa-project
source venv/bin/activate
streamlit run streamlit_chat.py --server.port 8501
```

**Access:** Open browser to `http://localhost:8501`

---

### Method 3: Standalone HTML Interface (Recommended)

#### Step 1: Start Action Server
```bash
# Terminal 1
cd ~/almdfaa-chatbot/rasa-project
source venv/bin/activate
rasa run actions
```

#### Step 2: Start Rasa Server with API
```bash
# Terminal 2
cd ~/almdfaa-chatbot/rasa-project
source venv/bin/activate
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
rasa run --enable-api --cors "*" --port 5005
```

#### Step 3: Open HTML File
```bash
# Simply double-click rasa_chatbot.html in your file manager
# Or open it with:
xdg-open rasa_chatbot.html
```

**Benefits:**
- ✅ No external dependencies
- ✅ Perfect Arabic rendering
- ✅ Works offline
- ✅ Beautiful ChatGPT-like interface
- ✅ Connection status indicator

---

## 🎓 Training the Model

### Initial Training

```bash
cd ~/almdfaa-chatbot/rasa-project
source venv/bin/activate

# Train the model
rasa train

# This creates a new model in models/ directory
# Example: models/20231217-123456-gentle-tenant.tar.gz
```

**Training time:** 2-5 minutes (depending on hardware)

### Retraining After Changes

After modifying any of these files:
- `data/nlu.yml` (training examples)
- `data/rules.yml` (conversation rules)
- `data/stories.yml` (conversation flows)
- `config.yml` (NLU pipeline or policies)
- `domain.yml` (intents, entities, responses)

Run:
```bash
rasa train --force
```

---

## 🧪 Testing

### Interactive Testing

```bash
# Start interactive learning mode
rasa interactive

# This allows you to:
# - Test conversations
# - Correct bot predictions
# - Generate new training data
```

### Test NLU Only

```bash
# Test intent classification
rasa shell nlu

# Example:
Your input -> مرحبا
{
  "intent": {"name": "greet", "confidence": 0.9876},
  "entities": [],
  "text": "مرحبا"
}
```

### Validate Configuration

```bash
# Check for errors in config files
rasa data validate

# Check for conflicting stories
rasa data validate stories
```

### Evaluate Model Performance

```bash
# Split data and evaluate
rasa test nlu --cross-validation

# Generate confusion matrix
rasa test nlu --nlu data/nlu.yml
```

---

## 🎨 User Interfaces

### 1. Terminal Interface

**Pros:**
- Fastest to start
- No additional dependencies
- Good for testing

**Cons:**
- Limited Arabic rendering
- No visual appeal
- Basic interaction

**Usage:**
```bash
rasa shell
```

---

### 2. Streamlit Web Interface

**Features:**
- Modern, responsive design
- Dark theme with gold accents
- Message bubbles with avatars
- Typing indicators
- Clear chat functionality
- Suggestion chips
- Perfect Arabic RTL support

**Customization:**
Edit `streamlit_chat.py` to modify:
- Colors and theme
- Fonts and typography
- Message styling
- Suggestion chips
- Header content

**Usage:**
```bash
streamlit run streamlit_chat.py
```

---

### 3. Standalone HTML Interface

**Features:**
- No external dependencies
- ChatGPT/Claude-like design
- Connection status indicator
- Smooth animations
- RTL Arabic support
- Glassmorphism effects
- Responsive design

**Customization:**
Edit `rasa_chatbot.html` to modify:
- CSS styles (colors, fonts, layout)
- Suggestion chips
- Welcome message
- Connection check interval

**Usage:**
```bash
# Just open the file in any browser
xdg-open rasa_chatbot.html
```

---

## 🔧 Troubleshooting

### Issue 1: `protobuf` Version Conflict

**Error:**
```
TypeError: Descriptors cannot be created directly.
```

**Solution:**
```bash
pip install protobuf==3.20.3
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
```

---

### Issue 2: Action Server Not Found

**Error:**
```
Failed to execute custom action 'action_respond_with_language' 
because no endpoint is configured
```

**Solution:**
1. Ensure `endpoints.yml` exists with:
   ```yaml
   action_endpoint:
     url: "http://localhost:5055/webhook"
   ```
2. Start action server: `rasa run actions`
3. Restart Rasa shell/server

---

### Issue 3: Arabic Text Not Rendering

**Terminal Solution:**
```bash
# Install Arabic fonts
sudo apt-get install fonts-noto fonts-dejavu

# Use HTML interface instead (recommended)
xdg-open rasa_chatbot.html
```

---

### Issue 4: Port Already in Use

**Error:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**
```bash
# Find and kill process using port 5005
sudo lsof -t -i:5005 | xargs kill -9

# Or use different port
rasa run --enable-api --cors "*" --port 5006
```

---

### Issue 5: NumPy Version Warning

**Warning:**
```
A NumPy version >=1.16.5 and <1.23.0 is required
```

**Solution:**
```bash
pip install numpy==1.19.5
```

---

### Issue 6: Model Not Found

**Error:**
```
No model found
```

**Solution:**
```bash
# Train a new model
rasa train

# Or specify model path
rasa shell --model models/20231217-123456.tar.gz
```

---

### Issue 7: Connection Refused (HTML/Streamlit)

**Error:**
```
Connection refused to http://localhost:5005
```

**Checklist:**
1. ✅ Action server running? (`rasa run actions`)
2. ✅ Rasa API server running? (`rasa run --enable-api`)
3. ✅ Correct port (5005)?
4. ✅ CORS enabled? (`--cors "*"`)

---

## 🎨 Customization

### Adding New Intents

#### 1. Add training examples in `data/nlu.yml`:

```yaml
- intent: refund_request
  examples: |
    - I want a refund
    - ابي استرجع فلوسي
    - refund my money
    - ارجاع المبلغ
```

#### 2. Add to domain in `domain.yml`:

```yaml
intents:
  - refund_request  # Add new intent
```

#### 3. Create response in `domain.yml`:

```yaml
responses:
  utter_refund_en:
    - text: "To request a refund, please contact support..."
  
  utter_refund_ar:
    - text: "لطلب استرجاع، يرجى التواصل مع الدعم..."
```

#### 4. Add rule in `data/rules.yml`:

```yaml
- rule: Handle refund request
  steps:
    - intent: refund_request
    - action: action_respond_with_language
```

#### 5. Update action mapping in `actions/actions.py`:

```python
INTENT_RESPONSES = {
    # ... existing intents ...
    'refund_request': 'utter_refund',
}
```

#### 6. Retrain:

```bash
rasa train --force
```

---

### Modifying Responses

Edit `domain.yml`:

```yaml
responses:
  utter_greet_en:
    - text: "Welcome to Al-Mdfaa! 😊"
    - text: "Hello! How may I assist you today?"
  
  utter_greet_ar:
    - text: "أهلاً وسهلاً في المدفع! 😊"
    - text: "مرحباً! كيف أقدر أساعدك؟"
```

Multiple responses = random selection for variety.

---

### Changing Branch Information

In `domain.yml`, update:

```yaml
utter_branch_locations_ar:
  - text: |
      فروع المدفع:
      
      📍 دبي - شارع الشيخ زايد
      📍 أبوظبي - الكورنيش
      📍 الشارقة - المجاز
      
      جميع الفروع تعمل من 9 صباحاً - 6 مساءً
```

---

### Customizing the HTML Interface

Edit `rasa_chatbot.html`:

```css
/* Change colors */
body {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.message.user .message-content {
    background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
}

/* Change fonts */
body {
    font-family: 'Tajawal', 'Roboto', sans-serif;
}

/* Modify suggestion chips */
.chip {
    background: rgba(255, 100, 100, 0.2);
    border-color: #FF6B6B;
}
```

---

### Adding Entity Extraction

#### 1. Define entity in `domain.yml`:

```yaml
entities:
  - phone_number
```

#### 2. Add training examples in `data/nlu.yml`:

```yaml
- intent: contact_info
  examples: |
    - my number is [0501234567](phone_number)
    - call me at [+971501234567](phone_number)
```

#### 3. Use in custom action:

```python
def run(self, dispatcher, tracker, domain):
    phone = tracker.get_slot("phone_number")
    if phone:
        dispatcher.utter_message(text=f"Got your number: {phone}")
```

---

## 📚 Additional Resources

### Official Documentation
- [Rasa Documentation](https://rasa.com/docs/)
- [Rasa Community Forum](https://forum.rasa.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

### Tutorials
- [Building Conversational AI with Rasa](https://rasa.com/docs/rasa/playground/)
- [Arabic NLP Best Practices](https://github.com/topics/arabic-nlp)
- [Chatbot Design Principles](https://www.nngroup.com/articles/chatbot-design/)

### Tools
- [Rasa X](https://rasa.com/rasa-x/): Conversation-driven development tool
- [Rasa Playground](https://rasa.com/docs/rasa/playground/): Quick prototyping
- [Botfront](https://botfront.io/): Open-source Rasa UI

---
