# CivicMindAI - Setup and Deployment Guide

## 🚀 Quick Start

1. **Clone or Download the Project**
   ```bash
   # Extract the CivicMindAI folder to your desired location
   cd CivicMindAI
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables (Optional)**
   ```bash
   # For OpenAI integration (optional - app works without it)
   export OPENAI_API_KEY="your-openai-api-key-here"
   ```

4. **Run the Application**
   ```bash
   streamlit run main.py
   ```

5. **Open in Browser**
   - Navigate to `http://localhost:8501`
   - Start chatting with CivicMindAI!

## 🧩 System Architecture

```
CivicMindAI/
├── main.py                 # Streamlit UI - Main application interface
├── agent_controller.py     # Central routing logic for AI modules
├── rag_module.py           # Retrieval-Augmented Generation
├── kag_module.py           # Knowledge-Augmented Generation  
├── cag_module.py           # Cache-Augmented Generation
├── slm_module.py           # Small Language Model Interface
├── data/
│   ├── civic_docs/         # Sample Chennai civic documents
│   ├── civic_knowledge.json # Structured knowledge graph data
│   ├── civic_cache.json    # Cached frequently-asked information
└── requirements.txt        # Python dependencies
```

## 🤖 AI Modules Overview

### 1. CAG (Cache-Augmented Generation)
- **Purpose**: Instant responses for static information
- **Triggers**: "helpline", "contact", "emergency", "office hours"
- **Example**: "Fire emergency number" → "🚨 Fire Emergency: 101"

### 2. RAG (Retrieval-Augmented Generation)  
- **Purpose**: Search documents and web sources for latest info
- **Triggers**: "latest", "schedule", "rules", "2025", "current"
- **Example**: "Latest garbage collection schedule" → Searches civic documents

### 3. KAG (Knowledge-Augmented Generation)
- **Purpose**: Step-by-step procedures and multi-hop reasoning
- **Triggers**: "how to", "procedure", "steps", "apply", "repair"
- **Example**: "How to apply for birth certificate?" → Step-by-step guide

### 4. SLM (Small Language Model)
- **Purpose**: General conversation and fallback responses
- **Triggers**: "hello", "who are you", "thank you", "help"
- **Example**: "Hello" → Welcome message and capabilities

## 🔧 Configuration Options

### OpenAI Integration
- Set `OPENAI_API_KEY` environment variable for advanced SLM responses
- Without API key: Uses predefined fallback responses
- Supported models: gpt-3.5-turbo, gpt-4, etc.

### Data Customization
- **Add Documents**: Place `.txt` files in `data/civic_docs/`
- **Update Cache**: Modify `data/civic_cache.json` for new contacts
- **Extend Knowledge**: Edit `data/civic_knowledge.json` for procedures

### Module Configuration
- Each module can be disabled if initialization fails
- Fallback mechanisms ensure app continues working
- Logging available for debugging

## 📊 Usage Examples

### Emergency Contacts
```
User: "Fire emergency number"
Response: 🚨 Fire Emergency
📞 Contact: 101
⏰ Availability: 24x7
[Module: CAG]
```

### Procedures  
```
User: "How to pay property tax online?"
Response: 🧠 Knowledge Graph Analysis:
🔗 Step-by-step Reasoning:
1. Identify Service: Property Tax Payment
2. Find Department: Greater Chennai Corporation (GCC)
3. Get Procedure: Online payment procedure available
[Module: KAG]
```

### Latest Information
```
User: "Latest water supply schedule"
Response: 🔍 Latest Information Found (3 sources):
📄 From Official Documents:
• Water Supply Guidelines: Morning: 6:00 AM to 8:00 AM...
[Module: RAG]
```

## 🛠️ Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```
   Warning: Could not import module
   Solution: Check requirements.txt installation
   ```

2. **OpenAI API Errors**
   ```
   Warning: OpenAI client setup failed
   Solution: Check API key or use without OpenAI
   ```

3. **Document Loading Issues**
   ```
   Warning: Documents directory not found
   Solution: Ensure data/civic_docs/ exists with .txt files
   ```

4. **Port Already in Use**
   ```bash
   streamlit run main.py --server.port 8502
   ```

### Performance Optimization

- **Vector Search**: Uses FAISS for efficient document retrieval
- **Caching**: Streamlit session state for conversation history
- **Lazy Loading**: Modules initialized only when first used
- **Error Handling**: Graceful fallbacks prevent crashes

## 🧪 Testing the System

### Test Queries by Module

**CAG (Cache) Tests:**
- "Chennai Corporation helpline"
- "Police emergency number"  
- "Water tax contact"
- "Office hours"

**RAG (Retrieval) Tests:**
- "Latest property tax rules 2025"
- "Current garbage collection schedule"
- "Recent water supply updates"

**KAG (Knowledge) Tests:**
- "How to get new water connection?"
- "Property tax payment procedure"
- "Steps to register birth certificate"

**SLM (Language) Tests:**
- "Hello, who are you?"
- "What can you help me with?"
- "Thank you for your help"

## 🎯 Deployment Options

### Local Development
```bash
streamlit run main.py
```

### Production Deployment

1. **Streamlit Cloud**
   - Push to GitHub repository
   - Connect to Streamlit Cloud
   - Deploy with one click

2. **Docker Deployment**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 8501
   CMD ["streamlit", "run", "main.py"]
   ```

3. **Heroku Deployment**
   ```bash
   # Add Procfile: web: streamlit run main.py --server.port $PORT
   git push heroku main
   ```

## 📈 Future Enhancements

- **Voice Input/Output**: Speech recognition and text-to-speech
- **Multi-language**: Tamil language support
- **Mobile App**: React Native or Flutter version
- **Real-time Updates**: Live data feeds from government APIs
- **Analytics Dashboard**: Usage statistics and popular queries
- **Feedback System**: User rating collection and analysis

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Add your improvements
4. Test thoroughly
5. Submit pull request

## 📝 License

This project is designed for educational and civic service purposes.
Ensure compliance with local data protection and AI usage regulations.

---

**CivicMindAI** - Empowering Chennai citizens with AI-powered civic assistance! 🏛️🤖
