import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()

class UPSCagent:
    """
    The 'Brain' of CivilMind AI.
    Handles reasoning, categorization, and MCQ generation.
    """
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
        
    def identify_critical_topics(self, context):
        """
        Pass 1: Identifies high-priority topics for deep-dive.
        """
        prompt = f"From the following UPSC news context, identify the TOP 2 most critical topics that require a deep-dive analysis for the Mains exam. Return only the topic names as a comma-separated list.\n\nContext: {context}"
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def analyze_news(self, news_context):
        """
        Pass 2: Recursive analysis. Synthesizes final briefing using initial context 
        and critical topic identification.
        """
        time.sleep(15)
        
        # 1. Internal Reasoning Loop
        critical_topics = self.identify_critical_topics(news_context)
        
        system_instruction = f"""
        You are CivilMind AI, a specialized UPSC Mentor.
        Your task is to analyze the provided news context and create a 'Daily Briefing'.
        
        Recursive Focus: You have identified '{critical_topics}' as high-priority areas. 
        Ensure the 'Mains Perspective' for these topics is exceptionally detailed.
        
        RULES:
        1. Categorize each item into GS I-IV.
        2. Format: Headline, GS Category, Context & Facts, Mains Perspective.
        3. Use a formal, bureaucratic tone.
        """
        
        prompt = f"Analyze the following news for UPSC candidates, focusing on the identified critical areas:\n\n{news_context}"
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
            )
        )
        return response.text, critical_topics

    def generate_mcqs(self, topic, count=3):
        """
        Generates MCQs with elimination hints and strategic approach.
        Returns a JSON string for structured parsing.
        """
        time.sleep(15)
        prompt = f"""
        Act as a UPSC Paper Setter. Generate {count} high-quality MCQs for the topics found in: {topic}.
        
        OUTPUT FORMAT: A valid JSON list of objects.
        
        Each object must have:
        - "topic": The specific subject (e.g., 'Polity', 'Climate Change').
        - "question": The question text.
        - "options": A list of 4 strings.
        - "answer": The correct option string (exact match from options).
        - "strategy": "How to approach" this specific question (Elimination tips, keyword focus).
        - "explanation": Detailed background linking to UPSC syllabus.
        
        Ensure the JSON is strictly valid.
        """
        
        response = self.model.generate_content(prompt)
        # Basic cleanup in case of markdown wrapping
        text = response.text.replace('```json', '').replace('```', '').strip()
        return text

    def ask_advisor(self, query):
        """
        Provides strategic mentorship.
        """
        time.sleep(15)
        prompt = f"You are a UPSC Strategy Mentor. Answer the following aspirant doubt: {query}"
        response = self.model.generate_content(prompt)
        return response.text
