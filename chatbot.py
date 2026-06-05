"""
Medical Symptom Checker & Health Assistant with Gemini AI
Provides educational information and triage recommendations
Gemini enhances responses but strict safety rules prevent medical diagnosis
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Emergency keywords - immediate action required (NO Gemini for these)
EMERGENCY_KEYWORDS = [
    'chest pain', 'difficulty breathing', 'severe bleeding', 
    'loss of consciousness', 'severe head injury', 'stroke symptoms',
    'severe allergic reaction', 'suicidal', 'want to die', 'heart attack',
    'can\'t breathe', 'unconscious', 'seizure'
]

# Symptom database for structured responses
SYMPTOM_INFO = {
    'headache': {
        'info': 'Headaches can be caused by stress, dehydration, tension, eye strain, or other factors.',
        'when_to_see_doctor': 'See a doctor if: severe, persistent >3 days, with fever, after head injury, with vision changes, or worst headache of your life.'
    },
    'fever': {
        'info': 'Fever is your body\'s natural defense against infection. Most fevers are harmless.',
        'when_to_see_doctor': 'See doctor if: temperature >103°F (39.5°C), lasts >3 days, in infants <3 months, or with severe symptoms.'
    },
    'cough': {
        'info': 'Cough helps clear your airways. Can be from cold, allergies, or infections.',
        'when_to_see_doctor': 'See doctor if: lasts >3 weeks, with blood, difficulty breathing, or high fever.'
    },
    'abdominal pain': {
        'info': 'Stomach pain can be from indigestion, gas, constipation, food poisoning, or other causes.',
        'when_to_see_doctor': 'Seek care if: severe pain, persistent >3 days, with fever, vomiting, or blood in stool.'
    },
    'fatigue': {
        'info': 'Fatigue can be caused by lack of sleep, stress, anemia, thyroid issues, or other conditions.',
        'when_to_see_doctor': 'See doctor if: persistent >2 weeks despite rest, with weight loss, or impacting daily life.'
    },
    'nausea': {
        'info': 'Nausea can be from food poisoning, pregnancy, motion sickness, or other causes.',
        'when_to_see_doctor': 'See doctor if: persistent >2 days, with severe abdominal pain, blood in vomit, or signs of dehydration.'
    },
    'sore throat': {
        'info': 'Sore throat is often from viral infections like cold or flu.',
        'when_to_see_doctor': 'See doctor if: severe pain, lasts >5 days, with fever >101°F, difficulty swallowing, or white patches.'
    },
    'back pain': {
        'info': 'Back pain is very common. Often from muscle strain, poor posture, or lifting incorrectly.',
        'when_to_see_doctor': 'See doctor if: after injury, with leg numbness/weakness, loss of bladder/bowel control, or fever.'
    }
}


def detect_emergency(user_message):
    """Check for emergency keywords - returns True if emergency detected"""
    user_lower = user_message.lower()
    for keyword in EMERGENCY_KEYWORDS:
        if keyword in user_lower:
            return True
    return False


def identify_symptom(user_message):
    """Identify which symptom the user is describing"""
    user_lower = user_message.lower()
    for symptom in SYMPTOM_INFO.keys():
        if symptom in user_lower:
            return symptom
    return None


def get_crisis_response():
    """Emergency response - NO Gemini, just redirect to emergency services"""
    return """
### 🚨 **MEDICAL EMERGENCY DETECTED** 🚨

**Please seek immediate medical attention RIGHT NOW:**

📞 **Call Emergency Services: 911 (US) / 112 (EU) / 999 (UK)**

**Go to the nearest Emergency Room immediately.**

⚠️ **Do NOT wait. Do NOT rely on AI or online information for emergencies.**

**If having a mental health crisis:**
- Call or text **988** (Suicide & Crisis Lifeline)
- Text **HOME** to **741741**
- Go to nearest emergency room

**Close this chat and seek professional help now. Your health and safety come first.**
"""


def get_gemini_health_response(user_message, symptom_name):
    """Use Gemini for enhanced, SAFE health information"""
    
    if not GOOGLE_API_KEY:
        # Fallback to rule-based response if no API key
        return get_rule_based_response(symptom_name)
    
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=GOOGLE_API_KEY)
        
        # STRICT SAFETY PROMPT - prevents diagnosis
        safety_prompt = f"""You are a HEALTH INFORMATION ASSISTANT, NOT A DOCTOR. You provide ONLY educational health information.

STRICT RULES (NEVER BREAK THESE):
1. NEVER diagnose any medical condition
2. NEVER recommend specific medications or treatments
3. ALWAYS say "consult a doctor" for medical advice
4. ALWAYS include disclaimer that you are not a medical professional
5. For symptoms like {symptom_name if symptom_name else 'the described symptom'}, provide general educational information only

User says: {user_message}

Provide a helpful, empathetic response that:
- Acknowledges their concern
- Gives general educational information about possible causes (as general knowledge, not diagnosis)
- Lists warning signs that need medical attention
- Recommends seeing a doctor for proper evaluation
- Includes a clear disclaimer

Keep response warm but professional. 3-4 sentences maximum."""
        
        response = client.models.generate_content(
            model='gemini-2.0-flash-lite',  # Faster, cheaper model
            contents=safety_prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=500,
            )
        )
        
        return response.text
        
    except Exception as e:
        # Fallback if Gemini fails
        return get_rule_based_response(symptom_name)


def get_rule_based_response(symptom_name):
    """Fallback rule-based response when Gemini unavailable"""
    if symptom_name and symptom_name in SYMPTOM_INFO:
        info = SYMPTOM_INFO[symptom_name]
        return f"""
### 📚 About {symptom_name.title()}

**What you should know:**
{info['info']}

**🏥 When to see a doctor:**
{info['when_to_see_doctor']}

**Self-care tips:**
- Rest and stay hydrated
- Monitor your symptoms
- Use over-the-counter remedies as directed (consult pharmacist)

### ⚠️ Important Reminder
I'm an AI assistant, not a doctor. This information is educational only. 
Please consult a healthcare provider for proper medical advice.
"""
    else:
        return """
### 💙 How I Can Help

I can provide educational information about common health concerns.

**Tell me about your symptom and I'll help you understand:**
- General information about the symptom
- When you should see a doctor
- Self-care tips

**Examples:**
- "I have a headache for 2 days"
- "My child has a fever"
- "I feel very tired lately"

⚠️ **Remember:** I'm not a doctor. I provide educational information only.
"""


def get_general_health_response(user_message):
    """Response when no specific symptom is identified"""
    return """
### 💙 I'm here to help with health information

I can provide educational information about common health concerns.

**What I can help with:**
- ✅ General information about symptoms like headache, fever, cough, stomach pain, fatigue, etc.
- ✅ When you should see a doctor
- ✅ Self-care tips for common conditions
- ✅ Answer general health questions

**What I cannot do:**
- ❌ Diagnose medical conditions
- ❌ Prescribe medications or treatments  
- ❌ Replace seeing a real doctor

**To get started, please tell me:**
- What symptoms are you experiencing?
- How long have you had them?

**For medical emergencies, call 911 immediately.**
"""


def save_chat_history(patient_id, user_message, bot_response):
    """Save chat history to CSV"""
    import pandas as pd
    import os
    
    os.makedirs("hospital_data", exist_ok=True)
    chat_file = f"hospital_data/chat_history_{patient_id}.csv"
    
    new_entry = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'user_message': user_message[:500],
        'bot_response': bot_response[:500]
    }
    
    if os.path.exists(chat_file):
        df = pd.read_csv(chat_file)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])
    
    if len(df) > 100:
        df = df.tail(100)
    
    df.to_csv(chat_file, index=False)


def chatbot_ui():
    """Main chatbot interface"""
    
    st.subheader("🏥 Medical Symptom Checker & Health Assistant")
    st.caption("AI-powered health information - Educational purposes only")
    
    # Show API status
    if GOOGLE_API_KEY:
        st.success("✅ Gemini AI is connected - I can provide enhanced health information")
    else:
        st.info("ℹ️ Running in basic mode. Add Gemini API key in Secrets for enhanced responses.")
    
    # Strong disclaimer
    st.warning("""
    ⚠️ **MEDICAL DISCLAIMER**: I am an AI assistant, NOT a doctor. 
    - I provide **educational information only**
    - I do **NOT diagnose** medical conditions
    - Always **consult a doctor** for medical advice
    - **Call 911** for emergencies
    """)
    
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
        st.session_state.chat_messages = [
            {"role": "assistant", "content": """Hello! I'm your health information assistant powered by AI.

**I can help you understand:**
- What your symptoms might mean (general educational info)
- When you should see a doctor
- Self-care tips for common conditions

**Tell me about your symptoms** (e.g., "I have a headache for 2 days" or "My child has fever and cough")

⚠️ **Remember**: I provide educational information only. Always consult a doctor for medical advice.

How can I help you today?"""}
        ]
    
    # Display chat history
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Quick symptom buttons
    st.markdown("---")
    st.caption("**Common symptoms I can help with:**")
    cols = st.columns(4)
    common_symptoms = ["Headache", "Fever", "Cough", "Abdominal pain", "Fatigue", "Nausea", "Sore throat", "Back pain"]
    
    for i, symptom in enumerate(common_symptoms):
        with cols[i % 4]:
            if st.button(f"📝 {symptom}", key=f"sym_{symptom}", use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": symptom})
                with st.chat_message("user"):
                    st.markdown(symptom)
                
                # Check emergency first
                if detect_emergency(symptom):
                    response = get_crisis_response()
                else:
                    symptom_lower = symptom.lower()
                    if symptom_lower in SYMPTOM_INFO:
                        if GOOGLE_API_KEY:
                            response = get_gemini_health_response(symptom, symptom_lower)
                        else:
                            response = get_rule_based_response(symptom_lower)
                    else:
                        response = get_general_health_response(symptom)
                
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
                
                if selected_patient != "Guest":
                    save_chat_history(selected_patient, symptom, response)
                
                st.rerun()
    
    st.markdown("---")
    
    # Chat input
    if prompt := st.chat_input("Describe your symptoms or ask a health question..."):
        
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Step 1: Check for emergency (ALWAYS first)
        if detect_emergency(prompt):
            response = get_crisis_response()
        
        else:
            # Step 2: Identify symptom
            symptom = identify_symptom(prompt)
            
            # Step 3: Generate response using Gemini (if available) or rule-based
            if symptom and GOOGLE_API_KEY:
                response = get_gemini_health_response(prompt, symptom)
            elif symptom:
                response = get_rule_based_response(symptom)
            else:
                response = get_general_health_response(prompt)
        
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        
        if selected_patient != "Guest":
            save_chat_history(selected_patient, prompt, response)
    
    # Clear chat button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "Conversation cleared. How can I help with your health questions today? Remember, I provide educational information only - not medical diagnosis."}
            ]
            st.rerun()
    
    # Footer
    st.markdown("""
    ---
    <div style="background: #f0f2f5; padding: 15px; border-radius: 10px; font-size: 0.8rem;">
    <strong>⚠️ IMPORTANT MEDICAL DISCLAIMER</strong><br>
    This AI assistant provides general health information for educational purposes only. 
    It does NOT provide medical diagnosis, treatment recommendations, or replace professional medical advice.
    <br><br>
    <strong>🔴 If you are experiencing a medical emergency, call emergency services immediately (911 in US).</strong>
    <br><br>
    Always consult a qualified healthcare provider for any health concerns.
    </div>
    """, unsafe_allow_html=True)
