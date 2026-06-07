"""
ICT in Health - Hospital Management System
With Admin, Doctor & Patient Portals
Appointment Request/Accept Workflow + Edit/Delete Options
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

    .reminder-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid #f59e0b;
    }
    
    .appointment-pending {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 5px solid #f59e0b;
    }
    
    .appointment-accepted {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 5px solid #10b981;
    }
    
    .appointment-declined {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 5px solid #ef4444;
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
    "doctor": {"name": "Dr. Sarah Ahmed", "password_hash": hash_password("doctor123"), "specialty": "Cardiologist", "available": True},
    "doctor2": {"name": "Dr. Ali Raza", "password_hash": hash_password("doctor123"), "specialty": "General Physician", "available": True},
    "doctor3": {"name": "Dr. Fatima Khan", "password_hash": hash_password("doctor123"), "specialty": "Pediatrician", "available": True}
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
    if 'reminders' not in st.session_state:
        st.session_state.reminders = []
    if 'reminder_check_time' not in st.session_state:
        st.session_state.reminder_check_time = None

init_auth()

def login_admin(username, password):
    return username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH

def login_doctor(username, password):
    if username in DOCTORS and DOCTORS[username]["password_hash"] == hash_password(password):
        return True, DOCTORS[username]["name"]
    return False, None

def verify_patient(patient_id, patient_name):
    patients = st.session_state.patients
    for patient in patients:
        if patient['patient_id'] == patient_id and patient['name'].lower() == patient_name.lower() and patient.get('active', True):
            return True, patient['name']
    return False, None

# ==================== REMINDER FUNCTIONS ====================

REMINDERS_FILE = os.path.join("hospital_data", "reminders.json")

def save_reminders():
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(st.session_state.reminders, f, indent=2)

def load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, 'r') as f:
            st.session_state.reminders = json.load(f)

def add_reminder(patient_id, medicine_name, reminder_time, dosage):
    reminder = {
        'id': len(st.session_state.reminders) + 1,
        'patient_id': patient_id,
        'medicine_name': medicine_name,
        'reminder_time': reminder_time,
        'dosage': dosage,
        'active': True,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.reminders.append(reminder)
    save_reminders()
    return True

def delete_reminder(reminder_id):
    st.session_state.reminders = [r for r in st.session_state.reminders if r['id'] != reminder_id]
    save_reminders()

def toggle_reminder(reminder_id):
    for r in st.session_state.reminders:
        if r['id'] == reminder_id:
            r['active'] = not r['active']
            break
    save_reminders()

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
load_reminders()

# ==================== HELPER FUNCTIONS ====================

def add_patient(patient_id, name, age, gender, contact, address):
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
    return True

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
    # Also delete related data
    st.session_state.vitals = [v for v in st.session_state.vitals if v['patient_id'] != patient_id]
    st.session_state.medications = [m for m in st.session_state.medications if m['patient_id'] != patient_id]
    st.session_state.appointments = [a for a in st.session_state.appointments if a['patient_id'] != patient_id]
    st.session_state.reminders = [r for r in st.session_state.reminders if r['patient_id'] != patient_id]
    save_patients(st.session_state.patients)
    save_vitals(st.session_state.vitals)
    save_medications(st.session_state.medications)
    save_appointments(st.session_state.appointments)
    save_reminders()

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
        
        tab1, tab2, tab3 = st.tabs(["👨‍💼 Admin Login", "👨‍⚕️ Doctor Login", "👤 Patient Login"])
        
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
            st.info("Available Doctors: doctor, doctor2, doctor3 (Password: doctor123)")
            doctor_username = st.text_input("Doctor Username", key="doctor_user", placeholder="doctor")
            doctor_password = st.text_input("Password", type="password", key="doctor_pass", placeholder="•••••")
            if st.button("🔐 Login as Doctor", key="doctor_login"):
                valid, name = login_doctor(doctor_username, doctor_password)
                if valid:
                    st.session_state.logged_in = True
                    st.session_state.user_type = "doctor"
                    st.session_state.current_user = doctor_username
                    st.session_state.current_user_name = name
                    st.rerun()
                else:
                    st.error("❌ Invalid doctor credentials!")
        
        with tab3:
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
                        st.error("❌ Invalid Patient ID or Name!")
                else:
                    st.warning("⚠️ Please enter both fields")

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
            
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(st.session_state.patients)}</div>
                <div class="stat-label">Total Patients</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([a for a in st.session_state.appointments if a['status'] == 'pending'])}</div>
                <div class="stat-label">Pending Appointments</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 20px 0 10px 15px; color: #ffd700; font-size: 0.8rem;'>📋 MAIN MENU</div>", unsafe_allow_html=True)
            
            menu_items = [
                "📊 Dashboard", "👨‍👩‍👧 Patient Registration", "🩺 Record Vitals",
                "💊 Medications", "📅 Appointments", "📈 Analytics",
                "📄 Reports", "⏰ Medicine Reminders", "💾 Backup/Restore", "🤖 AI Assistant", "ℹ️ About"
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
            
            active_reminders = len([r for r in st.session_state.reminders if r['patient_id'] == st.session_state.current_patient_id and r['active']])
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(patient_vitals)}</div>
                <div class="stat-label">Your Vitals</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(patient_meds)}</div>
                <div class="stat-label">Your Medications</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{active_reminders}</div>
                <div class="stat-label">Active Reminders</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 20px 0 10px 15px; color: #ffd700; font-size: 0.8rem;'>📋 YOUR PORTAL</div>", unsafe_allow_html=True)
            
            menu_items = [
                "📊 My Dashboard", "🩺 My Vitals", "💊 My Medications",
                "📅 My Appointments", "📈 My Analytics", "📄 My Reports",
                "⏰ My Reminders", "🤖 AI Assistant", "ℹ️ About"
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

# ==================== REMINDER UI COMPONENTS ====================

def show_reminder_management():
    st.header("⏰ Medicine Reminder System")
    
    if st.session_state.user_type == "admin":
        patients = {p['patient_id']: p['name'] for p in st.session_state.patients if p.get('active', True)}
        if patients:
            selected_patient = st.selectbox("Select Patient", list(patients.keys()), format_func=lambda x: f"{x} - {patients[x]}")
            show_patient = selected_patient
        else:
            st.warning("No patients registered yet.")
            return
    else:
        show_patient = st.session_state.current_patient_id
    
    with st.expander("➕ Add New Medicine Reminder", expanded=True):
        with st.form("add_reminder_form"):
            col1, col2 = st.columns(2)
            with col1:
                medicine_name = st.text_input("Medicine Name", placeholder="e.g., Metformin, Lisinopril")
                reminder_time = st.time_input("Reminder Time", value=dt_time(9, 0))
            with col2:
                dosage = st.text_input("Dosage", placeholder="e.g., 500mg, 1 tablet")
            
            submitted = st.form_submit_button("🔔 Set Reminder", use_container_width=True)
            
            if submitted and medicine_name:
                add_reminder(show_patient, medicine_name, reminder_time.strftime("%H:%M"), dosage)
                st.success(f"✅ Reminder set for {medicine_name} at {reminder_time.strftime('%H:%M')}")
                st.rerun()
            elif submitted:
                st.warning("Please enter medicine name")
    
    st.subheader("📋 Your Reminders")
    patient_reminders = [r for r in st.session_state.reminders if r['patient_id'] == show_patient]
    
    if patient_reminders:
        for reminder in patient_reminders:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                with col1:
                    st.markdown(f"**💊 {reminder['medicine_name']}**")
                with col2:
                    st.markdown(f"⏰ {reminder['reminder_time']}")
                with col3:
                    st.markdown(f"📦 {reminder['dosage']}")
                with col4:
                    status = "✅ Active" if reminder['active'] else "⏸️ Paused"
                    st.markdown(f"<span style='color: #10b981;'>{status}</span>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    if st.button("⏯️ Toggle", key=f"toggle_{reminder['id']}"):
                        toggle_reminder(reminder['id'])
                        st.rerun()
                with col2:
                    if st.button("🗑️ Delete", key=f"del_{reminder['id']}"):
                        delete_reminder(reminder['id'])
                        st.rerun()
                st.markdown("---")
    else:
        st.info("No reminders set. Add a reminder above!")

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
        
        if st.session_state.patients:
            st.subheader("📋 All Registered Patients")
            df = pd.DataFrame([p for p in st.session_state.patients if p.get('active', True)])
            st.dataframe(df, use_container_width=True)
    
    elif menu == "👨‍👩‍👧 Patient Registration":
        st.header("📝 Patient Management")
        
        tab1, tab2, tab3 = st.tabs(["➕ Register New", "✏️ Edit Patient", "🗑️ Delete Patient"])
        
        with tab1:
            with st.form("reg_form"):
                col1, col2 = st.columns(2)
                with col1:
                    pid = st.text_input("Patient ID (Unique)")
                    name = st.text_input("Full Name")
                    age = st.number_input("Age", min_value=0, max_value=150)
                with col2:
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                    contact = st.text_input("Contact")
                    address = st.text_area("Address")
                if st.form_submit_button("Register Patient"):
                    if pid and name:
                        if pid in [p['patient_id'] for p in st.session_state.patients]:
                            st.error("❌ Patient ID already exists!")
                        else:
                            add_patient(pid, name, age, gender, contact, address)
                            st.success(f"✅ {name} registered! Login ID: {pid}, Name: {name}")
                            st.balloons()
                    else:
                        st.warning("Please fill required fields")
        
        with tab2:
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
        
        with tab3:
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
        
        st.subheader("📋 Registered Patients")
        if st.session_state.patients:
            df = pd.DataFrame([p for p in st.session_state.patients if p.get('active', True)])
            st.dataframe(df, use_container_width=True)
    
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
            
            # Delete appointment option
            appointment_ids = [a.get('id') for a in st.session_state.appointments]
            if appointment_ids:
                del_id = st.selectbox("Select Appointment ID to Delete", appointment_ids)
                if st.button("🗑️ Delete Appointment"):
                    delete_appointment(del_id)
                    st.success("Appointment deleted!")
                    st.rerun()
    
    elif menu == "⏰ Medicine Reminders":
        show_reminder_management()
    
    elif menu == "🤖 AI Assistant":
        chatbot_ui()
    
    else:
        # Other menus remain same as before
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
            - Secure Admin, Doctor & Patient Portals
            - Patient Registration with Edit/Delete
            - Doctor Appointment Request/Accept Workflow
            - Vitals Tracking (BP, Sugar, Heart Rate)
            - Medication Prescription & Tracking
            - Medicine Reminders with Alarm
            - Health Analytics Dashboard
            - PDF Reports Generation
            - AI Health Assistant Chatbot
            
            **Access Credentials:**
            - **Admin:** Username: `admin` | Password: `12345`
            - **Doctors:** `doctor`, `doctor2`, `doctor3` | Password: `doctor123`
            - **Patient:** Use registered Patient ID + Name
            """)

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
        
        # Today's appointments
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
        
        if my_patient_ids:
            for pid in my_patient_ids:
                patient = get_patient_by_id(pid)
                if patient:
                    with st.expander(f"👤 {patient['name']} (ID: {pid})"):
                        st.write(f"**Age:** {patient['age']}")
                        st.write(f"**Gender:** {patient['gender']}")
                        st.write(f"**Contact:** {patient.get('contact', 'N/A')}")
                        st.write(f"**Address:** {patient.get('address', 'N/A')}")
                        
                        # Show patient vitals
                        patient_vitals = [v for v in st.session_state.vitals if v['patient_id'] == pid]
                        if patient_vitals:
                            st.write("**Recent Vitals:**")
                            df = pd.DataFrame(patient_vitals[-3:])
                            st.dataframe(df[['date', 'bp_systolic', 'bp_diastolic', 'heart_rate']], use_container_width=True)
        else:
            st.info("No patients assigned yet.")
    
    elif menu == "🤖 AI Assistant":
        chatbot_ui()
    
    elif menu == "ℹ️ About":
        st.header("ℹ️ About Doctor Portal")
        st.markdown("""
        **Doctor Portal Features:**
        
        - ✅ View and manage appointment requests
        - ✅ Accept or decline patient appointments
        - ✅ View your schedule and patient list
        - ✅ Access patient health records
        - ✅ AI Health Assistant for clinical support
        
        **Your Info:**
        - You can set your availability status
        - Appear in admin's doctor list
        - Patients can request appointments with you
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
        
        # Show appointment status
        pending_appointments = [a for a in patient_appointments if a['status'] == 'pending']
        accepted_appointments = [a for a in patient_appointments if a['status'] == 'accepted']
        
        if pending_appointments:
            st.warning(f"📅 You have {len(pending_appointments)} pending appointment requests")
        if accepted_appointments:
            st.success(f"✅ You have {len(accepted_appointments)} accepted appointments")
        
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
    
    elif menu == "⏰ My Reminders":
        show_reminder_management()
    
    elif menu == "🤖 AI Assistant":
        chatbot_ui()
    
    else:
        # Other menus remain same
        if menu == "🩺 My Vitals" and patient_vitals:
            df = pd.DataFrame(patient_vitals)
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            st.markdown(f'<a href="data:file/csv;base64,{b64}" download="my_vitals.csv">📥 Export CSV</a>', unsafe_allow_html=True)
        
        elif menu == "💊 My Medications" and patient_meds:
            df = pd.DataFrame(patient_meds)
            st.dataframe(df[['med_name', 'dosage', 'frequency', 'start_date', 'end_date', 'status']], use_container_width=True)
        
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
            st.text_area("Report", report, height=300)
            b64 = base64.b64encode(report.encode()).decode()
            st.markdown(f'<a href="data:text/plain;base64,{b64}" download="my_report.txt">📥 Download Report</a>', unsafe_allow_html=True)
        
        elif menu == "ℹ️ About":
            st.header("About Your Portal")
            st.markdown("View your medical records, track vitals, and manage appointments.")

# ==================== MAIN ====================

def main():
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
