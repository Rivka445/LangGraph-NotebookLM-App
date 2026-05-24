import streamlit as st
from agent import build_agent, summarize
from search import fetch_sources

st.set_page_config(page_title="NotebookLM Mini", page_icon="🏗️", layout="centered")
st.title("🏗️ NotebookLM Mini")
st.write("Enter a topic, the agent will gather sources and you can choose which ones to include in the final summary.")

if "agent_graph" not in st.session_state:
    st.session_state.agent_graph, st.session_state.config = build_agent()
    st.session_state.step = "input"
    st.session_state.raw_sources = []

# --- Step 1: Enter topic ---
if st.session_state.step == "input":
    topic = st.text_input("What topic would you like to research?", placeholder="e.g. Angular 18 new features")

    if st.button("Start Research 🔎"):
        if topic:
            with st.spinner("Scanning the internet for sources..."):
                st.session_state.raw_sources = fetch_sources(topic)
                st.session_state.topic = topic
                st.session_state.step = "approve"
                st.rerun()
        else:
            st.warning("Please enter a topic first.")

# --- Step 2: Approve sources ---
elif st.session_state.step == "approve":
    st.subheader(f"🛑 Approve sources for: '{st.session_state.topic}'")
    st.write("Check the sources you want to include in the summary:")

    for idx, source in enumerate(st.session_state.raw_sources):
        title = source.get("title", f"Source {idx+1}")
        url = source.get("url", "#")
        st.checkbox(f"🔗 [{title}]({url})", value=True, key=f"src_{idx}")

    if st.button("Confirm selected sources and summarize 🚀"):
        approved_sources = [
            source for idx, source in enumerate(st.session_state.raw_sources)
            if st.session_state.get(f"src_{idx}", False)
        ]
        with st.spinner("Agent is processing approved sources..."):
            st.session_state.final_result = summarize(
                st.session_state.agent_graph,
                st.session_state.config,
                st.session_state.topic,
                approved_sources
            )
            st.session_state.step = "final"
            st.rerun()

# --- Step 3: Final result ---
elif st.session_state.step == "final":
    st.subheader("🎯 Final Summary")
    st.markdown(st.session_state.final_result)

    if st.button("New Research 🔄"):
        st.session_state.step = "input"
        st.session_state.raw_sources = []
        st.rerun()
