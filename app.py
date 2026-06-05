"""
ICT in Health - Hospital Management System
With Secure Login: Admin Portal + Patient Portal (ID + Name only)
Beautiful Sidebar Navigation - All features visible
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import base64
import hashlib

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
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2b1f 0%, #1a4a2a 50%, #0f2b1f 100%);
        padding-top: 20px;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: white;
    }

    /* Fix the ugly bottom - force consistent color on all sidebar children */
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }

    section[data-testid="stSidebar"] > div:last-child {
        background: #0f2b1f !important;
    }
    
    /* Sidebar navigation buttons */
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
    
    .nav-button:hover {
        background: rgba(255,255,255,0.2);
        transform: translateX(5px);
    }
    
    .nav-button-active {
        background: linear-gradient(135deg, #2d8c5a 0%, #1f6e4a 100%);
        border-left: 4px solid #ffd700;
    }
    
    /* Sidebar header */
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
    
    /* User info card */
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
    
    /* Stats in sidebar */
.stat-card {
    background: rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 10px;
    margin: 8px 10px;
    text-align: center;
    border-left: 3px solid #ffd700;  /* ADD THIS LINE */
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
    
    /* Logout button */
    .logout-btn {
        background: #dc2626;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px;
        margin: 20px 10px;
        width: calc(100% - 20px);
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .logout-btn:hover {
        background: #b91c1c;
        transform: scale(1.02);
    }
    
    /* Main content area */
    .main-header {
        background: linear-gradient(135deg, #1f6e4a 0%, #0f533a 100%);
        padding: 20px 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        color: white;
    }
    
    /* Metric cards */
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

    /* Fix Streamlit's default selectbox & widget backgrounds in sidebar */
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

    /* Hide Streamlit's default footer branding at bottom of sidebar */
    [data-testid="stSidebar"] footer {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== AUTHENTICATION ====================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("12345")

def init_auth():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'current_patient_id' not in st.session_state:
        st.session_state.current_patient_id = None
    if 'current_patient_name' not in st.session_state:
        st.session_state.current_patient_name = None
    if 'selected_menu' not in st.session_state:
        st.session_state.selected_menu = "📊 Dashboard"

init_auth()

def login_admin(username, password):
    return username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH

def verify_patient(patient_id, patient_name):
    patients = st.session_state.patients
    for patient in patients:
        if patient['patient_id'] == patient_id and patient['name'].lower() == patient_name.lower():
            return True, patient['name']
    return False, None

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

def get_patient_data(patient_id):
    patient_vitals = [v for v in st.session_state.vitals if v['patient_id'] == patient_id]
    patient_meds = [m for m in st.session_state.medications if m['patient_id'] == patient_id]
    patient_appointments = [a for a in st.session_state.appointments if a['patient_id'] == patient_id]
    return patient_vitals, patient_meds, patient_appointments

def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
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
        
        tab1, tab2 = st.tabs(["👨‍💼 Admin Login", "👤 Patient Login"])
        
        with tab1:
            admin_username = st.text_input("Username", key="admin_user", placeholder="admin")
            admin_password = st.text_input("Password", type="password", key="admin_pass", placeholder="•••••")
            if st.button("🔐 Login as Admin", key="admin_login"):
                if login_admin(admin_username, admin_password):
                    st.session_state.logged_in = True
                    st.session_state.user_type = "admin"
                    st.rerun()
                else:
                    st.error("❌ Invalid admin credentials!")
        
        with tab2:
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
    """Render beautiful sidebar with navigation buttons"""
    
    with st.sidebar:
        # Header
        st.markdown("""
        <div class="sidebar-header">
            <h1>🏥 ICT Health</h1>
            <p>Hospital Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User info
        if st.session_state.user_type == "admin":
            st.markdown("""
            <div class="user-card">
                <h4>👨‍💼 Admin</h4>
                <p>Full Access</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Stats for admin
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(st.session_state.patients)}</div>
                <div class="stat-label">Total Patients</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(st.session_state.vitals)}</div>
                <div class="stat-label">Vitals Records</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len([m for m in st.session_state.medications if m.get('status') == 'active'])}</div>
                <div class="stat-label">Active Medications</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin: 20px 0 10px 15px; color: #ffd700; font-size: 0.8rem;'>📋 MAIN MENU</div>", unsafe_allow_html=True)
            
            # Admin menu items
            menu_items = [
                "📊 Dashboard", "👨‍👩‍👧 Register Patient", "🩺 Record Vitals",
                "💊 Medications", "📅 Appointments", "📈 Analytics",
                "📄 Reports", "💾 Backup/Restore", "🤖 AI Assistant", "ℹ️ About"
            ]
            
        else:
            # Patient info
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
            
            # Patient menu items
            menu_items = [
                "📊 My Dashboard", "🩺 My Vitals", "💊 My Medications",
                "📅 My Appointments", "📈 My Analytics", "📄 My Reports",
                "🤖 AI Assistant", "ℹ️ About"
            ]
        
        # Render menu buttons
        for item in menu_items:
            is_active = st.session_state.selected_menu == item
            active_class = "nav-button-active" if is_active else ""
            
            # Create clickable button
            if st.button(item, key=f"sidebar_{item}", use_container_width=True):
                st.session_state.selected_menu = item
                st.rerun()
        
        # Logout button
        st.markdown("---")
        if st.button("🚪 Logout", key="sidebar_logout", use_container_width=True):
            logout()
        
        # Footer
        st.markdown("""
        <div style="text-align: center; padding: 20px 10px; margin-top: 20px;">
            <small style="color: #a0c4b0;">© 2026 ICT Health<br>Secure Hospital System</small>
        </div>
        """, unsafe_allow_html=True)

# ==================== ADMIN DASHBOARD ====================

def show_admin_dashboard():
    render_sidebar()
    
    # Main content header
    st.markdown('<div class="main-header"><h2>🏥 ICT Health - Admin Dashboard</h2><p>Complete Patient Data Access</p></div>', unsafe_allow_html=True)
    
    menu = st.session_state.selected_menu
    
    if menu == "📊 Dashboard":
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(st.session_state.patients)}</div><div class="metric-label">Total Patients</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(st.session_state.vitals)}</div><div class="metric-label">Vitals Records</div></div>', unsafe_allow_html=True)
        with col3:
            active = len([m for m in st.session_state.medications if m.get('status') == 'active'])
            st.markdown(f'<div class="metric-card"><div class="metric-value">{active}</div><div class="metric-label">Active Meds</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><div class="metric-value">{len(st.session_state.appointments)}</div><div class="metric-label">Appointments</div></div>', unsafe_allow_html=True)
        
        if st.session_state.patients:
            st.subheader("📋 All Registered Patients")
            df = pd.DataFrame(st.session_state.patients)
            st.dataframe(df, use_container_width=True)
    
    elif menu == "👨‍👩‍👧 Register Patient":
        st.header("📝 Register New Patient")
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
            if st.form_submit_button("Register"):
                if pid and name:
                    if pid in [p['patient_id'] for p in st.session_state.patients]:
                        st.error("ID exists!")
                    else:
                        add_patient(pid, name, age, gender, contact, address)
                        st.success(f"✅ {name} registered! Login ID: {pid}, Name: {name}")
                        st.balloons()
                else:
                    st.warning("Fill required fields")
        
        st.subheader("📋 Registered Patients")
        if st.session_state.patients:
            df = pd.DataFrame(st.session_state.patients)
            st.dataframe(df, use_container_width=True)
    
    elif menu == "🩺 Record Vitals":
        st.header("🩺 Record Patient Vitals")
        if st.session_state.patients:
            patients = {p['patient_id']: p['name'] for p in st.session_state.patients}
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
            patients = {p['patient_id']: p['name'] for p in st.session_state.patients}
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
    
    elif menu == "📅 Appointments":
        st.header("📅 Schedule Appointment")
        if st.session_state.patients:
            patients = {p['patient_id']: p['name'] for p in st.session_state.patients}
            selected = st.selectbox("Select Patient", list(patients.keys()), format_func=lambda x: f"{x} - {patients[x]}")
            with st.form("app_form"):
                doctor = st.text_input("Doctor Name")
                date_time = st.datetime_input("Date & Time")
                reason = st.text_area("Reason")
                if st.form_submit_button("Schedule"):
                    add_appointment(selected, doctor, str(date_time), reason)
                    st.success("✅ Appointment scheduled!")
    
    elif menu == "📈 Analytics":
        st.header("📊 Health Analytics")
        if st.session_state.vitals:
            patients = {p['patient_id']: p['name'] for p in st.session_state.patients}
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
                
                col1, col2 = st.columns(2)
                with col1:
                    fig2 = px.line(df_patient, x='date', y='heart_rate', title="Heart Rate")
                    st.plotly_chart(fig2, use_container_width=True)
                with col2:
                    fig3 = px.line(df_patient, x='date', y='blood_sugar', title="Blood Sugar")
                    st.plotly_chart(fig3, use_container_width=True)
    
    elif menu == "📄 Reports":
        st.header("📄 Generate Report")
        if st.session_state.patients:
            patients = {p['patient_id']: p['name'] for p in st.session_state.patients}
            selected = st.selectbox("Select Patient", list(patients.keys()), format_func=lambda x: f"{x} - {patients[x]}")
            if st.button("Generate Report"):
                patient = next(p for p in st.session_state.patients if p['patient_id'] == selected)
                vitals = [v for v in st.session_state.vitals if v['patient_id'] == selected]
                meds = [m for m in st.session_state.medications if m['patient_id'] == selected]
                report = f"""
                ICT HEALTH REPORT
                =================
                Patient: {patient['name']} (ID: {selected})
                Age: {patient['age']} | Gender: {patient['gender']}
                Contact: {patient['contact']}
                
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
    
    elif menu == "🤖 AI Assistant":
        chatbot_ui()
    
    elif menu == "ℹ️ About":
        st.header("🌐 About ICT Health")
        st.markdown("""
        **ICT in Health - Hospital Management System**
        
        Features:
        - Secure Admin & Patient Portals
        - Patient Registration & Management
        - Vitals Tracking (BP, Sugar, Heart Rate)
        - Medication Prescription & Tracking
        - Appointment Scheduling
        - Health Analytics Dashboard
        - PDF Reports Generation
        - AI Health Assistant Chatbot
        
        **Access:**
        - Admin: `admin` / `12345`
        - Patient: Use registered Patient ID + Name
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
        if patient_vitals:
            st.subheader("Recent Vitals")
            df = pd.DataFrame(patient_vitals[-5:])
            st.dataframe(df[['date', 'bp_systolic', 'bp_diastolic', 'heart_rate', 'blood_sugar']], use_container_width=True)
    
    elif menu == "🩺 My Vitals":
        st.header("Your Vitals History")
        if patient_vitals:
            df = pd.DataFrame(patient_vitals)
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            st.markdown(f'<a href="data:file/csv;base64,{b64}" download="my_vitals.csv">📥 Export CSV</a>', unsafe_allow_html=True)
    
    elif menu == "💊 My Medications":
        st.header("Your Medications")
        if patient_meds:
            df = pd.DataFrame(patient_meds)
            st.dataframe(df[['med_name', 'dosage', 'frequency', 'start_date', 'end_date', 'status']], use_container_width=True)
    
    elif menu == "📅 My Appointments":
        st.header("Your Appointments")
        if patient_appointments:
            df = pd.DataFrame(patient_appointments)
            st.dataframe(df[['date_time', 'doctor', 'reason', 'status']], use_container_width=True)
    
    elif menu == "📈 My Analytics":
        st.header("Your Health Trends")
        if len(patient_vitals) > 1:
            df = pd.DataFrame(patient_vitals)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['date'], y=df['bp_systolic'], name='Systolic'))
            fig.add_trace(go.Scatter(x=df['date'], y=df['bp_diastolic'], name='Diastolic'))
            fig.update_layout(title="Your Blood Pressure Trend")
            st.plotly_chart(fig, use_container_width=True)
    
    elif menu == "📄 My Reports":
        st.header("Your Health Report")
        if st.button("Generate Report"):
            report = f"""
            PATIENT HEALTH REPORT
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
    
    elif menu == "🤖 AI Assistant":
        chatbot_ui()
    
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
        else:
            show_patient_portal()

if __name__ == "__main__":
    main()
