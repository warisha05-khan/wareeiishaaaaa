"""
Mental Health Chatbot Module powered by Google Gemini AI
Provides empathetic support with crisis detection
"""

import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    st.error("⚠️ Google API Key not found! Please add GOOGLE_API_KEY to your .env file")

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
    
    chat_file = f"hospital_data/chat_history_{patient_id}.csv"
    
    new_entry = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'user_message': user_message,
        'bot_response': bot_response[:200]  # Truncate for storage
    }
    
    if os.path.exists(chat_file):
        df = pd.read_csv(chat_file)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])
    
    # Keep only last 100 messages per patient
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
        return "⚠️ Chatbot is not configured. Please set up the Google API key in the .env file."
    
    # Check for crisis first
    if detect_crisis(user_message):
        return CRISIS_RESPONSE
    
    try:
        # Initialize the model
        model = genai.GenerativeModel('gemini-pro')
        
        # Build full prompt with context
        full_prompt = f"""{MENTAL_HEALTH_PROMPT}

Previous conversation:
{chat_history_context}

User says: {user_message}

Respond as a caring mental health support assistant:"""
        
        # Generate response
        response = model.generate_content(full_prompt)
        
        return response.text
        
    except Exception as e:
        return f"I'm having trouble connecting right now. Please try again in a moment. (Error: {str(e)})"


def chatbot_ui():
    """Display the chatbot interface in Streamlit"""
    
    st.markdown("""
    <style>
    .chat-message {
        padding: 10px;
        border-radius: 20px;
        margin: 5px 0;
        max-width: 80%;
    }
    .user-message {
        background-color: #1f6e4a;
        color: white;
        float: right;
        text-align: right;
    }
    .bot-message {
        background-color: #f0f2f5;
        color: black;
        float: left;
    }
    .disclaimer {
        font-size: 0.7rem;
        color: #666;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.subheader("🧠 Mental Health Support Chatbot")
    st.caption("I'm here to listen and support. This is a safe, non-judgmental space.")
    
    # Patient selection for chat history
    if st.session_state.patients:
        patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
        selected_patient = st.selectbox(
            "Select Patient (for saving chat history)",
            ["Guest (no history save)"] + [p['patient_id'] for p in st.session_state.patients],
            format_func=lambda x: f"{x} - {patient_names.get(x, 'Guest Mode')}" if x in patient_names else x
        )
    else:
        selected_patient = "Guest (no history save)"
        st.info("Register a patient to save chat history.")
    
    # Initialize session state for chat messages
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    
    # Load previous chat history if patient selected
    if selected_patient != "Guest (no history save)":
        if st.button("📜 Load Previous Chats"):
            history = load_chat_history(selected_patient)
            if history:
                st.session_state.chat_messages = []
                for entry in history:
                    st.session_state.chat_messages.append({"role": "user", "content": entry['user_message']})
                    st.session_state.chat_messages.append({"role": "assistant", "content": entry['bot_response']})
                st.success(f"Loaded {len(history)} previous conversations")
                st.rerun()
            else:
                st.info("No previous chat history found for this patient")
    
    # Display disclaimer
    st.info("💡 **Remember**: I'm an AI support companion, not a replacement for professional mental health care. For emergencies, please contact crisis services.")
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("How are you feeling today? I'm here to listen..."):
        
        # Add user message to chat
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Prepare context from last 5 exchanges
        context = ""
        for msg in st.session_state.chat_messages[-6:]:
            context += f"{msg['role']}: {msg['content']}\n"
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_gemini_response(prompt, context)
                st.markdown(response)
        
        # Add bot response to chat
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        
        # Save to history if patient selected
        if selected_patient != "Guest (no history save)":
            save_chat_history(selected_patient, prompt, response)
    
    # Quick action buttons
    st.markdown("---")
    st.caption("**Quick coping strategies:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧘 Deep Breathing", use_container_width=True):
            breathing_response = """**Try this 4-7-8 breathing technique:**

1. Inhale through your nose for **4 seconds**
2. Hold your breath for **7 seconds**
3. Exhale slowly through your mouth for **8 seconds**

Repeat 4 times. This activates your parasympathetic nervous system and reduces stress. How do you feel after trying it?"""
            st.session_state.chat_messages.append({"role": "assistant", "content": breathing_response})
            st.rerun()
    
    with col2:
        if st.button("🌿 Grounding Exercise", use_container_width=True):
            grounding_response = """**5-4-3-2-1 Grounding Technique**

- **5** things you can SEE around you
- **4** things you can TOUCH
- **3** things you can HEAR
- **2** things you can SMELL
- **1** thing you can TASTE

This brings you to the present moment. Name them out loud or write them down."""
            st.session_state.chat_messages.append({"assistant": "assistant", "content": grounding_response})
            st.rerun()
    
    with col3:
        if st.button("📝 Journal Prompt", use_container_width=True):
            journal_response = """**Today's journal prompt:**

"Today, I feel... because..."

Write freely for 5 minutes. Don't edit or judge - just let your thoughts flow. Journaling helps process emotions and reduce anxiety."""
            st.session_state.chat_messages.append({"role": "assistant", "content": journal_response})
            st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Current Conversation", use_container_width=True):
        st.session_state.chat_messages = []
        st.rerun()
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
    ⚠️ This chatbot is for emotional support and information only. It is not a substitute for 
    professional medical advice, diagnosis, or treatment. If you're experiencing a mental health 
    emergency, please contact emergency services or a crisis helpline immediately.
    </div>
    """, unsafe_allow_html=True)
