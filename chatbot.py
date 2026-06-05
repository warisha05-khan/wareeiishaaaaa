"""
Mental Health Chatbot Module powered by Google Gemini AI
Provides empathetic support with crisis detection
"""

import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables (works for both local and cloud)
load_dotenv()

# Get API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Crisis keywords for emergency detection
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die", "don't want to live",
    "self harm", "cut myself", "hurt myself", "emergency", "crisis",
    "overdose", "help me please", "i can't go on", "no hope"
]

# Support resources
CRISIS_RESPONSE = """
### 🚨 **I hear that you're going through a really difficult time right now.**

**Please reach out to professional support immediately:**
- **988 Suicide and Crisis Lifeline** (US): Call or text **988** - 24/7, free, confidential
- **Crisis Text Line**: Text **HOME** to **741741**
- **Emergency Services**: Call **911** (or your local emergency number)

**You are not alone. People care about you and want to help. Please reach out now.** 💙
"""

# System prompt for mental health context
MENTAL_HEALTH_PROMPT = """You are a compassionate, empathetic mental health support assistant. Your role is to:

1. Listen actively and show empathy
2. Validate the user's feelings
3. Ask gentle, open-ended questions when appropriate
4. Suggest healthy coping strategies (deep breathing, grounding exercises, journaling)
5. NEVER provide clinical diagnoses or medical advice
6. ALWAYS remind users to seek professional help for serious concerns
7. Keep responses warm, supportive, and conversational (2-4 sentences typically)

For stress/anxiety: Suggest deep breathing, 5-4-3-2-1 grounding technique
For sadness: Normalize feelings, suggest talking to someone or light activity
For loneliness: Recommend connecting with friends, family, or support groups

Important disclaimers to include naturally:
- "I'm an AI, not a therapist"
- "If you're in crisis, please contact emergency services"

Keep responses helpful but concise. Be warm and caring.

Current conversation:"""


def detect_crisis(user_message):
    """Check if user message contains crisis indicators"""
    user_lower = user_message.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in user_lower:
            return True
    return False


def save_chat_history(patient_id, user_message, bot_response):
    """Save chat history to CSV file for persistence"""
    import pandas as pd
    import os
    
    os.makedirs("hospital_data", exist_ok=True)
    
    chat_file = f"hospital_data/chat_history_{patient_id}.csv"
    
    new_entry = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'user_message': user_message,
        'bot_response': bot_response[:200]
    }
    
    if os.path.exists(chat_file):
        df = pd.read_csv(chat_file)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])
    
    if len(df) > 100:
        df = df.tail(100)
    
    df.to_csv(chat_file, index=False)


def load_chat_history(patient_id):
    """Load chat history for a specific patient"""
    import pandas as pd
    import os
    
    chat_file = f"hospital_data/chat_history_{patient_id}.csv"
    if os.path.exists(chat_file):
        df = pd.read_csv(chat_file)
        return df.to_dict('records')
    return []


def get_gemini_response(user_message, chat_history_context):
    """Get empathetic response from Gemini API"""
    
    if not GOOGLE_API_KEY:
        return "⚠️ Chatbot is not configured. Please add your Google API key in Streamlit Cloud Settings → Secrets."
    
    if detect_crisis(user_message):
        return CRISIS_RESPONSE
    
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # UPDATED: Use the correct model name (gemini-pro is deprecated)
        # gemini-1.5-flash is faster and works well for chat
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        full_prompt = f"""{MENTAL_HEALTH_PROMPT}

Previous conversation:
{chat_history_context}

User says: {user_message}

Respond as a caring mental health support assistant:"""
        
        response = model.generate_content(full_prompt)
        return response.text
        
    except Exception as e:
        return f"I'm having trouble connecting right now. Please try again in a moment.\n\nError: {str(e)}"


def chatbot_ui():
    """Display the chatbot interface in Streamlit"""
    
    st.subheader("🧠 Mental Health Support Chatbot")
    st.caption("I'm here to listen and support. This is a safe, non-judgmental space.")
    
    # Check API key
    if not GOOGLE_API_KEY:
        st.error("""
        ### ⚠️ Chatbot Not Configured
        
        To use the mental health chatbot, add your Google Gemini API key:
        
        1. Go to **Settings** → **Secrets**
        2. Add: `GOOGLE_API_KEY = "your_key_here"`
        3. Click **Save**
        """)
        return
    
    st.success("✅ Chatbot is ready! I'm here to listen and support you.")
    
    # Patient selection
    if st.session_state.patients:
        patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
        selected_patient = st.selectbox(
            "Select Patient",
            ["Guest"] + [p['patient_id'] for p in st.session_state.patients],
            format_func=lambda x: f"{x} - {patient_names.get(x, 'Guest Mode')}" if x in patient_names else x
        )
    else:
        selected_patient = "Guest"
        st.info("Register a patient to save chat history.")
    
    # Initialize chat
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # Load history for patient
    if selected_patient != "Guest":
        if st.button("📜 Load Previous Chats"):
            history = load_chat_history(selected_patient)
            if history:
                st.session_state.chat_messages = []
                for entry in history:
                    st.session_state.chat_messages.append({"role": "user", "content": entry['user_message']})
                    st.session_state.chat_messages.append({"role": "assistant", "content": entry['bot_response']})
                st.success(f"Loaded {len(history)} conversations")
                st.rerun()
    
    st.info("💡 **Remember**: I'm an AI support companion, not a replacement for professional care.")
    
    # Display messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("How are you feeling today?"):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        context = ""
        for msg in st.session_state.chat_messages[-6:]:
            context += f"{msg['role']}: {msg['content']}\n"
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_gemini_response(prompt, context)
                st.markdown(response)
        
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        if selected_patient != "Guest":
            save_chat_history(selected_patient, prompt, response)
    
    # Quick buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧘 Deep Breathing", use_container_width=True):
            breathing = "**4-7-8 Breathing:** Inhale 4 sec → Hold 7 sec → Exhale 8 sec. Repeat 4 times."
            st.session_state.chat_messages.append({"role": "assistant", "content": breathing})
            st.rerun()
    
    with col2:
        if st.button("🌿 Grounding", use_container_width=True):
            grounding = "**5-4-3-2-1:** Name 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste."
            st.session_state.chat_messages.append({"role": "assistant", "content": grounding})
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()
