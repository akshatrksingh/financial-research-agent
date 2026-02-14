
# """Simple agent."""
# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from groq import Groq
# from config import GROQ_API_KEY, GROQ_MODEL
# from tools.mock_portfolio import get_portfolio
# from tools.market_data import get_stock_data
# from tools.web_search import search_web
# import json

# client = Groq(api_key=GROQ_API_KEY)

# def extract_ticker(query):
#     """Find stock ticker in query."""
#     known = ['AAPL', 'NVDA', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'META', 'NFLX']
#     query_upper = query.upper()
#     for ticker in known:
#         if ticker in query_upper:
#             return ticker
#     return None

# def run_agent(user_query):
#     """Run agent."""
#     context = {}
    
#     # Portfolio
#     if "portfolio" in user_query.lower():
#         context["portfolio"] = get_portfolio()
    
#     # Stock data
#     ticker = extract_ticker(user_query)
#     if ticker:
#         context["stock_data"] = get_stock_data(ticker)
    
#     # News
#     if "news" in user_query.lower():
#         context["news"] = search_web(user_query)
    
#     if not context:
#         return "No data found. Try asking about: stock prices, portfolio, or news."
    
#     # Synthesize
#     prompt = f"""Answer using this data:
# {json.dumps(context, indent=2)}

# Question: {user_query}
# Be concise, use exact numbers."""
    
#     response = client.chat.completions.create(
#         model=GROQ_MODEL,
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.1
#     )
    
#     return response.choices[0].message.content

# if __name__ == "__main__":
#     print(run_agent("Summarise my portfolio and the current price of NVIDIA."))



"""Agent using LangChain for tool orchestration."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from config import GROQ_API_KEY, GROQ_MODEL
from tools.mock_portfolio import get_portfolio
from tools.market_data import get_stock_data
from tools.web_search import search_web
import json

# Initialize LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0
)

# Define tools
def portfolio_tool(query: str) -> str:
    """Get user's portfolio with current values."""
    portfolio = get_portfolio()
    
    # Enrich with current prices
    for holding in portfolio["holdings"]:
        ticker = holding["ticker"]
        current_data = get_stock_data(ticker)
        holding["current_price"] = current_data.get("price")
        if holding["current_price"]:
            holding["current_value"] = holding["shares"] * holding["current_price"]
            holding["gain_loss"] = holding["current_value"] - (holding["shares"] * holding["avg_cost"])
    
    return json.dumps(portfolio, indent=2)

def stock_price_tool(ticker: str) -> str:
    """Get current stock price and info. Input should be a ticker symbol like AAPL."""
    data = get_stock_data(ticker.upper())
    return json.dumps(data, indent=2)

def news_tool(query: str) -> str:
    """Search for latest news. Input should be a search query."""
    results = search_web(query)
    return json.dumps(results[:3], indent=2)  # Top 3 results

# Create LangChain tools
tools = [
    Tool(
        name="Portfolio",
        func=portfolio_tool,
        description="Use this to get the user's stock portfolio, holdings, and current values. Input: any query about portfolio."
    ),
    Tool(
        name="StockPrice",
        func=stock_price_tool,
        description="Use this to get current stock price and market data. Input: ticker symbol (e.g., AAPL, NVDA, MSFT)."
    ),
    Tool(
        name="News",
        func=news_tool,
        description="Use this to search for latest news about stocks or companies. Input: search query."
    )
]

# Create prompt template
template = """Answer the following question as best you can. You have access to these tools:

{tools}

Use this format:

Question: the input question
Thought: think about what to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Question: {input}
{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# Create agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True,
    max_iterations=5
)

def run_agent(user_query: str) -> str:
    """Run the LangChain agent."""
    try:
        result = agent_executor.invoke({"input": user_query})
        return result["output"]
    except Exception as e:
        return f"Error: {str(e)}\n\nTry:\n• 'What's AAPL's price?'\n• 'What's my portfolio worth?'\n• 'Latest news on Tesla'"

if __name__ == "__main__":
    queries = [
        "What's NVDA's price one year back?",
        "Latest news on Apple"
    ]
    
    for q in queries:
        print(f"\n{'='*60}")
        print(f"Q: {q}")
        print(f"{'='*60}")
        print(run_agent(q))