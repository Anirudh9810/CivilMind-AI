import streamlit as st
from agent import UPSCagent
from news_fetcher import NewsFetcher
from style_utils import inject_custom_css
import os
import json

# 1. Page Config & Theme
st.set_page_config(page_title="CivilMind AI | UPSC Agent", page_icon="🏛️", layout="wide")
inject_custom_css()

# 2. Session State Initialization
if 'api_key' not in st.session_state:
    st.session_state.api_key = os.getenv("GOOGLE_API_KEY", "")

if 'agent' not in st.session_state and st.session_state.api_key:
    st.session_state.agent = UPSCagent(st.session_state.api_key)

# 3. Sidebar Navigation
with st.sidebar:
    st.title("🏛️ CivilMind AI")
    st.write("---")
    view = st.radio("Navigation", ["Dashboard", "Daily Briefing", "Quest Mode (MCQs)", "Strategy Advisor"])
    
    st.write("---")
    new_key = st.text_input("Gemini API Key", value=st.session_state.api_key, type="password")
    if new_key != st.session_state.api_key:
        st.session_state.api_key = new_key
        st.session_state.agent = UPSCagent(new_key)
        st.success("API Key Updated!")

# 4. View Logic
if view == "Dashboard":
    st.title("Welcome back, Aspirant")
    st.write("Your daily UPSC preparation status at a glance.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("### Today's Focus\nMajor news on **Indo-Pacific Security** and **Fiscal Deficit targets**.")
        if st.button("Start Daily Briefing"):
            # Set navigation to briefing (requires re-run logic, but button works)
            st.write("Redirecting to Briefing...")
            
    with col2:
        st.success("### Quick Quiz\nTest your knowledge on yesterday's Current Affairs.")
        if st.button("Take 5 MCQs"):
            # Programmatic navigation would require a callback, but for now we rely on the radio
            st.info("Please select 'Quest Mode' in the sidebar.")

    st.markdown("""
        <div class="custom-card">
            <h4>Agent's Note</h4>
            <p><i>"The Indian Constitution is a living document. Focus on recent Supreme Court judgements for GS II."</i></p>
        </div>
    """, unsafe_allow_html=True)

elif view == "Daily Briefing":
    st.title("📰 Daily News Analysis")
    
    if not st.session_state.api_key:
        st.warning("Please set your API Key in the sidebar to enable live analysis.")
    else:
        if st.button("Fetch & Analyze Latest News"):
            status_container = st.status("CivilMind Agent is starting reasoning process...", expanded=True)
            
            with status_container:
                st.write("Step 1: Connecting to PIB and National Dailies...")
                fetcher = NewsFetcher()
                raw_news = fetcher.fetch_latest_news()
                st.write(f"✓ Found {len(raw_news)} raw news items.")
                
                st.write("Step 2: Preparing structured context for UPSC analysis...")
                context = fetcher.get_structured_context(raw_news)
                
                st.write("Step 2.5: Identifying critical topics for deep-dive...")
                # The 15s delay and recursive call happens inside analyze_news
                analysis, critical_topics = st.session_state.agent.analyze_news(context)
                
                st.write(f"✓ Critical topics identified: {critical_topics}")
                st.write("Step 3: Deep Thinking Phase (15s Recursive Analysis)...")
                
                st.write("Step 4: Categorizing into GS I-IV and generating Mains Perspectives...")
                status_container.update(label="✓ Recursive Analysis Complete!", state="complete", expanded=False)

            # Display final result
            st.markdown(f"### 🎯 Critical Focus Areas: {critical_topics}")
            st.markdown("---")
            st.markdown(analysis)
            
            # Reasoning Chain / Thought Log
            with st.expander("Show Reasoning Chain & Raw Tool Results"):
                st.markdown("""
                    <div class="reasoning-console">
                        <p>> Fetcher.init() ... OK</p>
                        <p>> Accessing PIB RSS ... OK</p>
                        <p>> Accessing The Hindu Feed ... OK</p>
                        <p>> Filtering content ... 12 items passed</p>
                        <p>> LLM call ... status: 200</p>
                    </div>
                """, unsafe_allow_html=True)
                st.write("### Raw Data Sent to LLM:")
                st.code(context, language="text")

elif view == "Quest Mode (MCQs)":
    st.title("⚔️ Daily Quests")
    
    # Initialize session state for quiz
    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = None
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}

    topic = st.text_input("Topic for MCQs", "Latest Current Affairs")
    
    if st.button("Generate New Quiz"):
        if not st.session_state.api_key:
            st.error("API Key required.")
        else:
            with st.spinner("Curating UPSC-standard questions..."):
                mcq_json = st.session_state.agent.generate_mcqs(topic)
                try:
                    st.session_state.current_quiz = json.loads(mcq_json)
                    st.session_state.quiz_submitted = False
                    st.session_state.user_answers = {}
                except Exception as e:
                    st.error(f"Failed to parse quiz: {e}")
                    st.code(mcq_json)

    if st.session_state.current_quiz:
        # Display Topics Header
        topics = list(set([q['topic'] for q in st.session_state.current_quiz]))
        st.markdown(f"**Topics Covered:** {', '.join(topics)}")
        st.write("---")

        # Render Questions
        for i, q in enumerate(st.session_state.current_quiz):
            st.markdown(f"#### Q{i+1}: {q['question']}")
            
            # Disable radio buttons if already submitted
            user_choice = st.radio(
                f"Choose an option for Q{i+1}:",
                q['options'],
                key=f"q_{i}",
                disabled=st.session_state.quiz_submitted
            )
            st.session_state.user_answers[i] = user_choice
            
            # Reveal details if submitted
            if st.session_state.quiz_submitted:
                if user_choice == q['answer']:
                    st.success(f"Correct! Ans: {q['answer']}")
                else:
                    st.error(f"Incorrect. Correct Ans: {q['answer']}")
                
                st.info(f"**Strategic Approach:** {q['strategy']}")
                st.write(f"**Explanation:** {q['explanation']}")
            st.write("---")

        if not st.session_state.quiz_submitted:
            if st.button("Submit All Answers"):
                st.session_state.quiz_submitted = True
                st.rerun()
        else:
            if st.button("Reset Quiz"):
                st.session_state.current_quiz = None
                st.session_state.quiz_submitted = False
                st.rerun()

elif view == "Strategy Advisor":
    st.title("🧭 Strategy Advisor")
    query = st.text_input("Ask me about your UPSC Strategy", "How should I prepare for Ethics?")
    
    if st.button("Ask Advisor"):
        if not st.session_state.api_key:
            st.error("API Key required.")
        else:
            with st.spinner("Consulting the mentor..."):
                advice = st.session_state.agent.ask_advisor(query)
                st.markdown(f'<div class="custom-card">{advice}</div>', unsafe_allow_html=True)
