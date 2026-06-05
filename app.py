"""
ICT in Health - Hospital Management System
Features: Patient Management, Vitals Logger, Medication Reminders, Reports
Author: ICT Health Project
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="ICT Health | Hospital Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stButton button {
        background-color: #1f6e4a;
        color: white;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #0f533a;
    }
    .css-1kyxreq {
        background-color: #f0f7f4;
    }
    .report-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f6e4a;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
def init_session_state():
    if 'patients' not in st.session_state:
        st.session_state.patients = {}
    if 'vitals' not in st.session_state:
        st.session_state.vitals = []
    if 'medications' not in st.session_state:
        st.session_state.medications = []
    if 'appointments' not in st.session_state:
        st.session_state.appointments = []
    if 'reminders' not in st.session_state:
        st.session_state.reminders = []

init_session_state()

# ==================== HELPER FUNCTIONS ====================

def add_patient(patient_id, name, age, gender, contact, address):
    st.session_state.patients[patient_id] = {
        'name': name,
        'age': age,
        'gender': gender,
        'contact': contact,
        'address': address,
        'registration_date': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    return True

def add_vitals(patient_id, bp_sys, bp_dia, heart_rate, blood_sugar, weight, notes=""):
    st.session_state.vitals.append({
        'patient_id': patient_id,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'bp_systolic': bp_sys,
        'bp_diastolic': bp_dia,
        'heart_rate': heart_rate,
        'blood_sugar': blood_sugar,
        'weight': weight,
        'notes': notes
    })

def add_medication(patient_id, med_name, dosage, frequency, start_date, end_date):
    st.session_state.medications.append({
        'patient_id': patient_id,
        'med_name': med_name,
        'dosage': dosage,
        'frequency': frequency,
        'start_date': start_date,
        'end_date': end_date,
        'status': 'active'
    })

def add_appointment(patient_id, doctor, date_time, reason):
    st.session_state.appointments.append({
        'patient_id': patient_id,
        'doctor': doctor,
        'date_time': date_time,
        'reason': reason,
        'status': 'scheduled'
    })

def generate_patient_report(patient_id):
    patient = st.session_state.patients.get(patient_id, {})
    patient_vitals = [v for v in st.session_state.vitals if v['patient_id'] == patient_id]
    patient_meds = [m for m in st.session_state.medications if m['patient_id'] == patient_id]
    
    report = f"""
    ========================================
    ICT IN HEALTH - PATIENT HEALTH REPORT
    ========================================
    
    PATIENT INFORMATION
    -------------------
    Patient ID: {patient_id}
    Name: {patient.get('name', 'N/A')}
    Age: {patient.get('age', 'N/A')}
    Gender: {patient.get('gender', 'N/A')}
    Contact: {patient.get('contact', 'N/A')}
    Registration Date: {patient.get('registration_date', 'N/A')}
    
    VITAL SIGNS HISTORY
    -------------------
    """
    
    for v in patient_vitals[-5:]:  # Last 5 records
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
    
    report += """
    
    ========================================
    Report Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
    ========================================
    """
    return report

# ==================== MAIN UI ====================

st.title("🏥 ICT in Health - Hospital Management System")
st.markdown("*Information & Communication Technology for Better Healthcare Delivery*")

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/000000/hospital.png", width=80)
st.sidebar.title("📋 Navigation")
menu = st.sidebar.selectbox(
    "Choose Module",
    ["🏠 Dashboard", "👨‍👩‍👧 Patient Registration", "📊 Vitals Logger", 
     "💊 Medication Manager", "📅 Appointments", "🔔 Reminders", 
     "📈 Health Analytics", "📄 Reports", "ℹ️ About ICT in Health"]
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
        st.metric("💊 Active Medications", len([m for m in st.session_state.medications if m['status'] == 'active']))
    with col4:
        st.metric("📅 Upcoming Appointments", len([a for a in st.session_state.appointments if a['status'] == 'scheduled']))
    
    st.subheader("📈 Recent Activity")
    
    if st.session_state.vitals:
        df_vitals = pd.DataFrame(st.session_state.vitals[-10:])
        st.dataframe(df_vitals[['date', 'patient_id', 'bp_systolic', 'bp_diastolic', 'heart_rate']], use_container_width=True)
    else:
        st.info("No vitals recorded yet. Go to Vitals Logger to add data.")
    
    st.subheader("🏥 ICT Features Active")
    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ Digital Patient Records")
        st.success("✅ Real-time Vitals Tracking")
        st.success("✅ Medication Reminders")
    with col2:
        st.success("✅ Automated Reports")
        st.success("✅ Appointment Scheduling")
        st.success("✅ Health Analytics")

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
                if add_patient(patient_id, name, age, gender, contact, address):
                    st.success(f"✅ Patient {name} registered successfully!")
                else:
                    st.error("Registration failed")
            else:
                st.warning("Please fill all required fields")
    
    st.subheader("📋 Registered Patients")
    if st.session_state.patients:
        df_patients = pd.DataFrame.from_dict(st.session_state.patients, orient='index')
        st.dataframe(df_patients, use_container_width=True)
    else:
        st.info("No patients registered yet")

# ==================== VITALS LOGGER ====================
elif menu == "📊 Vitals Logger":
    st.header("🩺 Record Patient Vitals")
    
    if not st.session_state.patients:
        st.warning("Please register patients first!")
    else:
        with st.form("vitals_form"):
            patient_id = st.selectbox("Select Patient", list(st.session_state.patients.keys()))
            col1, col2, col3 = st.columns(3)
            with col1:
                bp_sys = st.number_input("Systolic BP (mmHg)", min_value=50, max_value=250)
                bp_dia = st.number_input("Diastolic BP (mmHg)", min_value=30, max_value=150)
            with col2:
                heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200)
                blood_sugar = st.number_input("Blood Sugar (mg/dL)", min_value=0, max_value=600)
            with col3:
                weight = st.number_input("Weight (kg)", min_value=0, max_value=300)
            notes = st.text_area("Additional Notes")
            
            submitted = st.form_submit_button("Save Vitals")
            
            if submitted:
                add_vitals(patient_id, bp_sys, bp_dia, heart_rate, blood_sugar, weight, notes)
                st.success("✅ Vitals recorded successfully!")
                st.balloons()
    
    # Display vitals history
    st.subheader("📋 Recent Vitals Records")
    if st.session_state.vitals:
        df_vitals = pd.DataFrame(st.session_state.vitals)
        st.dataframe(df_vitals, use_container_width=True)
    else:
        st.info("No vitals recorded yet")

# ==================== MEDICATION MANAGER ====================
elif menu == "💊 Medication Manager":
    st.header("💊 Prescription & Medication Tracker")
    
    if not st.session_state.patients:
        st.warning("Please register patients first!")
    else:
        with st.form("medication_form"):
            patient_id = st.selectbox("Select Patient", list(st.session_state.patients.keys()))
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
                add_medication(patient_id, med_name, dosage, frequency, str(start_date), str(end_date))
                st.success(f"✅ {med_name} prescribed successfully!")
        
        # Display active medications
        st.subheader("💊 Active Prescriptions")
        active_meds = [m for m in st.session_state.medications if m['status'] == 'active']
        if active_meds:
            df_meds = pd.DataFrame(active_meds)
            st.dataframe(df_meds, use_container_width=True)
        else:
            st.info("No active prescriptions")

# ==================== APPOINTMENTS ====================
elif menu == "📅 Appointments":
    st.header("📅 Schedule Appointments")
    
    if not st.session_state.patients:
        st.warning("Please register patients first!")
    else:
        with st.form("appointment_form"):
            patient_id = st.selectbox("Select Patient", list(st.session_state.patients.keys()))
            doctor = st.text_input("Doctor Name")
            appointment_date = st.datetime_input("Appointment Date & Time")
            reason = st.text_area("Reason for Visit")
            
            submitted = st.form_submit_button("Schedule Appointment")
            
            if submitted:
                add_appointment(patient_id, doctor, str(appointment_date), reason)
                st.success(f"✅ Appointment scheduled for {appointment_date}")
        
        st.subheader("📋 Upcoming Appointments")
        if st.session_state.appointments:
            df_appointments = pd.DataFrame(st.session_state.appointments)
            st.dataframe(df_appointments, use_container_width=True)
        else:
            st.info("No appointments scheduled")

# ==================== REMINDERS ====================
elif menu == "🔔 Reminders":
    st.header("🔔 Medication & Health Reminders")
    
    st.info("💡 ICT Feature: Automated reminders improve medication adherence by 40%")
    
    col1, col2 = st.columns(2)
    with col1:
        reminder_time = st.time_input("Daily Reminder Time", value=datetime.strptime("09:00", "%H:%M").time())
        st.success(f"⏰ Daily reminder set for {reminder_time}")
    
    with col2:
        st.subheader("📱 Reminder Methods")
        st.checkbox("📧 Email Reminders", value=True)
        st.checkbox("📱 SMS Reminders")
        st.checkbox("🔔 Browser Notifications", value=True)
    
    st.subheader("💊 Medication Reminders")
    for med in st.session_state.medications:
        if med['status'] == 'active':
            st.write(f"• Take {med['med_name']} ({med['dosage']}) - {med['frequency']}")

# ==================== HEALTH ANALYTICS ====================
elif menu == "📈 Health Analytics":
    st.header("📊 Health Trends Analytics")
    
    if st.session_state.vitals:
        df = pd.DataFrame(st.session_state.vitals)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # BP Trends
        st.subheader("❤️ Blood Pressure Trends")
        fig_bp = go.Figure()
        fig_bp.add_trace(go.Scatter(x=df['date'], y=df['bp_systolic'], name='Systolic', line=dict(color='red')))
        fig_bp.add_trace(go.Scatter(x=df['date'], y=df['bp_diastolic'], name='Diastolic', line=dict(color='blue')))
        fig_bp.update_layout(title="Blood Pressure Over Time", xaxis_title="Date", yaxis_title="mmHg")
        st.plotly_chart(fig_bp, use_container_width=True)
        
        # Heart Rate & Blood Sugar
        col1, col2 = st.columns(2)
        with col1:
            fig_hr = px.line(df, x='date', y='heart_rate', title="Heart Rate Trend", color_discrete_sequence=['green'])
            st.plotly_chart(fig_hr, use_container_width=True)
        with col2:
            fig_sugar = px.line(df, x='date', y='blood_sugar', title="Blood Sugar Trend", color_discrete_sequence=['orange'])
            st.plotly_chart(fig_sugar, use_container_width=True)
        
        # Summary Statistics
        st.subheader("📊 Health Summary")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Systolic BP", f"{df['bp_systolic'].mean():.0f} mmHg")
            st.metric("Avg Diastolic BP", f"{df['bp_diastolic'].mean():.0f} mmHg")
        with col2:
            st.metric("Avg Heart Rate", f"{df['heart_rate'].mean():.0f} bpm")
            st.metric("Avg Blood Sugar", f"{df['blood_sugar'].mean():.0f} mg/dL")
    else:
        st.warning("No vitals data available for analytics")

# ==================== REPORTS ====================
elif menu == "📄 Reports":
    st.header("📄 Generate Patient Health Reports")
    
    if not st.session_state.patients:
        st.warning("No patients registered")
    else:
        patient_id = st.selectbox("Select Patient", list(st.session_state.patients.keys()))
        
        if st.button("📋 Generate Complete Health Report"):
            report = generate_patient_report(patient_id)
            st.text_area("Report Preview", report, height=400)
            
            # Download button for report
            b64 = base64.b64encode(report.encode()).decode()
            href = f'<a href="data:text/plain;base64,{b64}" download="patient_report_{patient_id}.txt">📥 Download Report (TXT)</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            st.success("✅ Report generated successfully! Can be shared with patient/doctor.")

# ==================== ABOUT ICT ====================
elif menu == "ℹ️ About ICT in Health":
    st.header("🌐 Information & Communication Technology (ICT) in Health")
    
    st.markdown("""
    ### What is ICT in Health?
    
    ICT in Health (also known as eHealth or Digital Health) refers to the use of information and communication technologies for health-related purposes.
    
    ### Key Benefits Demonstrated in This System:
    
    | ICT Application | Benefit |
    |----------------|---------|
    | Digital Patient Records | Instant access to patient history |
    | Real-time Vitals Logging | Early detection of health deterioration |
    | Medication Reminders | 40% improvement in adherence |
    | Automated Reports | Better doctor-patient communication |
    | Health Analytics | Data-driven clinical decisions |
    | Appointment Scheduling | Reduced wait times |
    
    ### WHO Recommendations:
    - Digital health interventions can improve health outcomes
    - Patient-generated data enhances clinical decision-making
    - ICT reduces healthcare costs and improves access
    
    ### Technologies Used:
    - 🐍 Python + Streamlit (Frontend & Backend)
    - 📊 Plotly (Interactive Charts)
    - 🗃️ Session State (In-memory data storage)
    - ☁️ Deployable via GitHub + Streamlit Cloud
    """)

# ==================== FOOTER ====================
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **🏥 ICT in Health Project**
    
    Features:
    - Patient Management
    - Vitals Tracking
    - Medication Reminders
    - Health Reports
    - Analytics Dashboard
    
    *Data stored in session only*
    """
)

# Display current time
st.sidebar.caption(f"🕐 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
