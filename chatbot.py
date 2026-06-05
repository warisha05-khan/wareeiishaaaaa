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
