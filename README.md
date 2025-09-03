# 🌍 TransCultura

**Autonomous Content Translation, Localization & Compliance for Global Digital Marketing**

TransCultura is an AI-powered platform that automates the entire content adaptation pipeline for global marketing campaigns. It uses a 4-agent system to handle translation, cultural adaptation, compliance checking, and exception management.

## 🚀 Features

- **🔤 Content Translation Agent**: Contextually-aware translation using Llama3.2
- **🎨 Cultural Adaptation Agent**: Adapts content for local cultural contexts
- **⚖️ Compliance & Regulatory Agent**: Ensures regional legal compliance
- **🚩 Exception Management Agent**: Smart flagging for human review

## 🛠️ Tech Stack

- **AI Model**: Llama3.2:3b via Ollama
- **Frontend**: Streamlit
- **Vector DB**: ChromaDB (RAG implementation)
- **Language**: Python 3.12+

## 📦 Installation

### Prerequisites
- Python 3.12+
- [Ollama](https://ollama.ai) installed and running
- Llama3.2:3b model pulled

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/himanshu-phulara/transCultura.git
   cd transCultura
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv transcultura_env
   source transcultura_env/bin/activate  # macOS/Linux
   # or
   transcultura_env\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Ollama and pull model**
   ```bash
   # In separate terminal
   ollama serve
   
   # Pull the model
   ollama pull llama3.2:3b
   ```

5. **Initialize knowledge base (optional)**
   ```bash
   python data_init.py
   ```

6. **Run the application**
   ```bash
   streamlit run transcultura_demo.py
   ```

## 🎯 Usage

1. Open http://localhost:8501 in your browser
2. Select a sample campaign or enter custom content
3. Choose target language, region, and industry
4. Click "🚀 Process Campaign" to see all agents in action
5. Review results in the tabbed interface
6. Check automation metrics and campaign history

## 📊 Supported Markets

### Languages
- Spanish, French, German, Japanese, Portuguese, Hindi

### Regions
- Spain, France, Germany, Japan, Brazil, India

### Industries
- Technology, Healthcare, Fashion, Food & Beverage, Finance

## 🎪 Demo Scenarios

The demo includes sample campaigns for:
- Technology product launches
- Health supplement marketing
- Fashion sales campaigns
- Food delivery promotions

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Content Input   │───▶│ Translation      │───▶│ Cultural        │
│                 │    │ Agent            │    │ Adaptation      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐             │
│ Human Review    │◄───│ Exception        │◄────────────┘
│ (if flagged)    │    │ Management       │
└─────────────────┘    └──────────────────┘
                                ▲
                       ┌──────────────────┐
                       │ Compliance &     │
                       │ Regulatory       │
                       └──────────────────┘
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Hackathon Project

Built for Gen AI Hackathon - demonstrating autonomous AI agents for global marketing automation.

## 📞 Contact

Himanshu Phulara - [@himanshu-phulara](https://github.com/himanshu-phulara)

Project Link: [https://github.com/himanshu-phulara/transCultura](https://github.com/himanshu-phulara/transCultura)