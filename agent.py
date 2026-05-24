import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt

load_dotenv()

search_tool = TavilySearch(max_results=5)
tools = [search_tool]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

system_prompt = (
    "You are a professional and autonomous research assistant. Your role is to gather high-quality sources from the internet only. "
    "When the user gives you a topic, you must:\n"
    "1. Decide on appropriate search queries.\n"
    "2. Use the search tool to find relevant sources.\n"
    "3. Present an organized list including: source name, link (URL), and a brief summary of the information found.\n"
    "4. Decide on your own how many searches to perform until you have a sufficient picture.\n\n"
    "Important: At this stage, do not provide a summary beyond describing the sources you found."
)

memory = MemorySaver()
agent_graph = create_react_agent(
    llm,
    tools,
    prompt=system_prompt,
    checkpointer=memory,
    interrupt_after=["tools"]
)
def run_interactive_research():
    topic = input("Enter a topic to research: ")

    config = {"configurable": {"thread_id": "research_session_1"}}
    print(f"\n🔎 Agent starting research on: '{topic}'...")
    events = agent_graph.stream(
        {"messages": [("user", topic)]}, 
        config, 
        stream_mode="values"
    )
    
    for event in events:
        if "messages" in event:
            last_msg = event["messages"][-1]
            
            if last_msg.type == "ai" and last_msg.content:
                print(f"\n🤖 Agent suggests:\n{last_msg.content}")
            
            elif last_msg.type == "tool":
                print("\n🌐 [Found Sources from Tavily]:")
                print(last_msg.content)

    state = agent_graph.get_state(config)
    if state.next:
        print("\n🛑 [HUMAN IN THE LOOP] The system is waiting for your decision.")
        user_feedback = input("Which sources to approve? (type 'approve all' or specify which sites to remove): ")

        print("\n⏳ Updating the agent and continuing...")

        resume_events = agent_graph.stream(
            {"messages": [("user", f"Here is my feedback on the sources: {user_feedback}. Act accordingly and present only the final approved list.")]},
            config,
            stream_mode="values"
        )
        for event in resume_events:
            if "messages" in event:
                last_msg = event["messages"][-1]
                if last_msg.type == "ai" and last_msg.content:
                    print(f"\n🤖 Agent presents the final list:\n{last_msg.content}")

        while agent_graph.get_state(config).next:
            for event in agent_graph.stream(None, config, stream_mode="values"):
                if "messages" in event:
                    last_msg = event["messages"][-1]
                    if last_msg.type == "ai" and last_msg.content:
                        print(f"\n🤖 Agent presents the final list:\n{last_msg.content}")


if __name__ == "__main__":
    run_interactive_research()
