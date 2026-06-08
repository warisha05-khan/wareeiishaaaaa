"""
ICT in Health - Hospital Management System
With Patient Self-Registration + Admin Manual Entry + Doctor Patient Management
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, time as dt_time, date, timedelta
import os
import base64
import hashlib
import json
import random

# Import chatbot module
from chatbot import chatbot_ui

# Page configuration
st.set_page_config(
    page_title="ICT Health | Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS FOR BEAUTIFUL SIDEBAR ====================

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2b1f 0%, #1a4a2a 50%, #0f2b1f 100%);
        padding-top: 20px;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }

    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] > div:last-child {
        background: #0f2b1f !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.18) !important;
        border-color: #ffd700 !important;
        transform: translateX(4px) !important;
    }

    [data-testid="stSidebar"] .stButton > button:focus {
        background: linear-gradient(135deg, #2d8c5a, #1f6e4a) !important;
        border-left: 3px solid #ffd700 !important;
        box-shadow: none !important;
    }
    
    .sidebar-header {
        text-align: center;
        padding: 20px 15px;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        margin-bottom: 20px;
    }
    
    .sidebar-header h1 {
        color: white;
        font-size: 1.5rem;
        margin-bottom: 5px;
    }
    
    .sidebar-header p {
        color: #a0c4b0;
        font-size: 0.7rem;
    }
    
    .user-card {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 15px;
        margin: 15px 10px;
        text-align: center;
    }
    
    .user-card h4 {
        color: white;
        margin-bottom: 5px;
    }
    
    .user-card p {
        color: #c0e0d0;
        font-size: 0.8rem;
    }
    
    .stat-card {
        background: rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 10px;
        margin: 8px 10px;
        text-align: center;
        border-left: 3px solid #ffd700;
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ffd700;
    }
    
    .stat-label {
        font-size: 0.7rem;
        color: #c0e0d0;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1f6e4a 0%, #0f533a 100%);
        padding: 20px 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        color: white;
    }
    
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f6e4a;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #666;
    }

    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255,255,255,0.1) !important;
        color: white !important;
        border-color: rgba(255,255,255,0.2) !important;
    }

    [data-testid="stSidebar"] .stSuccess,
    [data-testid="stSidebar"] .stInfo {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        border-radius: 10px;
    }

    [data-testid="stSidebar"] footer {
        display: none !important;
    }
    
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: bold;
    }
    .status-pending { background: #fef3c7; color: #d97706; }
    .status-accepted { background: #d1fae5; color: #059669; }
    .status-declined { background: #fee2e2; color: #dc2626; }
    
    .pending-approval {
        background: #fef3c7;
        border-left: 5px solid #f59e0b;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 15px 0;
    }
    
    .pending-box {
        background: #fef3c7;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 15px 0;
        border-left: 5px solid #f59e0b;
    }
    
    .medical-note {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 0.85rem;
    }
    
    .follow-up {
        background: #e0f2fe;
        border-left: 4px solid #0284c7;
        padding: 12px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ==================== AUTHENTICATION ====================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("12345")

# Doctor credentials
DOCTORS = {
    "cardiologist": {
        "name": "Dr. Sarah Ahmed", 
        "password_hash": hash_password("cardiologist"), 
        "specialty": "Cardiologist", 
        "available": True
    },
    "general physician": {
        "name": "Dr. Ali Raza", 
        "password_hash": hash_password("general physician"), 
        "specialty": "General Physician", 
        "available": True
    },
    "neurologist": {
        "name": "Dr. Fatima Khan", 
        "password_hash": hash_password("neurologist"), 
        "specialty": "Neurologist", 
        "available": True
    }
}

def init_auth():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'current_patient_id' not in st.session_state:
        st.session_state.current_patient_id = None
    if 'current_patient_name' not in st.session_state:
        st.session_state.current_patient_name = None
    if 'selected_menu' not in st.session_state:
        st.session_state.selected_menu = "📊 Dashboard"

init_auth()

def login_admin(username, password):
    return username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH

def login_doctor(username, password):
    username_lower = username.lower()
    for doc_key in DOCTORS.keys():
        if doc_key.lower() == username_lower and DOCTORS[doc_key]["password_hash"] == hash_password(password):
            return True, DOCTORS[doc_key]["name"], doc_key
    return False, None, None

def verify_patient(patient_id, patient_name):
    patients = st.session_state.patients
    for patient in patients:
        if patient['patient_id'] == patient_id and patient['name'].lower() == patient_name.lower() and patient.get('active', True):
            return True, patient['name']
    return False, None

# ==================== REGISTRATION REQUESTS FUNCTIONS ====================

REQUESTS_FILE = os.path.join("hospital_data", "registration_requests.json")
PATIENT_NOTES_FILE = os.path.join("hospital_data", "patient_notes.json")
DOCTOR_MEDICATIONS_FILE = os.path.join("hospital_data", "doctor_medications.json")
FOLLOWUP_FILE = os.path.join("hospital_data", "followups.json")

def save_requests():
    with open(REQUESTS_FILE, 'w') as f:
        json.dump(st.session_state.registration_requests, f, indent=2)

def load_requests():
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE, 'r') as f:
            st.session_state.registration_requests = json.load(f)
    else:
        st.session_state.registration_requests = []

def add_registration_request(name, age, gender, contact, address, reason):
    request = {
        'id': len(st.session_state.registration_requests) + 1,
        'name': name,
        'age': age,
        'gender': gender,
        'contact': contact,
        'address': address,
        'reason': reason,
        'status': 'pending',
        'submitted_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'assigned_id': None,
        'source': 'online'
    }
    st.session_state.registration_requests.append(request)
    save_requests()
    return True

def add_manual_patient(name, age, gender, contact, address, reason, refer_to_doctor):
    """Admin manually adds a patient directly without approval"""
    patient_id = generate_unique_id()
    add_patient(patient_id, name, age, gender, contact, address)
    
    # Also create a registration request record
    request = {
        'id': len(st.session_state.registration_requests) + 1,
        'name': name,
        'age': age,
        'gender': gender,
        'contact': contact,
        'address': address,
        'reason': reason,
        'status': 'approved',
        'submitted_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'assigned_id': patient_id,
        'source': 'manual'
    }
    st.session_state.registration_requests.append(request)
    save_requests()
    
    # If refer_to_doctor is selected, create an appointment request
    if refer_to_doctor and refer_to_doctor != "None":
        doctor_info = DOCTORS.get(refer_to_doctor, {})
        if doctor_info:
            appointment_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
            add_appointment(patient_id, refer_to_doctor, doctor_info["name"], appointment_date, reason)
    
    return patient_id

def approve_request(request_id, patient_id):
    for req in st.session_state.registration_requests:
        if req['id'] == request_id:
            req['status'] = 'approved'
            req['assigned_id'] = patient_id
            req['approved_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Add to patients list
            add_patient(patient_id, req['name'], req['age'], req['gender'], req['contact'], req['address'])
            break
    save_requests()

def reject_request(request_id):
    for req in st.session_state.registration_requests:
        if req['id'] == request_id:
            req['status'] = 'rejected'
            break
    save_requests()

# ==================== DOCTOR NOTES FUNCTIONS ====================

def save_patient_notes():
    if 'patient_notes' not in st.session_state:
        st.session_state.patient_notes = []
    with open(PATIENT_NOTES_FILE, 'w') as f:
        json.dump(st.session_state.patient_notes, f, indent=2)

def load_patient_notes():
    if os.path.exists(PATIENT_NOTES_FILE):
        with open(PATIENT_NOTES_FILE, 'r') as f:
            st.session_state.patient_notes = json.load(f)
    else:
        st.session_state.patient_notes = []

def add_patient_note(patient_id, doctor_username, doctor_name, note):
    new_note = {
        'id': len(st.session_state.patient_notes) + 1,
        'patient_id': patient_id,
        'doctor_username': doctor_username,
        'doctor_name': doctor_name,
        'note': note,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.patient_notes.append(new_note)
    save_patient_notes()

def get_patient_notes(patient_id):
    return [n for n in st.session_state.patient_notes if n['patient_id'] == patient_id]

def save_doctor_medications():
    if 'doctor_medications' not in st.session_state:
        st.session_state.doctor_medications = []
    with open(DOCTOR_MEDICATIONS_FILE, 'w') as f:
        json.dump(st.session_state.doctor_medications, f, indent=2)

def load_doctor_medications():
    if os.path.exists(DOCTOR_MEDICATIONS_FILE):
        with open(DOCTOR_MEDICATIONS_FILE, 'r') as f:
            st.session_state.doctor_medications = json.load(f)
    else:
        st.session_state.doctor_medications = []

def add_doctor_medication(patient_id, doctor_username, doctor_name, med_name, dosage, frequency, duration, instructions):
    new_med = {
        'id': len(st.session_state.doctor_medications) + 1,
        'patient_id': patient_id,
        'doctor_username': doctor_username,
        'doctor_name': doctor_name,
        'med_name': med_name,
        'dosage': dosage,
        'frequency': frequency,
        'duration': duration,
        'instructions': instructions,
        'prescribed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'active'
    }
    st.session_state.doctor_medications.append(new_med)
    save_doctor_medications()

def get_doctor_medications(patient_id):
    return [m for m in st.session_state.doctor_medications if m['patient_id'] == patient_id]

def save_followups():
    if 'followups' not in st.session_state:
        st.session_state.followups = []
    with open(FOLLOWUP_FILE, 'w') as f:
        json.dump(st.session_state.followups, f, indent=2)

def load_followups():
    if os.path.exists(FOLLOWUP_FILE):
        with open(FOLLOWUP_FILE, 'r') as f:
            st.session_state.followups = json.load(f)
    else:
        st.session_state.followups = []

def add_followup(patient_id, doctor_username, doctor_name, advice, followup_date):
    new_followup = {
        'id': len(st.session_state.followups) + 1,
        'patient_id': patient_id,
        'doctor_username': doctor_username,
        'doctor_name': doctor_name,
        'advice': advice,
        'followup_date': followup_date,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'status': 'scheduled'
    }
    st.session_state.followups.append(new_followup)
    save_followups()

def get_followups(patient_id):
    return [f for f in st.session_state.followups if f['patient_id'] == patient_id]

# ==================== FILE STORAGE FUNCTIONS ====================

DATA_FOLDER = "hospital_data"
os.makedirs(DATA_FOLDER, exist_ok=True)

PATIENTS_FILE = os.path.join(DATA_FOLDER, "patients.csv")
VITALS_FILE = os.path.join(DATA_FOLDER, "vitals.csv")
MEDICATIONS_FILE = os.path.join(DATA_FOLDER, "medications.csv")
APPOINTMENTS_FILE = os.path.join(DATA_FOLDER, "appointments.csv")

def load_patients():
    if os.path.exists(PATIENTS_FILE):
        df = pd.read_csv(PATIENTS_FILE)
        return df.to_dict('records')
    return []

def save_patients(patients):
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
load_requests()
load_patient_notes()
load_doctor_medications()
load_followups()

# ==================== HELPER FUNCTIONS ====================

def add_patient(patient_id, name, age, gender, contact, address):
    existing_ids = [p['patient_id'] for p in st.session_state.patients]
    if patient_id in existing_ids:
        patient_id = generate_unique_id()
    
    new_patient = {
        'patient_id': patient_id,
        'name': name,
        'age': age,
        'gender': gender,
        'contact': contact,
        'address': address,
        'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'active': True
    }
    st.session_state.patients.append(new_patient)
    save_patients(st.session_state.patients)
    return patient_id

def generate_unique_id():
    existing_ids = [p['patient_id'] for p in st.session_state.patients]
    prefix = "PAT"
    counter = 1
    while f"{prefix}{counter:03d}" in existing_ids:
        counter += 1
    return f"{prefix}{counter:03d}"

def update_patient(patient_id, name, age, gender, contact, address):
    for i, p in enumerate(st.session_state.patients):
        if p['patient_id'] == patient_id:
            st.session_state.patients[i].update({
                'name': name, 'age': age, 'gender': gender, 
                'contact': contact, 'address': address,
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            break
    save_patients(st.session_state.patients)

def delete_patient(patient_id):
    st.session_state.patients = [p for p in st.session_state.patients if p['patient_id'] != patient_id]
    st.session_state.vitals = [v for v in st.session_state.vitals if v['patient_id'] != patient_id]
    st.session_state.medications = [m for m in st.session_state.medications if m['patient_id'] != patient_id]
    st.session_state.appointments = [a for a in st.session_state.appointments if a['patient_id'] != patient_id]
    st.session_state.patient_notes = [n for n in st.session_state.patient_notes if n['patient_id'] != patient_id]
    st.session_state.doctor_medications = [m for m in st.session_state.doctor_medications if m['patient_id'] != patient_id]
    st.session_state.followups = [f for f in st.session_state.followups if f['patient_id'] != patient_id]
    save_patients(st.session_state.patients)
    save_vitals(st.session_state.vitals)
    save_medications(st.session_state.medications)
    save_appointments(st.session_state.appointments)
    save_patient_notes()
    save_doctor_medications()
    save_followups()

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

def add_appointment(patient_id, doctor_username, doctor_name, appointment_date, reason):
    new_appointment = {
        'id': len(st.session_state.appointments) + 1,
        'patient_id': patient_id,
        'doctor_username': doctor_username,
        'doctor_name': doctor_name,
        'date_time': appointment_date,
        'reason': reason,
        'status': 'pending',
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.appointments.append(new_appointment)
    save_appointments(st.session_state.appointments)

def update_appointment_status(appointment_id, status):
    for a in st.session_state.appointments:
        if a.get('id') == appointment_id:
            a['status'] = status
            a['responded_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    save_appointments(st.session_state.appointments)

def delete_appointment(appointment_id):
    st.session_state.appointments = [a for a in st.session_state.appointments if a.get('id') != appointment_id]
    save_appointments(st.session_state.appointments)

def get_patient_data(patient_id):
    patient_vitals = [v for v in st.session_state.vitals if v['patient_id'] == patient_id]
    patient_meds = [m for m in st.session_state.medications if m['patient_id'] == patient_id]
    patient_appointments = [a for a in st.session_state.appointments if a['patient_id'] == patient_id]
    return patient_vitals, patient_meds, patient_appointments

def get_patient_by_id(patient_id):
    for p in st.session_state.patients:
        if p['patient_id'] == patient_id:
            return p
    return None

def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.current_user = None
    st.session_state.current_patient_id = None
    st.session_state.current_patient_name = None
    st.session_state.selected_menu = "📊 Dashboard"
    st.rerun()

# ==================== LOGIN UI ====================

def show_login_page():
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1f6e4a 0%, #0f533a 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 12px;
        border-radius: 30px;
    }
    .stButton > button:hover {
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1f6e4a 0%, #0f533a 100%); 
                    border-radius: 20px; padding: 40px; text-align: center; margin-bottom: 30px;">
            <h1 style="color: white; margin-bottom: 10px;">🏥 ICT Health</h1>
            <p style="color: #e0e0e0;">Hospital Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["👨‍💼 Admin Login", "👨‍⚕️ Doctor Login", "👤 Patient Login", "📝 New Registration", "🔍 Check Status"])
        
        with tab1:
            admin_username = st.text_input("Username", key="admin_user", placeholder="admin")
            admin_password = st.text_input("Password", type="password", key="admin_pass", placeholder="•••••")
            if st.button("🔐 Login as Admin", key="admin_login"):
                if login_admin(admin_username, admin_password):
                    st.session_state.logged_in = True
                    st.session_state.user_type = "admin"
                    st.session_state.current_user = "admin"
                    st.rerun()
                else:
                    st.error("❌ Invalid admin credentials!")
        
        with tab2:
            st.info("👨‍⚕️ Doctor Login\n\n• Cardiologist → Username: `cardiologist` | Password: `cardiologist`\n• General Physician → Username: `general physician` | Password: `general physician`\n• Neurologist → Username: `neurologist` | Password: `neurologist`")
            doctor_username = st.text_input("Doctor Username", key="doctor_user", placeholder="cardiologist / general physician / neurologist")
            doctor_password = st.text_input("Password", type="password", key="doctor_pass", placeholder="•••••")
            if st.button("🔐 Login as Doctor", key="doctor_login"):
                valid, name, doc_key = login_doctor(doctor_username, doctor_password)
                if valid:
                    st.session_state.logged_in = True
                    st.session_state.user_type = "doctor"
                    st.session_state.current_user = doc_key
                    st.session_state.current_user_name = name
                    st.rerun()
                else:
                    st.error("❌ Invalid doctor credentials!")
        
        with tab3:
            st.info("🔐 Patient Login - Use the Patient ID provided after admin approval")
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.text_input("Patient ID", key="patient_id", placeholder="e.g., PAT001")
            with col2:
                patient_name = st.text_input("Full Name", key="patient_name", placeholder="Your registered name")
            if st.button("🔐 Access My Portal", key="patient_login"):
                if patient_id and patient_name:
                    valid, name = verify_patient(patient_id, patient_name)
                    if valid:
                        st.session_state.logged_in = True
                        st.session_state.user_type = "patient"
                        st.session_state.current_patient_id = patient_id
                        st.session_state.current_patient_name = name
                        st.rerun()
                    else:
                        st.error("❌ Invalid Patient ID or Name! Please wait for admin approval.")
                else:
                    st.warning("⚠️ Please enter both fields")
        
        with tab4:
            st.header("📝 Patient Self Registration")
            st.info("Register yourself online. After admin approval, you will receive a Patient ID.")
            
            with st.form("self_registration_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("Full Name*")
                    age = st.number_input("Age*", min_value=0, max_value=150)
                    gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
                with col2:
                    contact = st.text_input("Contact Number*", placeholder="e.g., 03001234567")
                    address = st.text_area("Address*")
                reason = st.text_area("Reason for Registration / Any Health Concerns", height=100, 
                                     placeholder="Please describe any health concerns or reason for registration...")
                
                st.warning("⚠️ Your registration will be reviewed by admin. You will receive your Patient ID via the 'Check Status' tab after approval.")
                
                submitted = st.form_submit_button("Submit Registration Request")
                
                if submitted:
                    if name and age and contact and address:
                        add_registration_request(name, age, gender, contact, address, reason)
                        st.success("✅ Registration request submitted successfully!")
                        st.info("📌 Please go to the 'Check Status' tab to see your approval status and Patient ID once approved.")
                        st.balloons()
                    else:
                        st.warning("Please fill all required fields (*)")
        
        with tab5:
            st.header("🔍 Check Your Registration Status")
            st.info("Enter your registered name and contact number to check your approval status and get your Patient ID.")
            
            col1, col2 = st.columns(2)
            with col1:
                check_name = st.text_input("Enter your Full Name", key="check_name", placeholder="Enter the name you registered with")
            with col2:
                check_contact = st.text_input("Enter your Contact Number", key="check_contact", placeholder="Enter your registered contact number")
            
            if st.button("🔍 Check Status", key="check_status", use_container_width=True):
                if check_name and check_contact:
                    matching_requests = [r for r in st.session_state.registration_requests 
                                        if r['name'].lower() == check_name.lower() and r['contact'] == check_contact]
                    
                    if matching_requests:
                        latest_request = matching_requests[-1]
                        
                        if latest_request['status'] == 'approved':
                            st.balloons()
                            st.markdown(f"""
                            <div class="success-box">
                                <h2 style="color: #059669;">✅ Registration Approved!</h2>
                                <hr>
                                <p style="font-size: 1.1rem;">Your Patient ID is:</p>
                                <h1 style="color: #059669; font-size: 3rem; font-weight: bold;">{latest_request['assigned_id']}</h1>
                                <div style="background: white; padding: 15px; border-radius: 10px; margin-top: 15px;">
                                    <p><strong>📝 Login Credentials:</strong></p>
                                    <p>🔐 Patient ID: <code>{latest_request['assigned_id']}</code></p>
                                    <p>🔐 Password/Name: <code>{latest_request['name']}</code></p>
                                    <hr>
                                    <p>✅ Use these credentials to login to your patient portal.</p>
                                    <p>📅 You can now schedule appointments and access your health records.</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            creds = f"Patient ID: {latest_request['assigned_id']}\nName: {latest_request['name']}\nContact: {latest_request['contact']}\n\nPlease keep this information safe."
                            b64 = base64.b64encode(creds.encode()).decode()
                            st.markdown(f'<a href="data:text/plain;base64,{b64}" download="my_credentials.txt">📥 Download My Credentials</a>', unsafe_allow_html=True)
                            
                            st.info(f"📱 A notification has been sent to your registered number: {latest_request['contact']} (Simulated)")
                            
                        elif latest_request['status'] == 'rejected':
                            st.error(f"❌ Sorry, your registration request was rejected.")
                            st.markdown("""
                            <div style="background: #fee2e2; padding: 15px; border-radius: 10px; margin-top: 10px;">
                                <p>💡 You can submit a new registration request using the 'New Registration' tab.</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        else:
                            st.markdown(f"""
                            <div class="pending-box">
                                <h3 style="color: #d97706;">⏳ Pending Approval</h3>
                                <p>Your registration is still under review.</p>
                                <p><strong>📅 Submitted on:</strong> {latest_request['submitted_date']}</p>
                                <p>📌 Please check back later. Admin will review your request soon.</p>
                                <progress value="50" max="100" style="width: 100%; height: 10px; border-radius: 5px;"></progress>
                                <p style="color: #666;">Status: Under Review</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                    else:
                        st.error(f"❌ No registration found with name '{check_name}' and contact number '{check_contact}'. Please register first using the 'New Registration' tab.")
                else:
                    st.warning("⚠️ Please enter both your name and contact number")
            
            st.markdown("---")
            st.caption("💡 **Note:** After admin approves your registration, your Patient ID will appear here. Save it for future logins.")
        
        st.markdown("---")
        st.markdown("<center><small>© 2026 ICT Health | Secure Hospital Management System</small></center>", unsafe_allow_html=True)

# ==================== SIDEBAR NAVIGATION ====================

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h1>🏥 ICT Health</h1>
            <p>Hospital Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.user_type == "admin":
            st.markdown("""
            <div class="user-card">
                <h4>👨‍💼 Admin</h4>
                <p>Full Access</p>
            </div>
            """, unsafe_allow_html=True)
            
            pending_requests = len([r for r in st.session_state.registration_requests if r['status'] == 'pending' and r.get('source') != 'manual'])
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(st.session_state.patients)}</div>
                <div class="stat-label">Total Patients</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{pending_requests}</div>
                <div class="stat-label">Pending Approvals</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([a for a in st.session_state.appointments if a['status'] == 'pending'])}</div>
                <div class="stat-label">Pending Appointments</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 20px 0 10px 15px; color: #ffd700; font-size: 0.8rem;'>📋 MAIN MENU</div>", unsafe_allow_html=True)
            
            menu_items = [
                "📊 Dashboard", "👨‍👩‍👧 Patient Management",
                "🩺 Record Vitals", "💊 Medications", "📅 Appointments",
                "📈 Analytics", "📄 Reports", "💾 Backup/Restore", "🤖 AI Assistant", "ℹ️ About"
            ]
            
        elif st.session_state.user_type == "doctor":
            doctor_info = DOCTORS.get(st.session_state.current_user, {})
            st.markdown(f"""
            <div class="user-card">
                <h4>👨‍⚕️ {doctor_info.get('name', st.session_state.current_user)}</h4>
                <p>{doctor_info.get('specialty', 'Doctor')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            pending_count = len([a for a in st.session_state.appointments if a.get('doctor_username') == st.session_state.current_user and a['status'] == 'pending'])
            accepted_count = len([a for a in st.session_state.appointments if a.get('doctor_username') == st.session_state.current_user and a['status'] == 'accepted'])
            
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{pending_count}</div>
                <div class="stat-label">Pending Requests</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{accepted_count}</div>
                <div class="stat-label">Accepted Appointments</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 20px 0 10px 15px; color: #ffd700; font-size: 0.8rem;'>📋 DOCTOR PORTAL</div>", unsafe_allow_html=True)
            
            menu_items = [
                "📊 Doctor Dashboard", "📅 Appointment Requests", "✅ My Appointments",
                "👥 My Patients", "🤖 AI Assistant", "ℹ️ About"
            ]
            
        else:
            patient_vitals, patient_meds, _ = get_patient_data(st.session_state.current_patient_id)
            st.markdown(f"""
            <div class="user-card">
                <h4>👤 {st.session_state.current_patient_name}</h4>
                <p>ID: {st.session_state.current_patient_id}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(patient_vitals)}</div>
                <div class="stat-label">Your Vitals</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(patient_meds)}</div>
                <div class="stat-label">Your Medications</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 20px 0 10px 15px; color: #ffd700; font-size: 0.8rem;'>📋 YOUR PORTAL</div>", unsafe_allow_html=True)
            
            menu_items = [
                "📊 My Dashboard", "🩺 My Vitals", "💊 My Medications",
                "📅 My Appointments", "📈 My Analytics", "📄 My Reports",
                "🤖 AI Assistant", "ℹ️ About"
            ]
        
        for item in menu_items:
            if st.button(item, key=f"sidebar_{item}", use_container_width=True):
                st.session_state.selected_menu = item
                st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Logout", key="sidebar_logout", use_container_width=True):
            logout()
        
        st.markdown("""
        <div style="text-align: center; padding: 20px 10px; margin-top: 20px;">
            <small style="color: #a0c4b0;">© 2026 ICT Health<br>Secure Hospital System</small>
        </div>
        """, unsafe_allow_html=True)

# ==================== PATIENT MANAGEMENT (ADMIN) ====================

def show_patient_management():
    st.header("📝 Patient Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Pending Approvals", "➕ Register Patient", "✏️ Edit Patient", "🗑️ Delete Patient"])
    
    # Tab 1: Pending Approvals
    with tab1:
        st.subheader("📋 Pending Online Registrations")
        pending_requests = [r for r in st.session_state.registration_requests if r['status'] == 'pending' and r.get('source') != 'manual']
        
        if not pending_requests:
            st.info("No pending registration requests.")
        else:
            for req in pending_requests:
                with st.container():
                    st.markdown(f"""
                    <div class="pending-approval">
                        <strong>📅 Submitted:</strong> {req['submitted_date']}<br>
                        <strong>👤 Name:</strong> {req['name']}<br>
                        <strong>🎂 Age:</strong> {req['age']} | <strong>⚧ Gender:</strong> {req['gender']}<br>
                        <strong>📞 Contact:</strong> {req['contact']}<br>
                        <strong>📍 Address:</strong> {req['address']}<br>
                        <strong>📝 Reason for Registration:</strong> {req['reason'] if req['reason'] else 'Not specified'}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        suggested_id = generate_unique_id()
                        patient_id = st.text_input(f"Patient ID for {req['name']}", value=suggested_id, key=f"id_{req['id']}")
                    
                    with col2:
                        if st.button("✅ Approve", key=f"approve_{req['id']}"):
                            approve_request(req['id'], patient_id)
                            st.success(f"✅ Patient {req['name']} approved! Patient ID: {patient_id}")
                            st.info(f"📌 Patient can now login using ID: {patient_id} and Name: {req['name']}")
                            st.rerun()
                    
                    with col3:
                        if st.button("❌ Reject", key=f"reject_{req['id']}"):
                            reject_request(req['id'])
                            st.warning(f"❌ Registration request from {req['name']} rejected")
                            st.rerun()
                    
                    st.markdown("---")
    
    # Tab 2: Register Patient (Manual)
    with tab2:
        st.subheader("➕ Register New Patient & Refer to Doctor")
        st.info("Register a walk-in patient and refer them to an available doctor.")
        
        with st.form("manual_patient_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*")
                age = st.number_input("Age*", min_value=0, max_value=150)
                gender = st.selectbox("Gender*", ["Male", "Female", "Other"])
            with col2:
                contact = st.text_input("Contact Number*")
                address = st.text_area("Address*")
            reason = st.text_area("Reason for Visit / Initial Complaint", height=80)
            
            # Doctor referral section
            st.markdown("---")
            st.markdown("### 👨‍⚕️ Refer to Doctor")
            doctor_options = {username: f"{info['name']} ({info['specialty']})" for username, info in DOCTORS.items()}
            doctor_options["None"] = "No referral needed"
            selected_doctor = st.selectbox("Select Doctor to Refer", list(doctor_options.keys()), format_func=lambda x: doctor_options[x])
            
            submitted = st.form_submit_button("Register & Refer Patient")
            
            if submitted:
                if name and age and contact and address:
                    refer_doctor = None if selected_doctor == "None" else selected_doctor
                    patient_id = add_manual_patient(name, age, gender, contact, address, reason, refer_doctor)
                    st.success(f"✅ Patient {name} registered successfully!")
                    st.info(f"📌 Patient ID: {patient_id}")
                    st.info(f"🔐 Patient can login using ID: {patient_id} and Name: {name}")
                    
                    if refer_doctor:
                        st.success(f"📅 Appointment request sent to {DOCTORS[refer_doctor]['name']} for tomorrow")
                    st.balloons()
                else:
                    st.warning("Please fill all required fields (*)")
    
    # Tab 3: Edit Patient
    with tab3:
        st.subheader("✏️ Edit Patient Information")
        patients = {p['patient_id']: p['name'] for p in st.session_state.patients if p.get('active', True)}
        if patients:
            selected_patient = st.selectbox("Select Patient to Edit", list(patients.keys()), format_func=lambda x: f"{x} - {patients[x]}")
            patient_data = get_patient_by_id(selected_patient)
            if patient_data:
                with st.form("edit_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Full Name", value=patient_data['name'])
                        age = st.number_input("Age", min_value=0, max_value=150, value=patient_data['age'])
                    with col2:
                        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(patient_data['gender']))
                        contact = st.text_input("Contact", value=patient_data.get('contact', ''))
                        address = st.text_area("Address", value=patient_data.get('address', ''))
                    if st.form_submit_button("Update Patient"):
                        update_patient(selected_patient, name, age, gender, contact, address)
                        st.success("✅ Patient updated successfully!")
                        st.rerun()
        else:
            st.info("No patients registered")
    
    # Tab 4: Delete Patient
    with tab4:
        st.subheader("🗑️ Delete Patient")
        patients = {p['patient_id']: p['name'] for p in st.session_state.patients if p.get('active', True)}
        if patients:
            selected_patient = st.selectbox("Select Patient to Delete", list(patients.keys()), format_func=lambda x: f"{x} - {patients[x]}")
            if st.button("🗑️ Permanently Delete Patient", use_container_width=True):
                if st.checkbox("I understand this action cannot be undone"):
                    delete_patient(selected_patient)
                    st.success(f"✅ Patient {selected_patient} deleted successfully!")
                    st.rerun()
                else:
                    st.warning("Please confirm deletion")
        else:
            st.info("No patients registered")

# ==================== DOCTOR MY PATIENTS DETAILS ====================

def show_doctor_patient_details(patient_id, patient_name, doctor_username, doctor_name):
    """Show detailed view of a single patient for doctor with edit capabilities"""
    
    st.subheader(f"👤 Patient: {patient_name} (ID: {patient_id})")
    
    # Tabs for different sections
    tabs = st.tabs(["📋 Patient Info", "🩺 Vitals History", "💊 Prescribe Medication", "📝 Medical Notes", "📅 Follow-up Advice", "💊 Prescribed Medications"])
    
    with tabs[0]:
        patient = get_patient_by_id(patient_id)
        if patient:
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 15px; border-radius: 10px;">
                <p><strong>📛 Name:</strong> {patient['name']}</p>
                <p><strong>🎂 Age:</strong> {patient['age']}</p>
                <p><strong>⚧ Gender:</strong> {patient['gender']}</p>
                <p><strong>📞 Contact:</strong> {patient.get('contact', 'N/A')}</p>
                <p><strong>📍 Address:</strong> {patient.get('address', 'N/A')}</p>
                <p><strong>📅 Registered:</strong> {patient.get('registration_date', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tabs[1]:
        patient_vitals = [v for v in st.session_state.vitals if v['patient_id'] == patient_id]
        if patient_vitals:
            df = pd.DataFrame(patient_vitals)
            st.dataframe(df[['date', 'bp_systolic', 'bp_diastolic', 'heart_rate', 'blood_sugar', 'weight', 'notes']], use_container_width=True)
        else:
            st.info("No vitals recorded for this patient yet.")
    
    with tabs[2]:
        st.markdown("### 💊 Prescribe New Medication")
        with st.form("doctor_prescribe_form"):
            col1, col2 = st.columns(2)
            with col1:
                med_name = st.text_input("Medication Name*")
                dosage = st.text_input("Dosage*", placeholder="e.g., 500mg")
                frequency = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily", "Weekly"])
            with col2:
                duration = st.text_input("Duration", placeholder="e.g., 7 days, 1 month")
                instructions = st.text_area("Special Instructions", placeholder="e.g., Take with food, after meal")
            
            submitted = st.form_submit_button("💊 Prescribe Medication")
            
            if submitted and med_name and dosage:
                add_doctor_medication(patient_id, doctor_username, doctor_name, med_name, dosage, frequency, duration, instructions)
                st.success(f"✅ {med_name} prescribed to {patient_name}!")
                st.rerun()
            elif submitted:
                st.warning("Please fill medication name and dosage")
    
    with tabs[3]:
        st.markdown("### 📝 Add Medical Note")
        with st.form("doctor_note_form"):
            note = st.text_area("Medical Note / Clinical Notes", height=150, 
                               placeholder="e.g., Patient presented with... Examination findings... Diagnosis...")
            
            if st.form_submit_button("➕ Add Note"):
                if note:
                    add_patient_note(patient_id, doctor_username, doctor_name, note)
                    st.success("✅ Medical note added!")
                    st.rerun()
                else:
                    st.warning("Please enter a note")
        
        st.markdown("### 📋 Previous Medical Notes")
        patient_notes = get_patient_notes(patient_id)
        if patient_notes:
            for note in reversed(patient_notes[-10:]):
                st.markdown(f"""
                <div class="medical-note">
                    <strong>👨‍⚕️ {note['doctor_name']}</strong> | 📅 {note['created_at']}<br>
                    📝 {note['note']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No medical notes yet.")
    
    with tabs[4]:
        st.markdown("### 📅 Add Follow-up Advice")
        with st.form("followup_form"):
            advice = st.text_area("Follow-up Advice / Instructions", height=100,
                                  placeholder="e.g., Come back after 2 weeks for review, Get blood tests done...")
            followup_date = st.date_input("Suggested Follow-up Date")
            
            if st.form_submit_button("➕ Add Follow-up"):
                if advice:
                    add_followup(patient_id, doctor_username, doctor_name, advice, followup_date.strftime("%Y-%m-%d"))
                    st.success("✅ Follow-up advice added!")
                    st.rerun()
                else:
                    st.warning("Please enter advice")
        
        st.markdown("### 📋 Previous Follow-ups")
        followups = get_followups(patient_id)
        if followups:
            for fup in reversed(followups[-10:]):
                st.markdown(f"""
                <div class="follow-up">
                    <strong>👨‍⚕️ {fup['doctor_name']}</strong> | 📅 Added: {fup['created_at']}<br>
                    <strong>📌 Advice:</strong> {fup['advice']}<br>
                    <strong>📅 Follow-up Date:</strong> {fup['followup_date']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No follow-up advice yet.")
    
    with tabs[5]:
        st.markdown("### 💊 Prescribed Medications")
        doctor_meds = get_doctor_medications(patient_id)
        if doctor_meds:
            for med in reversed(doctor_meds):
                st.markdown(f"""
                <div style="background: #fef3c7; padding: 12px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #f59e0b;">
                    <strong>💊 {med['med_name']}</strong> | {med['dosage']} | {med['frequency']}<br>
                    <strong>📋 By:</strong> {med['doctor_name']} | 📅 {med['prescribed_at']}<br>
                    <strong>📝 Instructions:</strong> {med['instructions'] if med['instructions'] else 'None'}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No medications prescribed by doctors yet.")

# ==================== ADMIN DASHBOARD ====================

def show_admin_dashboard():
    render_sidebar()
    
    st.markdown('<div class="main-header"><h2>🏥 ICT Health - Admin Dashboard</h2><p>Complete Patient Data Access</p></div>', unsafe_allow_html=True)
    
    menu = st.session_state.selected_menu
    
    if menu == "📊 Dashboard":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(st.session_state.patients)}</div><div class="metric-label">Total Patients</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(st.session_state.vitals)}</div><div class="metric-label">Vitals Records</div></div>', unsafe_allow_html=True)
        with col3:
            active = len([m for m in st.session_state.medications if m.get('status') == 'active'])
            st.markdown(f'<div class="metric-card"><div class="metric-value">{active}</div><div class="metric-label">Active Meds</div></div>', unsafe_allow_html=True)
        with col4:
            pending = len([a for a in st.session_state.appointments if a.get('status') == 'pending'])
            st.markdown(f'<div class="metric-card"><div class="metric-value">{pending}</div><div class="metric-label">Pending Appointments</div></div>', unsafe_allow_html=True)
        
        pending_requests = len([r for r in st.session_state.registration_requests if r['status'] == 'pending' and r.get('source') != 'manual'])
        if pending_requests > 0:
            st.warning(f"📝 You have {pending_requests} pending patient registration approvals. Go to 'Patient Management' to review.")
        
        if st.session_state.patients:
            st.subheader("📋 All Registered Patients")
            df = pd.DataFrame([p for p in st.session_state.patients if p.get('active', True)])
            st.dataframe(df, use_container_width=True)
    
    elif menu == "👨‍👩‍👧 Patient Management":
        show_patient_management()
    
    elif menu == "📅 Appointments":
        st.header("📅 Manage Appointments")
        
        with st.form("appointment_form"):
            patients = {p['patient_id']: p['name'] for p in st.session_state.patients if p.get('active', True)}
            if not patients:
                st.warning("No patients registered")
            else:
                selected_patient = st.selectbox("Select Patient", list(patients.keys()), format_func=lambda x: f"{x} - {patients[x]}")
                
                doctor_options = {username: f"{info['name']} ({info['specialty']})" for username, info in DOCTORS.items()}
                selected_doctor = st.selectbox("Select Doctor", list(doctor_options.keys()), format_func=lambda x: doctor_options[x])
                
                appointment_date = st.datetime_input("Appointment Date & Time")
                reason = st.text_area("Reason for Visit")
                
                if st.form_submit_button("Send Appointment Request"):
                    add_appointment(selected_patient, selected_doctor, DOCTORS[selected_doctor]["name"], str(appointment_date), reason)
                    st.success(f"✅ Appointment request sent to {DOCTORS[selected_doctor]['name']}!")
        
        st.subheader("📋 All Appointments")
        if st.session_state.appointments:
            df = pd.DataFrame(st.session_state.appointments)
            patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
            df['patient_name'] = df['patient_id'].map(patient_names)
            st.dataframe(df[['id', 'date_time', 'patient_name', 'doctor_name', 'reason', 'status']], use_container_width=True)
            
            appointment_ids = [a.get('id') for a in st.session_state.appointments]
            if appointment_ids:
                del_id = st.selectbox("Select Appointment ID to Delete", appointment_ids)
                if st.button("🗑️ Delete Appointment"):
                    delete_appointment(del_id)
                    st.success("Appointment deleted!")
                    st.rerun()
    
    elif menu == "🤖 AI Assistant":
        chatbot_ui()
    
    elif menu == "💾 Backup/Restore":
        st.header("💾 Backup & Restore")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create Backup"):
                import zipfile, io
                buf = io.BytesIO()
                with zipfile.ZipFile(buf, 'w') as zf:
                    for f in os.listdir(DATA_FOLDER):
                        zf.write(os.path.join(DATA_FOLDER, f), f)
                b64 = base64.b64encode(buf.getvalue()).decode()
                st.markdown(f'<a href="data:application/zip;base64,{b64}" download="backup.zip">📥 Download Backup</a>', unsafe_allow_html=True)
        with col2:
            uploaded = st.file_uploader("Restore", type=['zip'])
            if uploaded:
                import zipfile, io
                with zipfile.ZipFile(io.BytesIO(uploaded.read()), 'r') as zf:
                    zf.extractall(DATA_FOLDER)
                st.rerun()
    
    elif menu == "ℹ️ About":
        st.header("🌐 About ICT Health")
        st.markdown("""
        **ICT in Health - Hospital Management System**
        
        Features:
        - Patient Self Registration with Admin Approval
        - Manual Patient Entry by Admin for Walk-ins with Doctor Referral
        - Admin generates Unique Patient ID
        - Secure Admin, Doctor & Patient Portals
        - Vitals Tracking (BP, Sugar, Heart Rate)
        - Doctor can prescribe medications, add medical notes, and follow-up advice
        - Appointment Request/Accept Workflow
        - Health Analytics Dashboard
        - PDF Reports Generation
        - AI Health Assistant Chatbot
        
        **Access Credentials:**
        - **Admin:** `admin` / `12345`
        - **Doctors:** `cardiologist` / `cardiologist`, `general physician` / `general physician`, `neurologist` / `neurologist`
        - **Patient:** Use Patient ID (generated after admin approval) + Registered Name
        """)
    
    else:
        # Other menus (Record Vitals, Medications, Analytics, Reports)
        if menu == "🩺 Record Vitals":
            st.header("🩺 Record Patient Vitals")
            if st.session_state.patients:
                patients = {p['patient_id']: p['name'] for p in st.session_state.patients if p.get('active', True)}
                selected = st.selectbox("Select Patient", list(patients.keys()), format_func=lambda x: f"{x} - {patients[x]}")
                with st.form("vitals_form"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        sys = st.number_input("Systolic BP", 50, 250, 120)
                        dia = st.number_input("Diastolic BP", 30, 150, 80)
                    with col2:
                        hr = st.number_input("Heart Rate", 30, 200, 75)
                        bs = st.number_input("Blood Sugar", 0, 600, 100)
                    with col3:
                        wt = st.number_input("Weight (kg)", 0, 300, 70)
                    notes = st.text_area("Notes")
                    if st.form_submit_button("Save"):
                        add_vitals(selected, sys, dia, hr, bs, wt, notes)
                        st.success("✅ Vitals saved!")
        
        elif menu == "💊 Medications":
            st.header("💊 Prescribe Medication")
            if st.session_state.patients:
                patients = {p['patient_id']: p['name'] for p in st.session_state.patients if p.get('active', True)}
                selected = st.selectbox("Select Patient", list(patients.keys()), format_func=lambda x: f"{x} - {patients[x]}")
                with st.form("med_form"):
                    med = st.text_input("Medication Name")
                    dose = st.text_input("Dosage")
                    freq = st.selectbox("Frequency", ["Once daily", "Twice daily", "Three times daily"])
                    col1, col2 = st.columns(2)
                    with col1:
                        start = st.date_input("Start Date")
                    with col2:
                        end = st.date_input("End Date")
                    if st.form_submit_button("Prescribe") and med:
                        add_medication(selected, med, dose, freq, str(start), str(end))
                        st.success(f"✅ {med} prescribed!")
        
        elif menu == "📈 Analytics":
            st.header("📊 Health Analytics")
            if st.session_state.vitals:
                patients = {p['patient_id']: p['name'] for p in st.session_state.patients if p.get('active', True)}
                selected = st.selectbox("Select Patient", list(patients.keys()), format_func=lambda x: f"{x} - {patients[x]}")
                df = pd.DataFrame(st.session_state.vitals)
                df['date'] = pd.to_datetime(df['date'])
                df_patient = df[df['patient_id'] == selected].sort_values('date')
                if not df_patient.empty:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df_patient['date'], y=df_patient['bp_systolic'], name='Systolic'))
                    fig.add_trace(go.Scatter(x=df_patient['date'], y=df_patient['bp_diastolic'], name='Diastolic'))
                    fig.update_layout(title=f"BP Trend - {patients[selected]}")
                    st.plotly_chart(fig, use_container_width=True)
        
        elif menu == "📄 Reports":
            st.header("📄 Generate Report")
            if st.session_state.patients:
                patients = {p['patient_id']: p['name'] for p in st.session_state.patients if p.get('active', True)}
                selected = st.selectbox("Select Patient", list(patients.keys()), format_func=lambda x: f"{x} - {patients[x]}")
                if st.button("Generate Report"):
                    patient = get_patient_by_id(selected)
                    vitals = [v for v in st.session_state.vitals if v['patient_id'] == selected]
                    meds = [m for m in st.session_state.medications if m['patient_id'] == selected]
                    report = f"""ICT HEALTH REPORT
=================
Patient: {patient['name']} (ID: {selected})
Age: {patient['age']} | Gender: {patient['gender']}
Contact: {patient.get('contact', 'N/A')}

VITALS HISTORY:
"""
                    for v in vitals[-10:]:
                        report += f"\n{v['date']}: BP {v['bp_systolic']}/{v['bp_diastolic']}, HR {v['heart_rate']}, BS {v['blood_sugar']}"
                    report += "\n\nMEDICATIONS:\n"
                    for m in meds:
                        report += f"\n{m['med_name']}: {m['dosage']} ({m['frequency']})"
                    st.text_area("Report", report, height=400)
                    b64 = base64.b64encode(report.encode()).decode()
                    st.markdown(f'<a href="data:text/plain;base64,{b64}" download="report_{selected}.txt">📥 Download Report</a>', unsafe_allow_html=True)

# ==================== DOCTOR PORTAL ====================

def show_doctor_portal():
    render_sidebar()
    
    doctor_username = st.session_state.current_user
    doctor_info = DOCTORS.get(doctor_username, {})
    doctor_name = doctor_info.get("name", doctor_username)
    
    st.markdown(f'<div class="main-header"><h2>👨‍⚕️ Welcome, {doctor_name}!</h2><p>{doctor_info.get("specialty", "Doctor")} Portal</p></div>', unsafe_allow_html=True)
    
    menu = st.session_state.selected_menu
    
    if menu == "📊 Doctor Dashboard":
        st.header("📊 Your Dashboard")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            pending = len([a for a in st.session_state.appointments if a.get('doctor_username') == doctor_username and a['status'] == 'pending'])
            st.markdown(f'<div class="metric-card"><div class="metric-value">{pending}</div><div class="metric-label">Pending Requests</div></div>', unsafe_allow_html=True)
        with col2:
            accepted = len([a for a in st.session_state.appointments if a.get('doctor_username') == doctor_username and a['status'] == 'accepted'])
            st.markdown(f'<div class="metric-card"><div class="metric-value">{accepted}</div><div class="metric-label">Accepted Appointments</div></div>', unsafe_allow_html=True)
        with col3:
            patients_count = len(set([a['patient_id'] for a in st.session_state.appointments if a.get('doctor_username') == doctor_username and a['status'] == 'accepted']))
            st.markdown(f'<div class="metric-card"><div class="metric-value">{patients_count}</div><div class="metric-label">Your Patients</div></div>', unsafe_allow_html=True)
        
        today = date.today().strftime("%Y-%m-%d")
        today_appointments = [a for a in st.session_state.appointments if a.get('doctor_username') == doctor_username and a['status'] == 'accepted' and today in a.get('date_time', '')]
        if today_appointments:
            st.subheader("📋 Today's Appointments")
            for apt in today_appointments:
                patient = get_patient_by_id(apt['patient_id'])
                st.markdown(f"""
                <div class="appointment-accepted" style="padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <strong>🕐 Time:</strong> {apt['date_time']}<br>
                    <strong>👤 Patient:</strong> {patient['name'] if patient else apt['patient_id']}<br>
                    <strong>📝 Reason:</strong> {apt['reason']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No appointments scheduled for today.")
    
    elif menu == "📅 Appointment Requests":
        st.header("📅 Pending Appointment Requests")
        
        pending_appointments = [a for a in st.session_state.appointments if a.get('doctor_username') == doctor_username and a['status'] == 'pending']
        
        if pending_appointments:
            for apt in pending_appointments:
                patient = get_patient_by_id(apt['patient_id'])
                with st.container():
                    st.markdown(f"""
                    <div class="appointment-pending" style="padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                        <strong>📅 Date:</strong> {apt['date_time']}<br>
                        <strong>👤 Patient:</strong> {patient['name'] if patient else apt['patient_id']}<br>
                        <strong>📝 Reason:</strong> {apt['reason']}<br>
                        <strong>📅 Requested:</strong> {apt.get('created_at', 'N/A')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✅ Accept", key=f"accept_{apt['id']}"):
                            update_appointment_status(apt['id'], 'accepted')
                            st.success(f"Appointment accepted for {apt['date_time']}")
                            st.rerun()
                    with col2:
                        if st.button(f"❌ Decline", key=f"decline_{apt['id']}"):
                            update_appointment_status(apt['id'], 'declined')
                            st.warning("Appointment declined")
                            st.rerun()
                    st.markdown("---")
        else:
            st.info("No pending appointment requests.")
    
    elif menu == "✅ My Appointments":
        st.header("✅ Your Appointments")
        
        accepted_appointments = [a for a in st.session_state.appointments if a.get('doctor_username') == doctor_username and a['status'] == 'accepted']
        
        if accepted_appointments:
            for apt in accepted_appointments:
                patient = get_patient_by_id(apt['patient_id'])
                st.markdown(f"""
                <div class="appointment-accepted" style="padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                    <strong>📅 Date:</strong> {apt['date_time']}<br>
                    <strong>👤 Patient:</strong> {patient['name'] if patient else apt['patient_id']}<br>
                    <strong>📝 Reason:</strong> {apt['reason']}<br>
                    <strong>✅ Status:</strong> Accepted on {apt.get('responded_at', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No accepted appointments.")
    
    elif menu == "👥 My Patients":
        st.header("👥 Your Patients")
        
        my_patient_ids = set([a['patient_id'] for a in st.session_state.appointments if a.get('doctor_username') == doctor_username and a['status'] == 'accepted'])
        
        # Also include patients who have been prescribed medications or notes by this doctor
        med_patients = set([m['patient_id'] for m in st.session_state.doctor_medications if m['doctor_username'] == doctor_username])
        note_patients = set([n['patient_id'] for n in st.session_state.patient_notes if n['doctor_username'] == doctor_username])
        all_patient_ids = my_patient_ids.union(med_patients).union(note_patients)
        
        if all_patient_ids:
            for pid in all_patient_ids:
                patient = get_patient_by_id(pid)
                if patient:
                    with st.expander(f"👤 {patient['name']} (ID: {pid})", expanded=False):
                        if st.button(f"📋 View & Manage {patient['name']}", key=f"manage_{pid}"):
                            st.session_state.selected_patient_for_doctor = pid
                            st.session_state.show_patient_detail = True
                            st.rerun()
                        
                        # Quick preview
                        st.write(f"**Age:** {patient['age']} | **Gender:** {patient['gender']}")
                        st.write(f"**Contact:** {patient.get('contact', 'N/A')}")
        else:
            st.info("No patients assigned yet.")
        
        # Show detailed view if selected
        if st.session_state.get('show_patient_detail', False):
            patient_id = st.session_state.get('selected_patient_for_doctor')
            if patient_id:
                patient = get_patient_by_id(patient_id)
                if patient:
                    show_doctor_patient_details(patient_id, patient['name'], doctor_username, doctor_name)
    
    elif menu == "🤖 AI Assistant":
        chatbot_ui()
    
    elif menu == "ℹ️ About":
        st.header("ℹ️ About Doctor Portal")
        st.markdown("""
        **Doctor Portal Features:**
        
        - ✅ View and manage appointment requests
        - ✅ Accept or decline patient appointments
        - ✅ View your schedule and patient list
        - ✅ Prescribe medications to patients
        - ✅ Add medical notes and clinical observations
        - ✅ Schedule follow-up appointments with advice
        - ✅ Access complete patient health records
        - ✅ AI Health Assistant for clinical support
        """)

# ==================== PATIENT PORTAL ====================

def show_patient_portal():
    render_sidebar()
    
    patient_id = st.session_state.current_patient_id
    patient_name = st.session_state.current_patient_name
    patient_vitals, patient_meds, patient_appointments = get_patient_data(patient_id)
    
    st.markdown(f'<div class="main-header"><h2>🏥 Welcome, {patient_name}!</h2><p>Your Personal Health Dashboard</p></div>', unsafe_allow_html=True)
    
    menu = st.session_state.selected_menu
    
    if menu == "📊 My Dashboard":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(patient_vitals)}</div><div class="metric-label">Your Vitals</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(patient_meds)}</div><div class="metric-label">Medications</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(patient_appointments)}</div><div class="metric-label">Appointments</div></div>', unsafe_allow_html=True)
        
        pending_appointments = [a for a in patient_appointments if a['status'] == 'pending']
        accepted_appointments = [a for a in patient_appointments if a['status'] == 'accepted']
        
        if pending_appointments:
            st.warning(f"📅 You have {len(pending_appointments)} pending appointment requests")
        if accepted_appointments:
            st.success(f"✅ You have {len(accepted_appointments)} accepted appointments")
        
        # Show doctor's prescribed medications
        doctor_meds = get_doctor_medications(patient_id)
        if doctor_meds:
            st.subheader("💊 Prescribed by Doctors")
            for med in doctor_meds[-5:]:
                st.markdown(f"""
                <div style="background: #fef3c7; padding: 10px; border-radius: 8px; margin-bottom: 8px;">
                    <strong>{med['med_name']}</strong> - {med['dosage']} ({med['frequency']})<br>
                    <small>👨‍⚕️ Dr. {med['doctor_name']} | 📅 {med['prescribed_at'][:10]}</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Show follow-ups
        followups = get_followups(patient_id)
        if followups:
            st.subheader("📅 Upcoming Follow-ups")
            for fup in followups[-3:]:
                st.markdown(f"""
                <div style="background: #e0f2fe; padding: 10px; border-radius: 8px; margin-bottom: 8px;">
                    <strong>📅 Follow-up Date:</strong> {fup['followup_date']}<br>
                    <strong>📝 Advice:</strong> {fup['advice'][:100]}...
                </div>
                """, unsafe_allow_html=True)
        
        if patient_vitals:
            st.subheader("Recent Vitals")
            df = pd.DataFrame(patient_vitals[-5:])
            st.dataframe(df[['date', 'bp_systolic', 'bp_diastolic', 'heart_rate', 'blood_sugar']], use_container_width=True)
    
    elif menu == "📅 My Appointments":
        st.header("📅 Your Appointments")
        
        if patient_appointments:
            for apt in patient_appointments:
                status_class = f"status-{apt['status']}"
                status_text = apt['status'].upper()
                st.markdown(f"""
                <div style="padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #ddd;">
                    <strong>📅 Date:</strong> {apt['date_time']}<br>
                    <strong>👨‍⚕️ Doctor:</strong> {apt['doctor_name']}<br>
                    <strong>📝 Reason:</strong> {apt['reason']}<br>
                    <strong>📌 Status:</strong> <span class="status-badge {status_class}">{status_text}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No appointments scheduled.")
    
    elif menu == "🤖 AI Assistant":
        chatbot_ui()
    
    else:
        if menu == "🩺 My Vitals" and patient_vitals:
            df = pd.DataFrame(patient_vitals)
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            st.markdown(f'<a href="data:file/csv;base64,{b64}" download="my_vitals.csv">📥 Export CSV</a>', unsafe_allow_html=True)
        
        elif menu == "💊 My Medications":
            all_meds = patient_meds + get_doctor_medications(patient_id)
            if all_meds:
                df = pd.DataFrame(all_meds)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No medications prescribed yet.")
        
        elif menu == "📈 My Analytics" and len(patient_vitals) > 1:
            df = pd.DataFrame(patient_vitals)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['date'], y=df['bp_systolic'], name='Systolic'))
            fig.add_trace(go.Scatter(x=df['date'], y=df['bp_diastolic'], name='Diastolic'))
            fig.update_layout(title="Your Blood Pressure Trend")
            st.plotly_chart(fig, use_container_width=True)
        
        elif menu == "📄 My Reports" and st.button("Generate Report"):
            report = f"""PATIENT HEALTH REPORT
=====================
Patient: {patient_name} (ID: {patient_id})

VITALS HISTORY:
"""
            for v in patient_vitals[-10:]:
                report += f"\n{v['date']}: BP {v['bp_systolic']}/{v['bp_diastolic']}, HR {v['heart_rate']}"
            report += "\n\nMEDICATIONS:\n"
            for m in patient_meds:
                report += f"\n{m['med_name']}: {m['dosage']}"
            
            doctor_meds = get_doctor_medications(patient_id)
            if doctor_meds:
                report += "\n\nDOCTOR PRESCRIBED MEDICATIONS:\n"
                for m in doctor_meds:
                    report += f"\n{m['med_name']}: {m['dosage']} ({m['frequency']}) - Dr. {m['doctor_name']}"
            
            st.text_area("Report", report, height=400)
            b64 = base64.b64encode(report.encode()).decode()
            st.markdown(f'<a href="data:text/plain;base64,{b64}" download="my_report.txt">📥 Download Report</a>', unsafe_allow_html=True)
        
        elif menu == "ℹ️ About":
            st.header("About Your Portal")
            st.markdown("""
            **Your Personal Health Portal**
            
            Here you can:
            - ✅ View your medical records
            - ✅ Track your vitals over time
            - ✅ See prescribed medications
            - ✅ Check your appointments
            - ✅ View doctor's notes and follow-up advice
            - ✅ Download your health reports
            - ✅ Chat with our AI Health Assistant
            
            Stay healthy! 💙
            """)

# ==================== MAIN ====================

def main():
    if 'show_patient_detail' not in st.session_state:
        st.session_state.show_patient_detail = False
    if 'selected_patient_for_doctor' not in st.session_state:
        st.session_state.selected_patient_for_doctor = None
    
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.user_type == "admin":
            show_admin_dashboard()
        elif st.session_state.user_type == "doctor":
            show_doctor_portal()
        else:
            show_patient_portal()

if __name__ == "__main__":
    main()
