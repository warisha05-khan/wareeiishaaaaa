"""
ICT in Health - Hospital Management System
With Secure Login: Admin Portal + Patient Portal
All existing features preserved with role-based access
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

# Simple password hashing (for demo - use proper auth in production)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("12345")

# File storage for patient login credentials
CREDENTIALS_FILE = "hospital_data/patient_credentials.csv"

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

init_auth()

def save_patient_credentials(patient_id, password):
    """Save patient login credentials"""
    import pandas as pd
    os.makedirs("hospital_data", exist_ok=True)
    
    hashed_pwd = hash_password(password)
    
    if os.path.exists(CREDENTIALS_FILE):
        df = pd.read_csv(CREDENTIALS_FILE)
        # Check if patient already exists
        if patient_id in df['patient_id'].values:
            df.loc[df['patient_id'] == patient_id, 'password_hash'] = hashed_pwd
        else:
            new_entry = pd.DataFrame([{'patient_id': patient_id, 'password_hash': hashed_pwd}])
            df = pd.concat([df, new_entry], ignore_index=True)
    else:
        df = pd.DataFrame([{'patient_id': patient_id, 'password_hash': hashed_pwd}])
    
    df.to_csv(CREDENTIALS_FILE, index=False)

def verify_patient_credentials(patient_id, password):
    """Verify patient login credentials"""
    if not os.path.exists(CREDENTIALS_FILE):
        return False
    
    df = pd.read_csv(CREDENTIALS_FILE)
    patient_data = df[df['patient_id'] == patient_id]
    
    if patient_data.empty:
        return False
    
    stored_hash = patient_data.iloc[0]['password_hash']
    return stored_hash == hash_password(password)

def login_admin(username, password):
    return username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH

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

def add_patient(patient_id, name, age, gender, contact, address, password):
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
    save_patient_credentials(patient_id, password)
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
    
    # Custom CSS for login page
    st.markdown("""
    <style>
    .login-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
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
            st.markdown("### 🔐 Patient Portal")
            patient_id = st.text_input("Patient ID", key="patient_id", placeholder="Enter your Patient ID")
            patient_password = st.text_input("Password", type="password", key="patient_pass", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔐 Login as Patient", key="patient_login"):
                    if verify_patient_credentials(patient_id, patient_password):
                        # Verify patient exists
                        patient_exists = any(p['patient_id'] == patient_id for p in st.session_state.patients)
                        if patient_exists:
                            st.session_state.logged_in = True
                            st.session_state.user_type = "patient"
                            st.session_state.current_patient_id = patient_id
                            patient = next((p for p in st.session_state.patients if p['patient_id'] == patient_id), None)
                            st.session_state.current_patient_name = patient['name'] if patient else patient_id
                            st.rerun()
                        else:
                            st.error("❌ Patient ID not found!")
                    else:
                        st.error("❌ Invalid credentials!")
            
            with col2:
                st.markdown("""
                <div style="background: #f0f2f5; padding: 15px; border-radius: 10px; margin-top: 10px;">
                    <small>⚠️ <strong>New Patient?</strong><br>
                    Register using the admin panel.<br>
                    You will create your password during registration.</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<center><small>© 2026 ICT in Health | Secure Hospital Management System</small></center>", unsafe_allow_html=True)

# ==================== LOGOUT ====================

def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.current_patient_id = None
    st.session_state.current_patient_name = None
    st.rerun()

# ==================== ADMIN DASHBOARD ====================

def show_admin_dashboard():
    """Admin view - can see ALL patient data"""
    
    # Sidebar with logout
    st.sidebar.button("🚪 Logout", on_click=logout, use_container_width=True)
    st.sidebar.markdown(f"---")
    st.sidebar.success(f"✅ Logged in as: **Admin**")
    
    st.title("🏥 ICT in Health - Hospital Management System")
    st.markdown("*Admin Dashboard - Complete Patient Data Access*")
    
    # Sidebar Navigation
    st.sidebar.title("📋 Navigation")
    menu = st.sidebar.selectbox(
        "Choose Module",
        ["📊 Dashboard", "👨‍👩‍👧 Patient Registration", "📊 Vitals Logger", 
         "💊 Medication Manager", "📅 Appointments", "📈 Health Analytics", 
         "📄 Reports", "💾 Backup/Restore", "🤖 AI Health Assistant", 
         "ℹ️ About ICT in Health"]
    )
    
    # Display all patients in sidebar for quick access
    if st.session_state.patients:
        st.sidebar.markdown("---")
        st.sidebar.subheader("👥 All Patients")
        patient_list = {p['patient_id']: p['name'] for p in st.session_state.patients}
        selected_patient_for_view = st.sidebar.selectbox("Select Patient to View", list(patient_list.keys()), format_func=lambda x: f"{x} - {patient_list[x]}")
        
        if selected_patient_for_view:
            st.sidebar.info(f"👤 Viewing: {patient_list[selected_patient_for_view]}")
    
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
        
        # Recent Patients Table
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
    elif menu == "👨‍👩‍👧 Patient Registration":
        st.header("📝 Register New Patient")
        
        with st.form("patient_registration"):
            col1, col2 = st.columns(2)
            with col1:
                patient_id = st.text_input("Patient ID (Unique)")
                name = st.text_input("Full Name")
                age = st.number_input("Age", min_value=0, max_value=150)
                password = st.text_input("Create Patient Portal Password", type="password", help="Patient will use this to login")
            with col2:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                contact = st.text_input("Contact Number")
                address = st.text_area("Address")
            
            submitted = st.form_submit_button("Register Patient")
            
            if submitted:
                if patient_id and name and password:
                    existing_ids = [p['patient_id'] for p in st.session_state.patients]
                    if patient_id in existing_ids:
                        st.error(f"❌ Patient ID {patient_id} already exists!")
                    else:
                        add_patient(patient_id, name, age, gender, contact, address, password)
                        st.success(f"✅ Patient {name} registered successfully!")
                        st.info(f"📝 Patient Portal Credentials:\n\n**Patient ID:** {patient_id}\n**Password:** [Hidden for security]")
                        st.balloons()
                else:
                    st.warning("Please fill all required fields (including password)")
        
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
    elif menu == "💊 Medication Manager":
        st.header("💊 Prescription & Medication Tracker")
        
        if not st.session_state.patients:
            st.warning("Please register patients first!")
        else:
            patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
            selected_patient = st.selectbox("Select Patient", list(patient_names.keys()), format_func=lambda x: f"{x} - {patient_names[x]}")
            
            with st.form("medication_form"):
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
                    st.success(f"✅ Appointment scheduled for {appointment_date}")
            
            st.subheader("📋 All Appointments")
            if st.session_state.appointments:
                df_appointments = pd.DataFrame(st.session_state.appointments)
                df_appointments['patient_name'] = df_appointments['patient_id'].map(patient_names)
                st.dataframe(df_appointments, use_container_width=True)
            else:
                st.info("No appointments yet")
    
    # ==================== HEALTH ANALYTICS ====================
    elif menu == "📈 Health Analytics":
        st.header("📊 Health Trends Analytics")
        
        if st.session_state.vitals:
            # Select patient for analytics
            patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
            selected_patient = st.selectbox("Select Patient for Analytics", list(patient_names.keys()), format_func=lambda x: f"{x} - {patient_names[x]}")
            
            df = pd.DataFrame(st.session_state.vitals)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            df_patient = df[df['patient_id'] == selected_patient]
            
            if not df_patient.empty:
                st.subheader(f"❤️ Blood Pressure Trends - {patient_names[selected_patient]}")
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
                st.info("No vitals data for selected patient")
        else:
            st.warning("No vitals data available for analytics")
    
    # ==================== REPORTS ====================
    elif menu == "📄 Reports":
        st.header("📄 Generate Patient Health Reports")
        
        if not st.session_state.patients:
            st.warning("No patients registered")
        else:
            patient_names = {p['patient_id']: p['name'] for p in st.session_state.patients}
            selected_patient = st.selectbox("Select Patient", list(patient_names.keys()), format_func=lambda x: f"{x} - {patient_names[x]}")
            
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
                
                for v in patient_vitals[-10:]:
                    report += f"""
                Date: {v['date']}
                - Blood Pressure: {v['bp_systolic']}/{v['bp_diastolic']} mmHg
                - Heart Rate: {v['heart_rate']} bpm
                - Blood Sugar: {v['blood_sugar']} mg/dL
                - Weight: {v['weight']} kg
                """
                
                report += f"""
                
                MEDICATION HISTORY
                ------------------
                """
                for m in patient_meds:
                    report += f"""
                - {m['med_name']}: {m['dosage']} ({m['frequency']})
                  Duration: {m['start_date']} to {m['end_date']}
                  Status: {m.get('status', 'active')}
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
    
    # ==================== AI HEALTH ASSISTANT ====================
    elif menu == "🤖 AI Health Assistant":
        chatbot_ui()
    
    # ==================== ABOUT ====================
    elif menu == "ℹ️ About ICT in Health":
        st.header("🌐 Information & Communication Technology (ICT) in Health")
        
        st.markdown("""
        ### What is ICT in Health?
        
        ICT in Health (eHealth/Digital Health) uses technology for health-related purposes.
        
        ### System Features:
        - ✅ **Secure Login** - Admin and Patient portals
        - ✅ **Patient Data Privacy** - Patients see only their own data
        - ✅ **Complete Medical Records** - Vitals, medications, appointments
        - ✅ **AI Health Assistant** - Educational health information
        - ✅ **Analytics Dashboard** - Visual health trends
        - ✅ **Report Generation** - Share with doctors
        
        ### Access Levels:
        - **Admin**: View all patients, add/edit all data
        - **Patient**: View only their own medical history
        
        ### Technologies Used:
        - Streamlit (Frontend)
        - CSV Files (Storage)
        - Plotly (Charts)
        - Pandas (Data manipulation)
        - Google Gemini AI (Health Assistant Chatbot)
        """)

# ==================== PATIENT PORTAL ====================

def show_patient_portal():
    """Patient view - see ONLY their own data"""
    
    patient_id = st.session_state.current_patient_id
    patient_name = st.session_state.current_patient_name
    
    # Sidebar with logout
    st.sidebar.button("🚪 Logout", on_click=logout, use_container_width=True)
    st.sidebar.markdown(f"---")
    st.sidebar.success(f"✅ Logged in as: **{patient_name}**")
    st.sidebar.info(f"🆔 Patient ID: {patient_id}")
    
    st.title(f"🏥 Welcome, {patient_name}!")
    st.markdown("*Your Personal Health Dashboard*")
    
    # Get patient's data
    patient_vitals, patient_meds, patient_appointments = get_patient_data(patient_id)
    
    # Sidebar Navigation for patient
    st.sidebar.title("📋 Your Records")
    menu = st.sidebar.selectbox(
        "Choose Module",
        ["📊 My Dashboard", "📊 My Vitals", "💊 My Medications", 
         "📅 My Appointments", "📈 My Health Analytics", 
         "📄 My Reports", "🤖 AI Health Assistant", "ℹ️ About"]
    )
    
    if menu == "📊 My Dashboard":
        st.header("📊 Your Health Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Vitals Records", len(patient_vitals))
        with col2:
            st.metric("💊 Active Medications", len([m for m in patient_meds if m.get('status') == 'active']))
        with col3:
            st.metric("📅 Appointments", len(patient_appointments))
        with col4:
            if patient_vitals:
                last_bp = patient_vitals[-1]
                st.metric("Latest BP", f"{last_bp['bp_systolic']}/{last_bp['bp_diastolic']}")
            else:
                st.metric("Latest BP", "N/A")
        
        if patient_vitals:
            st.subheader("📋 Your Recent Vitals")
            df_vitals = pd.DataFrame(patient_vitals[-5:])
            st.dataframe(df_vitals[['date', 'bp_systolic', 'bp_diastolic', 'heart_rate', 'blood_sugar']], use_container_width=True)
        else:
            st.info("No vitals recorded yet. Visit the clinic to add your health data.")
    
    elif menu == "📊 My Vitals":
        st.header("🩺 Your Vitals History")
        if patient_vitals:
            df_vitals = pd.DataFrame(patient_vitals)
            st.dataframe(df_vitals, use_container_width=True)
            
            # Export option
            csv = df_vitals.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="my_vitals.csv">📥 Export My Vitals to CSV</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("No vitals records found for you.")
    
    elif menu == "💊 My Medications":
        st.header("💊 Your Medications")
        if patient_meds:
            df_meds = pd.DataFrame(patient_meds)
            st.dataframe(df_meds[['med_name', 'dosage', 'frequency', 'start_date', 'end_date', 'status']], use_container_width=True)
        else:
            st.info("No medications prescribed yet.")
    
    elif menu == "📅 My Appointments":
        st.header("📅 Your Appointments")
        if patient_appointments:
            df_appointments = pd.DataFrame(patient_appointments)
            st.dataframe(df_appointments[['date_time', 'doctor', 'reason', 'status']], use_container_width=True)
        else:
            st.info("No appointments scheduled yet.")
    
    elif menu == "📈 My Health Analytics":
        st.header("📊 Your Health Trends")
        
        if patient_vitals:
            df = pd.DataFrame(patient_vitals)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            st.subheader("❤️ Your Blood Pressure Trends")
            fig_bp = go.Figure()
            fig_bp.add_trace(go.Scatter(x=df['date'], y=df['bp_systolic'], name='Systolic', line=dict(color='red')))
            fig_bp.add_trace(go.Scatter(x=df['date'], y=df['bp_diastolic'], name='Diastolic', line=dict(color='blue')))
            fig_bp.update_layout(title="Blood Pressure Over Time", xaxis_title="Date", yaxis_title="mmHg")
            st.plotly_chart(fig_bp, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                fig_hr = px.line(df, x='date', y='heart_rate', title="Your Heart Rate Trend")
                st.plotly_chart(fig_hr, use_container_width=True)
            with col2:
                fig_sugar = px.line(df, x='date', y='blood_sugar', title="Your Blood Sugar Trend")
                st.plotly_chart(fig_sugar, use_container_width=True)
        else:
            st.warning("No vitals data available for analytics")
    
    elif menu == "📄 My Reports":
        st.header("📄 Your Health Report")
        
        if st.button("📋 Generate My Health Report"):
            report = f"""
            ========================================
            ICT IN HEALTH - PATIENT HEALTH REPORT
            ========================================
            
            PATIENT INFORMATION
            -------------------
            Patient ID: {patient_id}
            Name: {patient_name}
            
            YOUR VITAL SIGNS HISTORY
            -------------------------
            """
            
            for v in patient_vitals[-10:]:
                report += f"""
            Date: {v['date']}
            - BP: {v['bp_systolic']}/{v['bp_diastolic']} mmHg
            - Heart Rate: {v['heart_rate']} bpm
            - Blood Sugar: {v['blood_sugar']} mg/dL
            - Weight: {v['weight']} kg
            """
            
            report += f"""
            
            YOUR MEDICATIONS
            ----------------
            """
            for m in patient_meds:
                report += f"""
            - {m['med_name']}: {m['dosage']} ({m['frequency']})
            """
            
            report += f"""
            
            ========================================
            Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            ========================================
            """
            
            st.text_area("Your Report", report, height=400)
            
            b64 = base64.b64encode(report.encode()).decode()
            href = f'<a href="data:text/plain;base64,{b64}" download="my_health_report.txt">📥 Download My Report</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            st.success("✅ Report generated successfully!")
    
    elif menu == "🤖 AI Health Assistant":
        chatbot_ui()
    
    elif menu == "ℹ️ About":
        st.header("ℹ️ About Your Patient Portal")
        st.markdown("""
        ### Your Personal Health Portal
        
        Here you can:
        - ✅ View all your medical records
        - ✅ Track your vitals over time
        - ✅ See your prescribed medications
        - ✅ Check your appointments
        - ✅ Download your health reports
        - ✅ Chat with our AI Health Assistant
        
        ### Privacy & Security
        Your data is stored securely and only you can access your records.
        Always consult a doctor for medical advice.
        """)

# ==================== MAIN APP ENTRY POINT ====================

def main():
    """Main app entry point - handles routing between login and dashboards"""
    
    if not st.session_state.logged_in:
        show_login_page()
    else:
        if st.session_state.user_type == "admin":
            show_admin_dashboard()
        elif st.session_state.user_type == "patient":
            show_patient_portal()

if __name__ == "__main__":
    main()
