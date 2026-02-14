# """Configuration and API key management."""
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # API Keys
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# # Validate
# if not GROQ_API_KEY:
#     raise ValueError("GROQ_API_KEY not found in .env file")
# if not TAVILY_API_KEY:
#     raise ValueError("TAVILY_API_KEY not found in .env file")

# # Model settings
# GROQ_MODEL = "llama-3.3-70b-versatile"
# EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# # Vector DB
# CHROMA_PERSIST_DIR = "./chroma_db"

# print("✅ Config loaded successfully")



"""Configuration and API key management."""
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file")

GROQ_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHROMA_PERSIST_DIR = "./chroma_db"

print("✅ Config loaded successfully")
