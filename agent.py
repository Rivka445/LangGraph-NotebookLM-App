from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from config import LLM_MODEL, LLM_TEMPERATURE, MAX_SEARCH_RESULTS, SYSTEM_PROMPT


def build_agent():
    llm = ChatOpenAI(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
    tools = [TavilySearch(max_results=MAX_SEARCH_RESULTS)]
    memory = MemorySaver()
    graph = create_react_agent(llm, tools, prompt=SYSTEM_PROMPT, checkpointer=memory)
    config = {"configurable": {"thread_id": "streamlit_session"}}
    return graph, config


def summarize(agent_graph, config, topic: str, approved_sources: list[dict]) -> str:
    sources_text = "\n\n".join([
        f"Title: {s['title']}\nURL: {s['url']}\nContent: {s['content']}"
        for s in approved_sources
    ])
    prompt = f"The user approved only these sources for the topic '{topic}'. Summarize them:\n\n{sources_text}"
    response = agent_graph.invoke({"messages": [("user", prompt)]}, config)
    return response["messages"][-1].content
