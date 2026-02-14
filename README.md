# Financial Research Agent

Agentic AI system that provides personalized financial advice using:
- **LangGraph** for agent orchestration
- **Groq** (Llama 3.1 70B) as LLM
- **Tavily** for web search
- **Yahoo Finance** for market data
- **Chroma** for RAG over financial documents

---

## Setup

### 1. Clone & Environment
```bash
git clone <your-repo-url>
cd financial-research-agent
python3 -m venv financial-research-agent
source financial-research-agent/bin/activate
pip install -r requirements.txt
```

### 2. API Keys
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Run
```bash
streamlit run app.py
```

---

## Team Responsibilities

**Akshat**: Agent orchestration (LangGraph), project coordination  
**Netal**: Web search (Tavily) + Market data (Yahoo Finance)  
**Shruti**: RAG pipeline (Chroma + embeddings)  

---

## Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes, commit: `git commit -m "Add feature"`
3. Push: `git push origin feature/your-feature`
4. Open PR on GitHub
5. Review → Merge to main
