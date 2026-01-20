# hr_agent.py
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import os

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_xxxxxxxxxxxxxx"  # ← your token

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    temperature=0.6,
    max_new_tokens=400
)
model = ChatHuggingFace(llm=llm)


@tool
def search_candidates(skill: str, experience_years: int) -> str:
    """Fake candidate search (replace with real API later)"""
    return f"Found 3 candidates with {skill} and ≥{experience_years} years:\n• Ana – 5y\n• Raj – 8y\n• Priya – 4y"


@tool
def calculate_notice_period(join_date: str) -> str:
    """Dummy notice period calculator"""
    return "Standard notice: 60 days"


tools = [search_candidates, calculate_notice_period]

hr_agent = create_react_agent(model, tools)


if __name__ == "__main__":
    query = "Find backend engineer with at least 5 years experience"
    result = hr_agent.invoke({"messages": [{"role": "user", "content": query}]})
    print(result["messages"][-1].content)