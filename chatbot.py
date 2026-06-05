app.py file is 

"""

ICT in Health - Hospital Management System with Persistent Storage

Data saved to CSV files - never loses data!

"""



import streamlit as st

import pandas as pd

import plotly.express as px

import plotly.graph_objects as go

from datetime import datetime

import os

import base64



# Import chatbot module

from chatbot import chatbot_ui



# Page configuration

st.set_page_config(

    page_title="ICT Health | Hospital Management System",

    page_icon="🏥",

    layout="wide"

)



# ==================== FILE STORAGE FUNCTIONS ====================



DATA_FOLDER = "hospital_data"



# Create data folder if it doesn't exist

if not os.path.exists(DATA_FOLDER):

    os.makedirs(DATA_FOLDER)



# File paths

PATIENTS_FILE = os.path.join(DATA_FOLDER, "patients.csv")

VITALS_FILE = os.path.join(DATA_FOLDER, "vitals.csv")

MEDICATIONS_FILE = os.path.join(DATA_FOLDER, "medications.csv")

APPOINTMENTS_FILE = os.path.join(DATA_FOLDER, "appointments.csv")



def load_patients():

    """Load patients from CSV file"""

    if os.path.exists(PATIENTS_FILE):

        df = pd.read_csv(PATIENTS_FILE)

        return df.to_dict('records')

    return []



def save_patients(patients):

    """Save patients to CSV file"""

    if patients:

        df = pd.DataFrame(patients)

        df.to_csv(PATIENTS_FILE, index=False)

    elif os.path.exists(PATIENTS_FILE):

        os.remove(PATIENTS_FILE)



def load_vitals():

    if os.path.exists(VITALS_FILE):

        df = pd.read_csv(VITALS_FILE)

        return df.to_dict('records')

    return []



def save_vitals(vitals):

    if vitals:

        df = pd.DataFrame(vitals)

        df.to_csv(VITALS_FILE, index=False)

    elif os.path.exists(VITALS_FILE):

        os.remove(VITALS_FILE)



def load_medications():

    if os.path.exists(MEDICATIONS_FILE):

        df = pd.read_csv(MEDICATIONS_FILE)

        return df.to_dict('records')

    return []



def save_medications(medications):

    if medications:

        df = pd.DataFrame(medications)

        df.to_csv(MEDICATIONS_FILE, index=False)

    elif os.path.exists(MEDICATIONS_FILE):

        os.remove(MEDICATIONS_FILE)



def load_appointments():

    if os.path.exists(APPOINTMENTS_FILE):

        df = pd.read_csv(APPOINTMENTS_FILE)

        return df.to_dict('records')

    return []



def save_appointments(appointments):

    if appointments:

        df = pd.DataFrame(appointments)

        df.to_csv(APPOINTMENTS_FILE, index=False)

    elif os.path.exists(APPOINTMENTS_FILE):

        os.remove(APPOINTMENTS_FILE)



# Initialize session state with data from files

def init_session_state():

    if 'patients' not in st.session_state:

        st.session_state.patients = load_patients()

    if 'vitals' not in st.session_state:

        st.session_state.vitals = load_vitals()

    if 'medications' not in st.session_state:

        st.session_state.medications = load_medications()

    if 'appointments' not in st.session_state:

        st.session_state.appointments = load_appointments()



init_session_state()



# ==================== HELPER FUNCTIONS ====================



def add_patient(patient_id, name, age, gender, contact, address):

    new_patient = {

        'patient_id': patient_id,

        'name': name,

        'age': age,

        'gender': gender,

        'contact': contact,

        'address': address,

        'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M")

    }

    st.session_state.patients.append(new_patient)

    save_patients(st.session_state.patients)

    return True



def add_vitals(patient_id, bp_sys, bp_dia, heart_rate, blood_sugar, weight, notes=""):

    new_vital = {

        'patient_id': patient_id,

        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        'bp_systolic': bp_sys,

        'bp_diastolic': bp_dia,

        'heart_rate': heart_rate,

        'blood_sugar': blood_sugar,

        'weight': weight,

        'notes': notes

    }

    st.session_state.vitals.append(new_vital)

    save_vitals(st.session_state.vitals)



def add_medication(patient_id, med_name, dosage, frequency, start_date, end_date):

    new_med = {

        'patient_id': patient_id,

        'med_name': med_name,

        'dosage': dosage,

        'frequency': frequency,

        'start_date': start_date,

        'end_date': end_date,

        'status': 'active'

    }

    st.session_state.medications.append(new_med)

    save_medications(st.session_state.medications)



def add_appointment(patient_id, doctor, date_time, reason):

    new_appointment = {

        'patient_id': patient_id,

        'doctor': doctor,

        'date_time': date_time,

        'reason': reason,

        'status': 'scheduled'

    }

    st.session_state.appointments.append(new_appointment)

    save_appointments(st.session_state.appointments)



# ==================== MAIN UI ====================



st.title("🏥 ICT in Health - Hospital Management System")

st.markdown("*Persistent Storage - Your data is saved forever!*")



# Display saved data count in sidebar

st.sidebar.success(f"📊 Data Stats:\n\n👥 Patients: {len(st.session_state.patients)}\n📊 Vitals: {len(st.session_state.vitals)}\n💊 Medications: {len(st.session_state.medications)}")



# Sidebar Navigation

st.sidebar.title("📋 Navigation")

menu = st.sidebar.selectbox(

    "Choose Module",

    ["🏠 Dashboard", "👨‍👩‍👧 Patient Registration", "📊 Vitals Logger", 

     "💊 Medication Manager", "📅 Appointments", "📈 Health Analytics", 

     "📄 Reports", "💾 Backup/Restore", "AI Health Assistant", 

     "ℹ️ About ICT in Health"]

)



# ==================== DASHBOARD ====================

if menu == "🏠 Dashboard":

    st.header("📊 Hospital Dashboard")

    

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric("👥 Total Patients", len(st.session_state.patients))

    with col2:

        st.metric("📊 Vitals Records", len(st.session_state.vitals))

    with col3:

        active_meds = len([m for m in st.session_state.medications if m.get('status') == 'active'])

        st.metric("💊 Active Medications", active_meds)

    with col4:

        st.metric("📅 Appointments", len(st.session_state.appointments))

    

    if st.session_state.patients:

        st.subheader("📋 Recent Patients")

        df_patients = pd.DataFrame(st.session_state.patients)

        st.dataframe(df_patients[['patient_id', 'name', 'age', 'gender', 'registration_date']], use_container_width=True)

    else:

        st.info("No patients registered yet. Go to Patient Registration to add.")



# ==================== PATIENT REGISTRATION ====================

elif menu == "👨‍👩‍👧 Patient Registration":

    st.header("📝 Register New Patient")

    

    with st.form("patient_registration"):

        col1, col2 = st.columns(2)

        with col1:

            patient_id = st.text_input("Patient ID (Unique)")

            name = st.text_input("Full Name")

            age = st.number_input("Age", min_value=0, max_value=150)

        with col2:

            gender = st.selectbox("Gender", ["Male", "Female", "Other"])

            contact = st.text_input("Contact Number")

            address = st.text_area("Address")

        

        submitted = st.form_submit_button("Register Patient")

        

        if submitted:

            if patient_id and name:

                # Check if patient ID already exists

                existing_ids = [p['patient_id'] for p in st.session_state.patients]

                if patient_id in existing_ids:

                    st.error(f"❌ Patient ID {patient_id} already exists!")

                else:

                    add_patient(patient_id, name, age, gender, contact, address)

                    st.success(f"✅ Patient {name} registered successfully!")

                    st.balloons()

            else:

                st.warning("Please fill all required fields")

    

    st.subheader("📋 Registered Patients")

    if st.session_state.patients:

        df_patients = pd.DataFrame(st.session_state.patients)

        st.dataframe(df_patients, use_container_width=True)

        

        # Export button

        csv = df_patients.to_csv(index=False)

        b64 = base64.b64encode(csv.encode()).decode()

        href = f'<a href="data:file/csv;base64,{b64}" download="patients_export.csv">📥 Export Patients to CSV</a>'

        st.markdown(href, unsafe_allow_html=True)

    else:

        st.info("No patients registered yet")



# ==================== VITALS LOGGER ====================

elif menu == "📊 Vitals Logger":

    st.header("🩺 Record Patient Vitals")

    

    if not st.session_state.patients:

        st.warning("Please register patients first!")

    else:

        patient_ids = [p['patient_id'] for p in st.session_state.patients]

        patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}

        

        with st.form("vitals_form"):

            selected_patient = st.selectbox("Select Patient", patient_ids, format_func=lambda x: f"{x} - {patient_names.get(x, '')}")

            col1, col2, col3 = st.columns(3)

            with col1:

                bp_sys = st.number_input("Systolic BP (mmHg)", min_value=50, max_value=250, value=120)

                bp_dia = st.number_input("Diastolic BP (mmHg)", min_value=30, max_value=150, value=80)

            with col2:

                heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=75)

                blood_sugar = st.number_input("Blood Sugar (mg/dL)", min_value=0, max_value=600, value=100)

            with col3:

                weight = st.number_input("Weight (kg)", min_value=0, max_value=300, value=70)

            notes = st.text_area("Additional Notes")

            

            submitted = st.form_submit_button("Save Vitals")

            

            if submitted:

                add_vitals(selected_patient, bp_sys, bp_dia, heart_rate, blood_sugar, weight, notes)

                st.success("✅ Vitals recorded successfully!")

    

    st.subheader("📋 Recent Vitals Records")

    if st.session_state.vitals:

        df_vitals = pd.DataFrame(st.session_state.vitals)

        patient_names_dict = {p['patient_id']: p['name'] for p in st.session_state.patients}

        df_vitals['patient_name'] = df_vitals['patient_id'].map(patient_names_dict)

        st.dataframe(df_vitals[['date', 'patient_id', 'patient_name', 'bp_systolic', 'bp_diastolic', 'heart_rate', 'blood_sugar']], use_container_width=True)

    else:

        st.info("No vitals recorded yet")



# ==================== MEDICATION MANAGER ====================

elif menu == "💊 Medication Manager":

    st.header("💊 Prescription & Medication Tracker")

    

    if not st.session_state.patients:

        st.warning("Please register patients first!")

    else:

        patient_ids = [p['patient_id'] for p in st.session_state.patients]

        patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}

        

        with st.form("medication_form"):

            selected_patient = st.selectbox("Select Patient", patient_ids, format_func=lambda x: f"{x} - {patient_names.get(x, '')}")

            med_name = st.text_input("Medication Name")

            dosage = st.text_input("Dosage (e.g., 500mg twice daily)")

            frequency = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "Weekly"])

            col1, col2 = st.columns(2)

            with col1:

                start_date = st.date_input("Start Date")

            with col2:

                end_date = st.date_input("End Date")

            

            submitted = st.form_submit_button("Add Prescription")

            

            if submitted and med_name:

                add_medication(selected_patient, med_name, dosage, frequency, str(start_date), str(end_date))

                st.success(f"✅ {med_name} prescribed successfully!")

        

        st.subheader("💊 Active Prescriptions")

        active_meds = [m for m in st.session_state.medications if m.get('status') == 'active']

        if active_meds:

            df_meds = pd.DataFrame(active_meds)

            df_meds['patient_name'] = df_meds['patient_id'].map(patient_names)

            st.dataframe(df_meds[['patient_id', 'patient_name', 'med_name', 'dosage', 'frequency', 'start_date', 'end_date']], use_container_width=True)

        else:

            st.info("No active prescriptions")



# ==================== APPOINTMENTS ====================

elif menu == "📅 Appointments":

    st.header("📅 Schedule Appointments")

    

    if not st.session_state.patients:

        st.warning("Please register patients first!")

    else:

        patient_ids = [p['patient_id'] for p in st.session_state.patients]

        patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}

        

        with st.form("appointment_form"):

            selected_patient = st.selectbox("Select Patient", patient_ids, format_func=lambda x: f"{x} - {patient_names.get(x, '')}")

            doctor = st.text_input("Doctor Name")

            appointment_date = st.datetime_input("Appointment Date & Time")

            reason = st.text_area("Reason for Visit")

            

            submitted = st.form_submit_button("Schedule Appointment")

            

            if submitted:

                add_appointment(selected_patient, doctor, str(appointment_date), reason)

                st.success(f"✅ Appointment scheduled for {appointment_date}")

        

        st.subheader("📋 Upcoming Appointments")

        if st.session_state.appointments:

            df_appointments = pd.DataFrame(st.session_state.appointments)

            df_appointments['patient_name'] = df_appointments['patient_id'].map(patient_names)

            st.dataframe(df_appointments[['date_time', 'patient_id', 'patient_name', 'doctor', 'reason', 'status']], use_container_width=True)

        else:

            st.info("No appointments scheduled")



# ==================== HEALTH ANALYTICS ====================

elif menu == "📈 Health Analytics":

    st.header("📊 Health Trends Analytics")

    

    if st.session_state.vitals:

        df = pd.DataFrame(st.session_state.vitals)

        df['date'] = pd.to_datetime(df['date'])

        df = df.sort_values('date')

        

        patient_ids = list(set([v['patient_id'] for v in st.session_state.vitals]))

        if patient_ids:

            patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}

            selected_patient = st.selectbox("Select Patient for Analytics", patient_ids, format_func=lambda x: f"{x} - {patient_names.get(x, '')}")

            df_patient = df[df['patient_id'] == selected_patient]

            

            if not df_patient.empty:

                st.subheader("❤️ Blood Pressure Trends")

                fig_bp = go.Figure()

                fig_bp.add_trace(go.Scatter(x=df_patient['date'], y=df_patient['bp_systolic'], name='Systolic', line=dict(color='red')))

                fig_bp.add_trace(go.Scatter(x=df_patient['date'], y=df_patient['bp_diastolic'], name='Diastolic', line=dict(color='blue')))

                fig_bp.update_layout(title="Blood Pressure Over Time", xaxis_title="Date", yaxis_title="mmHg")

                st.plotly_chart(fig_bp, use_container_width=True)

                

                col1, col2 = st.columns(2)

                with col1:

                    fig_hr = px.line(df_patient, x='date', y='heart_rate', title="Heart Rate Trend")

                    st.plotly_chart(fig_hr, use_container_width=True)

                with col2:

                    fig_sugar = px.line(df_patient, x='date', y='blood_sugar', title="Blood Sugar Trend")

                    st.plotly_chart(fig_sugar, use_container_width=True)

    else:

        st.warning("No vitals data available for analytics")



# ==================== REPORTS ====================

elif menu == "📄 Reports":

    st.header("📄 Generate Patient Health Reports")

    

    if not st.session_state.patients:

        st.warning("No patients registered")

    else:

        patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}

        selected_patient = st.selectbox("Select Patient", [p['patient_id'] for p in st.session_state.patients], format_func=lambda x: f"{x} - {patient_names.get(x, '')}")

        

        if st.button("📋 Generate Complete Health Report"):

            patient = next((p for p in st.session_state.patients if p['patient_id'] == selected_patient), None)

            patient_vitals = [v for v in st.session_state.vitals if v['patient_id'] == selected_patient]

            patient_meds = [m for m in st.session_state.medications if m['patient_id'] == selected_patient]

            

            report = f"""

            ========================================

            ICT IN HEALTH - PATIENT HEALTH REPORT

            ========================================

            

            PATIENT INFORMATION

            -------------------

            Patient ID: {selected_patient}

            Name: {patient.get('name', 'N/A')}

            Age: {patient.get('age', 'N/A')}

            Gender: {patient.get('gender', 'N/A')}

            Contact: {patient.get('contact', 'N/A')}

            Registration Date: {patient.get('registration_date', 'N/A')}

            

            VITAL SIGNS HISTORY

            -------------------

            """

            

            for v in patient_vitals[-5:]:

                report += f"""

            Date: {v['date']}

            - Blood Pressure: {v['bp_systolic']}/{v['bp_diastolic']} mmHg

            - Heart Rate: {v['heart_rate']} bpm

            - Blood Sugar: {v['blood_sugar']} mg/dL

            - Weight: {v['weight']} kg

            """

            

            report += f"""

            

            CURRENT MEDICATIONS

            -------------------

            """

            for m in patient_meds:

                report += f"""

            - {m['med_name']}: {m['dosage']} ({m['frequency']})

              Duration: {m['start_date']} to {m['end_date']}

            """

            

            report += f"""

            

            ========================================

            Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

            ========================================

            """

            

            st.text_area("Report Preview", report, height=400)

            

            b64 = base64.b64encode(report.encode()).decode()

            href = f'<a href="data:text/plain;base64,{b64}" download="patient_report_{selected_patient}.txt">📥 Download Report (TXT)</a>'

            st.markdown(href, unsafe_allow_html=True)

            

            st.success("✅ Report generated successfully!")



# ==================== BACKUP/RESTORE ====================

elif menu == "💾 Backup/Restore":

    st.header("💾 Backup & Restore Data")

    

    st.info("Your data is automatically saved to CSV files. Use this section to backup or restore.")

    

    col1, col2 = st.columns(2)

    

    with col1:

        st.subheader("📤 Backup Data")

        if st.button("Create Backup ZIP"):

            import zipfile

            import io

            

            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(zip_buffer, 'w') as zip_file:

                for file in os.listdir(DATA_FOLDER):

                    file_path = os.path.join(DATA_FOLDER, file)

                    zip_file.write(file_path, file)

            

            b64 = base64.b64encode(zip_buffer.getvalue()).decode()

            href = f'<a href="data:application/zip;base64,{b64}" download="hospital_data_backup.zip">📥 Download Backup ZIP</a>'

            st.markdown(href, unsafe_allow_html=True)

            st.success("Backup created!")

    

    with col2:

        st.subheader("📥 Restore Data")

        uploaded_file = st.file_uploader("Upload Backup ZIP", type=['zip'])

        if uploaded_file:

            import zipfile

            import io

            

            with zipfile.ZipFile(io.BytesIO(uploaded_file.read()), 'r') as zip_file:

                zip_file.extractall(DATA_FOLDER)

            

            st.session_state.patients = load_patients()

            st.session_state.vitals = load_vitals()

            st.session_state.medications = load_medications()

            st.session_state.appointments = load_appointments()

            

            st.success("✅ Data restored successfully! Refresh the page to see changes.")

            st.rerun()



# ==================== MENTAL HEALTH CHATBOT ====================

elif menu == "🧠 Mental Health Chatbot":

    chatbot_ui()



# ==================== ABOUT ====================

elif menu == "ℹ️ About ICT in Health":

    st.header("🌐 Information & Communication Technology (ICT) in Health")

    

    st.markdown("""

    ### What is ICT in Health?

    

    ICT in Health (eHealth/Digital Health) uses technology for health-related purposes.

    

    ### Persistent Storage Features:

    - ✅ **Data never disappears** - Saved to CSV files

    - ✅ **Backup & Restore** - Export/Import your data

    - ✅ **Works on Streamlit Cloud** - Files persist between sessions

    - ✅ **No external database needed** - Everything works out of the box

    

    ### Technologies Used:

    - Streamlit (Frontend)

    - CSV Files (Storage)

    - Plotly (Charts)

    - Pandas (Data manipulation)

    - Google Gemini AI (Mental Health Chatbot)

    """)



st.sidebar.markdown("---")

st.sidebar.success(f"✅ Data is PERSISTENT!\n\nYour data is saved to CSV files. Close and reopen - data stays!")



chatbot.py file is this::"""

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

now i dont want thesse basic fewer headache features in chatbot i want if patient ask questions it recommend to google gemini and it tellss check sysmptoms tells exercise gave all educational information about health and lifestyle changing advice and all that 
