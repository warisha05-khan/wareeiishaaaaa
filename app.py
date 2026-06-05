"""
ICT in Health - Hospital Management System
With Secure Login: Admin Portal + Patient Portal (ID + Name only)
Top Navigation Bar - All icons displayed horizontally
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
    initial_sidebar_state="collapsed"
)

# ==================== AUTHENTICATION ====================

# Simple password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("12345")

# Initialize session state for login
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
    """Verify patient exists with matching ID and Name (no password)"""
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

def get_patient_data(patient_id):
    """Get all data for a specific patient"""
    patient_vitals = [v for v in st.session_state.vitals if v['patient_id'] == patient_id]
    patient_meds = [m for m in st.session_state.medications if m['patient_id'] == patient_id]
    patient_appointments = [a for a in st.session_state.appointments if a['patient_id'] == patient_id]
    return patient_vitals, patient_meds, patient_appointments

# ==================== LOGIN UI ====================

def show_login_page():
    """Display beautiful login page"""
    
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
        background: linear-gradient(135deg, #0f533a 0%, #1f6e4a 100%);
    }
    div[data-testid="stTextInput"] label {
        font-weight: 600;
        color: #1f6e4a;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Hero Section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1f6e4a 0%, #0f533a 100%); 
                    border-radius: 20px; padding: 30px; text-align: center; margin-bottom: 30px;">
            <h1 style="color: white; margin-bottom: 10px;">🏥 ICT Health</h1>
            <p style="color: #e0e0e0; font-size: 1.1rem;">Hospital Management System</p>
            <p style="color: #c0c0c0; font-size: 0.9rem;">Secure Access • Patient Records • Health Analytics</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login tabs
        tab1, tab2 = st.tabs(["👨‍💼 Admin Login", "👤 Patient Login"])
        
        with tab1:
            st.markdown("### 🔐 Admin Access")
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
            st.markdown("### 🔐 Patient Portal Access")
            st.info("💡 **Login using your Patient ID and Full Name**")
            
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.text_input("Patient ID", key="patient_id", placeholder="e.g., PAT001")
            with col2:
                patient_name = st.text_input("Full Name", key="patient_name", placeholder="Enter your registered name")
            
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
                    st.warning("⚠️ Please enter both Patient ID and Name")
        
        st.markdown("---")
        st.markdown("<center><small>© 2026 ICT in Health | Secure Hospital Management System</small></center>", unsafe_allow_html=True)

# ==================== LOGOUT ====================

def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.current_patient_id = None
    st.session_state.current_patient_name = None
    st.session_state.selected_menu = "📊 Dashboard"
    st.rerun()

# ==================== TOP NAVIGATION BAR ====================

def show_top_navbar(menu_items, user_type, user_name=None):
    """Display horizontal top navigation bar with icons"""
    
    # Custom CSS for top navigation bar
    st.markdown("""
    <style>
    .top-nav {
        background: linear-gradient(135deg, #1f6e4a 0%, #0f533a 100%);
        padding: 10px 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        align-items: center;
    }
    .nav-item {
        display: inline-block;
        padding: 10px 18px;
        margin: 5px;
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        text-align: center;
    }
    .nav-item:hover {
        background: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }
    .nav-item.active {
        background: rgba(255,255,255,0.3);
        border-bottom: 3px solid #ffd700;
    }
    .logout-btn {
        background: #dc2626;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        cursor: pointer;
        font-weight: bold;
    }
    .logout-btn:hover {
        background: #b91c1c;
    }
    .user-info {
        color: white;
        font-size: 0.9rem;
        margin-left: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create top navigation bar
    cols = st.columns([len(menu_items), 1])
    
    with cols[0]:
        nav_cols = st.columns(len(menu_items))
        for i, item in enumerate(menu_items):
            with nav_cols[i]:
                is_active = st.session_state.selected_menu == item
                button_style = "background: rgba(255,255,255,0.3); border-bottom: 3px solid #ffd700;" if is_active else ""
                if st.button(item, key=f"nav_{item}", use_container_width=True,
                            help=f"Go to {item}"):
                    st.session_state.selected_menu = item
                    st.rerun()
    
    with cols[1]:
        st.button("🚪 Logout", key="top_logout", on_click=logout, use_container_width=True)


def show_admin_top_navbar():
    """Admin top navigation bar"""
    menu_items = ["📊 Dashboard", "👨‍👩‍👧 Register", "📊 Vitals", "💊 Medications", 
                  "📅 Appointments", "📈 Analytics", "📄 Reports", "💾 Backup", "🤖 AI Assistant", "ℹ️ About"]
    show_top_navbar(menu_items, "admin")
    
    # Display stats in sidebar (compact)
    st.sidebar.markdown("---")
    st.sidebar.success(f"✅ Logged in as: **Admin**")
    st.sidebar.markdown(f"📊 **System Stats**")
    st.sidebar.write(f"👥 Patients: {len(st.session_state.patients)}")
    st.sidebar.write(f"📊 Vitals: {len(st.session_state.vitals)}")
    st.sidebar.write(f"💊 Medications: {len(st.session_state.medications)}")


def show_patient_top_navbar():
    """Patient top navigation bar"""
    menu_items = ["📊 Dashboard", "📊 My Vitals", "💊 My Meds", "📅 Appointments", 
                  "📈 Analytics", "📄 Reports", "🤖 AI Assistant", "ℹ️ About"]
    show_top_navbar(menu_items, "patient", st.session_state.current_patient_name)
    
    # Display patient info in sidebar
    st.sidebar.markdown("---")
    st.sidebar.success(f"✅ Logged in as: **{st.session_state.current_patient_name}**")
    st.sidebar.info(f"🆔 ID: {st.session_state.current_patient_id}")
    
    # Get patient data counts
    patient_vitals, patient_meds, patient_appointments = get_patient_data(st.session_state.current_patient_id)
    st.sidebar.markdown(f"📊 **Your Stats**")
    st.sidebar.write(f"📊 Vitals: {len(patient_vitals)}")
    st.sidebar.write(f"💊 Medications: {len(patient_meds)}")
    st.sidebar.write(f"📅 Appointments: {len(patient_appointments)}")

# ==================== ADMIN DASHBOARD ====================

def show_admin_dashboard():
    """Admin view - can see ALL patient data"""
    
    show_admin_top_navbar()
    
    st.title("🏥 ICT in Health - Hospital Management System")
    st.markdown("*Admin Dashboard - Complete Patient Data Access*")
    
    menu = st.session_state.selected_menu
    
    # ==================== DASHBOARD ====================
    if menu == "📊 Dashboard":
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
        
        # All Patients Table
        if st.session_state.patients:
            st.subheader("📋 All Registered Patients")
            df_patients = pd.DataFrame(st.session_state.patients)
            st.dataframe(df_patients, use_container_width=True)
        else:
            st.info("No patients registered yet.")
        
        # Recent Vitals
        if st.session_state.vitals:
            st.subheader("📊 Recent Vitals Records")
            df_vitals = pd.DataFrame(st.session_state.vitals[-10:])
            st.dataframe(df_vitals, use_container_width=True)
    
    # ==================== PATIENT REGISTRATION ====================
    elif menu == "👨‍👩‍👧 Register":
        st.header("📝 Register New Patient")
        
        with st.form("patient_registration"):
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.text_input("Patient ID (Unique)", placeholder="e.g., PAT001")
                name = st.text_input("Full Name")
                age = st.number_input("Age", min_value=0, max_value=150, step=1)
            with col2:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                contact = st.text_input("Contact Number")
                address = st.text_area("Address")
            
            submitted = st.form_submit_button("Register Patient")
            
            if submitted:
                if patient_id and name:
                    existing_ids = [p['patient_id'] for p in st.session_state.patients]
                    if patient_id in existing_ids:
                        st.error(f"❌ Patient ID {patient_id} already exists!")
                    else:
                        add_patient(patient_id, name, age, gender, contact, address)
                        st.success(f"✅ Patient {name} registered successfully!")
                        st.info(f"📝 **Login Credentials:**\n\n**Patient ID:** `{patient_id}`\n**Name:** {name}")
                        st.balloons()
                else:
                    st.warning("Please fill all required fields (Patient ID and Name)")
        
        st.subheader("📋 Registered Patients")
        if st.session_state.patients:
            df_patients = pd.DataFrame(st.session_state.patients)
            st.dataframe(df_patients, use_container_width=True)
            
            csv = df_patients.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="patients_export.csv">📥 Export Patients to CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("No patients registered yet")
    
    # ==================== VITALS LOGGER ====================
    elif menu == "📊 Vitals":
        st.header("🩺 Record Patient Vitals")
        
        if not st.session_state.patients:
            st.warning("Please register patients first!")
        else:
            patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
            selected_patient = st.selectbox("Select Patient", list(patient_names.keys()), format_func=lambda x: f"{x} - {patient_names[x]}")
            
            with st.form("vitals_form"):
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
    elif menu == "💊 Medications":
        st.header("💊 Prescription & Medication Tracker")
        
        if not st.session_state.patients:
            st.warning("Please register patients first!")
        else:
            patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
            selected_patient = st.selectbox("Select Patient", list(patient_names.keys()), format_func=lambda x: f"{x} - {patient_names[x]}")
            
            with st.form("medication_form"):
                med_name = st.text_input("Medication Name")
                dosage = st.text_input("Dosage")
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
            
            st.subheader("💊 All Prescriptions")
            if st.session_state.medications:
                df_meds = pd.DataFrame(st.session_state.medications)
                df_meds['patient_name'] = df_meds['patient_id'].map(patient_names)
                st.dataframe(df_meds, use_container_width=True)
            else:
                st.info("No prescriptions yet")
    
    # ==================== APPOINTMENTS ====================
    elif menu == "📅 Appointments":
        st.header("📅 Schedule Appointments")
        
        if not st.session_state.patients:
            st.warning("Please register patients first!")
        else:
            patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
            selected_patient = st.selectbox("Select Patient", list(patient_names.keys()), format_func=lambda x: f"{x} - {patient_names[x]}")
            
            with st.form("appointment_form"):
                doctor = st.text_input("Doctor Name")
                appointment_date = st.datetime_input("Appointment Date & Time")
                reason = st.text_area("Reason for Visit")
                
                submitted = st.form_submit_button("Schedule Appointment")
                
                if submitted:
                    add_appointment(selected_patient, doctor, str(appointment_date), reason)
                    st.success(f"✅ Appointment scheduled")
            
            st.subheader("📋 All Appointments")
            if st.session_state.appointments:
                df_appointments = pd.DataFrame(st.session_state.appointments)
                df_appointments['patient_name'] = df_appointments['patient_id'].map(patient_names)
                st.dataframe(df_appointments, use_container_width=True)
            else:
                st.info("No appointments yet")
    
    # ==================== HEALTH ANALYTICS ====================
    elif menu == "📈 Analytics":
        st.header("📊 Health Trends Analytics")
        
        if st.session_state.vitals:
            patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
            selected_patient = st.selectbox("Select Patient", list(patient_names.keys()), format_func=lambda x: f"{x} - {patient_names[x]}")
            
            df = pd.DataFrame(st.session_state.vitals)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            df_patient = df[df['patient_id'] == selected_patient]
            
            if not df_patient.empty:
                st.subheader(f"❤️ Blood Pressure - {patient_names[selected_patient]}")
                fig_bp = go.Figure()
                fig_bp.add_trace(go.Scatter(x=df_patient['date'], y=df_patient['bp_systolic'], name='Systolic', line=dict(color='red')))
                fig_bp.add_trace(go.Scatter(x=df_patient['date'], y=df_patient['bp_diastolic'], name='Diastolic', line=dict(color='blue')))
                fig_bp.update_layout(title="Blood Pressure Trend", xaxis_title="Date", yaxis_title="mmHg")
                st.plotly_chart(fig_bp, use_container_width=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    fig_hr = px.line(df_patient, x='date', y='heart_rate', title="Heart Rate")
                    st.plotly_chart(fig_hr, use_container_width=True)
                with col2:
                    fig_sugar = px.line(df_patient, x='date', y='blood_sugar', title="Blood Sugar")
                    st.plotly_chart(fig_sugar, use_container_width=True)
        else:
            st.warning("No vitals data available")
    
    # ==================== REPORTS ====================
    elif menu == "📄 Reports":
        st.header("📄 Generate Patient Health Reports")
        
        if not st.session_state.patients:
            st.warning("No patients registered")
        else:
            patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
            selected_patient = st.selectbox("Select Patient", list(patient_names.keys()), format_func=lambda x: f"{x} - {patient_names[x]}")
            
            if st.button("📋 Generate Report"):
                patient = next((p for p in st.session_state.patients if p['patient_id'] == selected_patient), None)
                patient_vitals = [v for v in st.session_state.vitals if v['patient_id'] == selected_patient]
                patient_meds = [m for m in st.session_state.medications if m['patient_id'] == selected_patient]
                
                report = f"""
                ========================================
                ICT IN HEALTH - PATIENT HEALTH REPORT
                ========================================
                
                PATIENT: {patient.get('name', 'N/A')} (ID: {selected_patient})
                Age: {patient.get('age', 'N/A')} | Gender: {patient.get('gender', 'N/A')}
                Contact: {patient.get('contact', 'N/A')}
                Registered: {patient.get('registration_date', 'N/A')}
                
                VITAL SIGNS HISTORY
                -------------------
                """
                for v in patient_vitals[-10:]:
                    report += f"""
                {v['date']}: BP {v['bp_systolic']}/{v['bp_diastolic']}, HR {v['heart_rate']}, BS {v['blood_sugar']}mg/dL, Wt {v['weight']}kg"""
                
                report += f"""
                
                MEDICATIONS
                -----------
                """
                for m in patient_meds:
                    report += f"""
                {m['med_name']}: {m['dosage']} ({m['frequency']}) | {m['start_date']} to {m['end_date']}"""
                
                report += f"""
                
                Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                ========================================
                """
                
                st.text_area("Report", report, height=400)
                b64 = base64.b64encode(report.encode()).decode()
                href = f'<a href="data:text/plain;base64,{b64}" download="report_{selected_patient}.txt">📥 Download Report</a>'
                st.markdown(href, unsafe_allow_html=True)
    
    # ==================== BACKUP/RESTORE ====================
    elif menu == "💾 Backup":
        st.header("💾 Backup & Restore Data")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create Backup ZIP"):
                import zipfile, io
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    for file in os.listdir(DATA_FOLDER):
                        zip_file.write(os.path.join(DATA_FOLDER, file), file)
                b64 = base64.b64encode(zip_buffer.getvalue()).decode()
                href = f'<a href="data:application/zip;base64,{b64}" download="backup.zip">📥 Download Backup</a>'
                st.markdown(href, unsafe_allow_html=True)
                st.success("Backup created!")
        
        with col2:
            uploaded = st.file_uploader("Restore Backup", type=['zip'])
            if uploaded:
                import zipfile, io
                with zipfile.ZipFile(io.BytesIO(uploaded.read()), 'r') as zf:
                    zf.extractall(DATA_FOLDER)
                st.session_state.patients = load_patients()
                st.session_state.vitals = load_vitals()
                st.session_state.medications = load_medications()
                st.session_state.appointments = load_appointments()
                st.success("Restored! Refresh page.")
                st.rerun()
    
    # ==================== AI ASSISTANT ====================
    elif menu == "🤖 AI Assistant":
        chatbot_ui()
    
    # ==================== ABOUT ====================
    elif menu == "ℹ️ About":
        st.header("🌐 ICT in Health")
        st.markdown("""
        **Information & Communication Technology in Healthcare**
        
        **Features:**
        - Secure Admin & Patient Portals
        - Complete Medical Records Management
        - AI Health Assistant
        - Health Analytics Dashboard
        - Report Generation
        
        **Access:**
        - **Admin**: Full access to all data
        - **Patient**: View only their own records
        """)

# ==================== PATIENT PORTAL ====================

def show_patient_portal():
    """Patient view - see ONLY their own data"""
    
    show_patient_top_navbar()
    
    patient_id = st.session_state.current_patient_id
    patient_name = st.session_state.current_patient_name
    
    st.title(f"🏥 Welcome, {patient_name}!")
    st.markdown("*Your Personal Health Dashboard*")
    
    patient_vitals, patient_meds, patient_appointments = get_patient_data(patient_id)
    
    menu = st.session_state.selected_menu
    
    if menu == "📊 Dashboard":
        st.header("📊 Your Health Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Vitals", len(patient_vitals))
        with col2:
            st.metric("💊 Medications", len([m for m in patient_meds if m.get('status') == 'active']))
        with col3:
            st.metric("📅 Appointments", len(patient_appointments))
        with col4:
            if patient_vitals:
                last = patient_vitals[-1]
                st.metric("Latest BP", f"{last['bp_systolic']}/{last['bp_diastolic']}")
        
        if patient_vitals:
            df = pd.DataFrame(patient_vitals[-5:])
            st.dataframe(df[['date', 'bp_systolic', 'bp_diastolic', 'heart_rate', 'blood_sugar']], use_container_width=True)
        else:
            st.info("No vitals recorded yet.")
    
    elif menu == "📊 My Vitals":
        st.header("🩺 Your Vitals")
        if patient_vitals:
            df = pd.DataFrame(patient_vitals)
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="my_vitals.csv">📥 Export CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("No vitals found.")
    
    elif menu == "💊 My Meds":
        st.header("💊 Your Medications")
        if patient_meds:
            df = pd.DataFrame(patient_meds)
            st.dataframe(df[['med_name', 'dosage', 'frequency', 'start_date', 'end_date', 'status']], use_container_width=True)
        else:
            st.info("No medications prescribed.")
    
    elif menu == "📅 Appointments":
        st.header("📅 Your Appointments")
        if patient_appointments:
            df = pd.DataFrame(patient_appointments)
            st.dataframe(df[['date_time', 'doctor', 'reason', 'status']], use_container_width=True)
        else:
            st.info("No appointments scheduled.")
    
    elif menu == "📈 Analytics":
        st.header("📊 Your Health Trends")
        if len(patient_vitals) > 1:
            df = pd.DataFrame(patient_vitals)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            fig_bp = go.Figure()
            fig_bp.add_trace(go.Scatter(x=df['date'], y=df['bp_systolic'], name='Systolic'))
            fig_bp.add_trace(go.Scatter(x=df['date'], y=df['bp_diastolic'], name='Diastolic'))
            fig_bp.update_layout(title="Blood Pressure Trend")
            st.plotly_chart(fig_bp, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                fig_hr = px.line(df, x='date', y='heart_rate', title="Heart Rate")
                st.plotly_chart(fig_hr, use_container_width=True)
            with col2:
                fig_sugar = px.line(df, x='date', y='blood_sugar', title="Blood Sugar")
                st.plotly_chart(fig_sugar, use_container_width=True)
        else:
            st.warning("Need at least 2 vitals records for trends")
    
    elif menu == "📄 Reports":
        st.header("📄 Your Health Report")
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
                report += f"\n{m['med_name']}: {m['dosage']} ({m['frequency']})"
            
            st.text_area("Report", report, height=300)
            b64 = base64.b64encode(report.encode()).decode()
            href = f'<a href="data:text/plain;base64,{b64}" download="my_report.txt">📥 Download Report</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    elif menu == "🤖 AI Assistant":
        chatbot_ui()
    
    elif menu == "ℹ️ About":
        st.header("ℹ️ About Your Portal")
        st.markdown("View your medical records, track vitals, and manage appointments.")

# ==================== MAIN APP ====================

def main():
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.user_type == "admin":
            show_admin_dashboard()
        elif st.session_state.user_type == "patient":
            show_patient_portal()

if __name__ == "__main__":
    main()
