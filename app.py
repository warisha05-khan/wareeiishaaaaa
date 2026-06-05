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
