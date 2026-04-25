import streamlit as st

def inject_custom_css():
    """
    Injects the 'Bureaucratic Gold' design system into Streamlit.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap');

        /* Main Background */
        .stApp {
            background-color: #f8f9fa;
            color: #1e293b;
            font-family: 'Inter', sans-serif;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0f172a;
            color: #ffffff;
        }
        
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
            color: #ffffff !important;
        }
        
        [data-testid="stSidebar"] h1 {
            font-family: 'Playfair Display', serif;
        }

        /* Sidebar Radio Buttons contrast */
        [data-testid="stSidebar"] .st-eb {
            color: #ffffff !important;
        }

        /* Card-like containers */
        div.stButton > button {
            background-color: #b59410;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s;
        }

        div.stButton > button:hover {
            background-color: #d4af37;
            transform: translateY(-2px);
            color: white;
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Playfair Display', serif;
            color: #0f172a;
        }
        
        p, span, div {
            color: #1e293b;
        }

        .gs-badge {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            background-color: #e2e8f0;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 700;
            color: #b59410;
            margin-bottom: 0.5rem;
        }

        /* Custom Card Class */
        .custom-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }

        /* Reasoning Console */
        .reasoning-console {
            background-color: #1e293b;
            color: #10b981;
            font-family: 'Courier New', Courier, monospace;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #10b981;
            margin: 1rem 0;
            font-size: 0.9rem;
        }
        
        .reasoning-console p {
            color: #10b981 !important;
            margin: 0;
        }
        </style>
    """, unsafe_allow_html=True)
