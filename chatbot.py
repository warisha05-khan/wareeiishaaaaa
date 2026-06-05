"""
AI Health Assistant powered by Google Gemini (google-generativeai SDK)
"""

import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Emergency keywords - bypass AI entirely
EMERGENCY_KEYWORDS = [
    'chest pain', 'difficulty breathing', 'severe bleeding',
    'loss of consciousness', 'severe head injury', 'stroke symptoms',
    'severe allergic reaction', 'suicidal', 'want to die', 'heart attack',
    "can't breathe", 'unconscious', 'seizure', 'not breathing',
    'overdose', 'poisoning', 'severe burn', 'choking'
]

SYSTEM_PROMPT = """You are an expert AI Health & Wellness Assistant. You are knowledgeable, warm, and empathetic.

YOUR CAPABILITIES:
- Analyze symptoms and explain possible general causes (educational only)
- Recommend appropriate exercises for health conditions or fitness goals
- Provide detailed lifestyle change advice (sleep, stress, diet, habits)
- Give nutrition and diet guidance
- Explain medical terms and health concepts clearly
- Provide mental wellness tips
- Suggest when to see a doctor and what type of specialist

YOUR STRICT RULES (NEVER BREAK):
1. NEVER diagnose any medical condition — always say "possible causes" or "commonly associated with"
2. NEVER prescribe specific medications or dosages
3. ALWAYS recommend consulting a doctor for persistent or serious symptoms
4. ALWAYS end with a brief disclaimer that you provide educational info, not medical advice
5. Be thorough and helpful — don't give vague one-line answers
6. Use clear headings and organized formatting in responses
7. For exercise recommendations, mention to consult a doctor first if they have health conditions
8. Be culturally sensitive and inclusive in your advice

RESPONSE STYLE:
- Use emojis sparingly for readability
- Structure responses with clear sections using markdown
- Be warm and encouraging, not clinical and cold
- Give actionable, practical advice
- Aim for 200-400 words per response"""


def detect_emergency(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in EMERGENCY_KEYWORDS)


def get_crisis_response():
    return """### 🚨 MEDICAL EMERGENCY DETECTED

**Please seek immediate medical attention RIGHT NOW.**

📞 **Emergency Services:**
- 🇵🇰 Pakistan: **115** (Rescue) / **1122** (Emergency) / **1021** (Edhi)
- 🌍 International: **112**
- 🇺🇸 US/Canada: **911**
- 🇬🇧 UK: **999**

**Go to your nearest Emergency Room immediately.**

⚠️ Do NOT rely on AI for emergencies. Close this and call for help now.

**Mental Health Crisis (Pakistan):** 0311-7786264 (Umang helpline)"""


def get_gemini_response(user_message, chat_history):
    """Call Gemini API using google-generativeai SDK"""

    if not GOOGLE_API_KEY:
        return """### ⚙️ Gemini API Key Not Found

To enable the AI assistant, add your Google Gemini API key:

**On Streamlit Cloud:**
1. Open your app → ⋮ menu → **Settings** → **Secrets**
2. Add this line:
```
GOOGLE_API_KEY = "your_api_key_here"
```

**Get a FREE API key:** [aistudio.google.com](https://aistudio.google.com)

Once added, I can help with symptom education, exercise plans, diet advice, lifestyle changes, and much more!"""

    try:
        import google.generativeai as genai

        genai.configure(api_key=GOOGLE_API_KEY)

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 1000,
            }
        )

        # Build history for multi-turn conversation (exclude last user message)
        history = []
        for msg in chat_history[-10:]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=history)
        response = chat.send_message(user_message)
        return response.text

    except ImportError:
        return """### ❌ Package Not Installed

The `google-generativeai` package is missing. Make sure your `requirements.txt` contains:

```
google-generativeai>=0.7.0
```

Then redeploy your Streamlit app."""

    except Exception as e:
        error_msg = str(e)

        # Give helpful hints for common errors
        if "API_KEY" in error_msg or "api key" in error_msg.lower() or "invalid" in error_msg.lower():
            return """### 🔑 Invalid API Key

Your Gemini API key appears to be invalid or expired.

**Fix:**
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Create a new API key
3. Update it in your Streamlit Secrets

Make sure there are no extra spaces or quotes around the key."""

        elif "quota" in error_msg.lower() or "429" in error_msg:
            return """### ⏳ API Quota Exceeded

You've hit the Gemini API rate limit. 

**Options:**
- Wait a minute and try again
- Check your quota at [console.cloud.google.com](https://console.cloud.google.com)
- The free tier allows ~60 requests/minute"""

        elif "model" in error_msg.lower() and "not found" in error_msg.lower():
            return f"""### 🤖 Model Not Available

The requested model isn't available for your API key.

**Error:** `{error_msg}`

This usually resolves itself. Try again in a moment, or check that your API key has access to Gemini models at [aistudio.google.com](https://aistudio.google.com)."""

        else:
            return f"""### ⚠️ Connection Error

Couldn't reach Gemini AI right now.

**Error details:** `{error_msg}`

**Things to try:**
- Check your internet connection
- Verify your API key in Streamlit Secrets
- Wait a moment and try again

For health info in the meantime, visit [mayoclinic.org](https://www.mayoclinic.org) or consult your doctor."""


def save_chat_history(patient_id, user_message, bot_response):
    """Save chat history to CSV"""
    import pandas as pd

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


# Quick action prompts
QUICK_PROMPTS = {
    "🩺 Check Symptoms": "I want to describe my symptoms and learn about possible causes and what I should do.",
    "🏃 Exercise Plan": "Recommend a beginner-friendly exercise routine. I'll tell you my goals and any conditions.",
    "🥗 Diet & Nutrition": "Give me practical, evidence-based diet and nutrition advice for a healthier lifestyle.",
    "💤 Sleep Problems": "I'm having trouble sleeping. Explain common causes and give me tips to improve sleep quality.",
    "🧘 Stress & Anxiety": "Give me science-backed techniques to manage stress and anxiety in daily life.",
    "❤️ Heart Health": "What lifestyle changes and habits improve cardiovascular health the most?",
    "⚖️ Weight Management": "Give me healthy and sustainable weight management advice.",
    "🌿 Healthy Habits": "Help me build a daily routine with healthy habits for energy, focus, and long-term wellness.",
}


def chatbot_ui():
    """Main chatbot interface"""

    st.subheader("🤖 AI Health & Wellness Assistant")
    st.caption("Powered by Google Gemini • Educational information only, not medical advice")

    # API status banner
    if GOOGLE_API_KEY:
        st.success("✅ Gemini AI connected — Ask me anything about health, symptoms, fitness, or lifestyle!")
    else:
        st.error("❌ Gemini API key missing — Add `GOOGLE_API_KEY` to your Streamlit Secrets to enable AI")

    # Collapsible disclaimer
    with st.expander("⚠️ Medical Disclaimer (click to read)", expanded=False):
        st.warning("""
        This AI assistant provides **general health information for educational purposes only**.

        - ❌ Does **NOT** diagnose medical conditions  
        - ❌ Does **NOT** prescribe medications or treatments  
        - ✅ Provides **educational information** to help you understand health topics  
        - ✅ Always **consult a qualified doctor** for medical advice  

        🔴 **For emergencies, call 115 (Pakistan) or your local emergency number immediately.**
        """)

    # Patient selection
    if st.session_state.get('patients'):
        patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
        selected_patient = st.selectbox(
            "👤 Patient (optional — for saving chat history)",
            ["Guest"] + [p['patient_id'] for p in st.session_state.patients],
            format_func=lambda x: f"{x} — {patient_names[x]}" if x in patient_names else x
        )
    else:
        selected_patient = "Guest"

    # Initialize chat
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": """👋 **Welcome! I'm your AI Health & Wellness Assistant.**

I can help you with:

🩺 **Symptom Education** — Understand what your symptoms might mean  
🏃 **Exercise Recommendations** — Plans tailored to your goals & health  
🥗 **Nutrition & Diet** — Practical, science-backed eating advice  
🧘 **Mental Wellness** — Stress, anxiety, sleep & mindfulness  
❤️ **Lifestyle Changes** — Build sustainable healthy habits  
💊 **Health Education** — Learn about conditions, tests, and more  

**Use the quick buttons below** or just type your question freely.

> ⚠️ I provide educational information only — not medical diagnosis or prescriptions. Always consult a doctor for medical concerns.

**What would you like to know today?**"""
            }
        ]

    # Display chat history
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Quick action buttons
    st.markdown("---")
    st.caption("⚡ **Quick actions:**")
    cols = st.columns(4)

    for i, (label, prompt_text) in enumerate(QUICK_PROMPTS.items()):
        with cols[i % 4]:
            if st.button(label, key=f"quick_{i}", use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": label})

                if detect_emergency(prompt_text):
                    response = get_crisis_response()
                else:
                    response = get_gemini_response(prompt_text, st.session_state.chat_messages[:-1])

                st.session_state.chat_messages.append({"role": "assistant", "content": response})

                if selected_patient != "Guest":
                    save_chat_history(selected_patient, label, response)

                st.rerun()

    st.markdown("---")

    # Chat input
    if prompt := st.chat_input("Ask about symptoms, exercises, diet, mental health, lifestyle..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if detect_emergency(prompt):
                    response = get_crisis_response()
                else:
                    response = get_gemini_response(prompt, st.session_state.chat_messages[:-1])
            st.markdown(response)

        st.session_state.chat_messages.append({"role": "assistant", "content": response})

        if selected_patient != "Guest":
            save_chat_history(selected_patient, prompt, response)

    # Clear button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "Conversation cleared! How can I help with your health and wellness today?"}
            ]
            st.rerun()

    st.markdown("""
    <div style="background:#f0f2f5;padding:12px 15px;border-radius:10px;font-size:0.78rem;margin-top:8px;">
    ⚠️ <strong>Disclaimer:</strong> Educational information only — not medical diagnosis or advice.
    🔴 <strong>Emergencies: Call 115 or 1122 (Pakistan) immediately.</strong>
    </div>
    """, unsafe_allow_html=True)
