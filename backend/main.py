from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
import os
import re
from typing import List, Dict, Any
from datetime import datetime

app = FastAPI(title="HMS Analytics Microservice")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to the CSV file - works on both local and Vercel environments
def get_data_file_path():
    """Find the CSV file in multiple possible locations."""
    possible_paths = [
        # Local development: CSV in parent of backend/
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'PatientAppointmentEntry.csv'),
        # Vercel: CSV in same directory as main.py (backend/)
        os.path.join(os.path.dirname(__file__), 'PatientAppointmentEntry.csv'),
        # Vercel fallback: Current working directory
        os.path.join(os.getcwd(), 'PatientAppointmentEntry.csv'),
        # Vercel fallback: Root of project
        '/var/task/PatientAppointmentEntry.csv',
        '/var/task/backend/PatientAppointmentEntry.csv',
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    # Return the first path as default (will show helpful error)
    return possible_paths[0]

DATA_FILE = get_data_file_path()


# ===================== HOME & INFO ROUTES =====================
@app.get("/")
def home():
    """Root endpoint - API information and available endpoints."""
    return {
        "message": "HMS Analytics API",
        "version": "1.0",
        "status": "running",
        "endpoints": {
            "home": "/",
            "insights": "/api/v1/analytics/doctor-patient-insights",
            "dashboard": "/api/v1/analytics/dashboard"
        },
        "description": "Hospital Management System Analytics Microservice providing doctor-patient insights and dashboard data."
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# ===================== DATA CLEANING FUNCTIONS =====================
def parse_age(age_str):
    """
    Parse age from various formats:
    - Numeric: "49", "45", "70"
    - With Y suffix: "6Y", "9Y", "3.3Y", "7Y", "5Y"  
    - With M suffix: "6M" (months)
    - Empty values
    """
    if pd.isna(age_str) or str(age_str).strip() == '':
        return None
    
    age_str = str(age_str).strip().upper()
    
    # Extract numeric part
    match = re.search(r"(\d+(\.\d+)?)", age_str)
    if match:
        val = float(match.group(1))
        # If 'M' is present (e.g. 6M), convert months to years
        if 'M' in age_str and 'Y' not in age_str:
            val = val / 12
        return val
    return None


def load_and_clean_data():
    """Load and clean the PatientAppointmentEntry.csv data."""
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Data file not found at: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    # --- Data Cleaning ---
    
    # 1. Strip whitespace from column names (handles trailing spaces like "Practitioner ")
    df.columns = df.columns.str.strip()
    
    # 2. Rename columns for consistency (flexible mapping)
    column_mapping = {
        'Practitioner': 'doctor_name',
        'Practitioner  Name': 'doctor_display_name',
        'Medical Department': 'department',
        'Appointment Date & Time': 'visit_datetime',
        'Paid Amount': 'revenue',
        'Company': 'branch',
        'Gender': 'gender',
        'Status': 'status',
        'Mode of Payment': 'payment_mode',
        'Patient': 'patient_id',
        'Patient Name': 'patient_name',
        'Age': 'age_raw',
        'Date Of Birth': 'dob',
        'ID': 'token_id',
        'Posting Date': 'posting_date',
        'Time': 'appointment_time',
        'Base Grand Total': 'base_total',
        'Advance Paid': 'advance_paid'
    }
    
    # Only rename columns that exist
    existing_cols = {k: v for k, v in column_mapping.items() if k in df.columns}
    df = df.rename(columns=existing_cols)

    # 3. Parse Dates
    if 'visit_datetime' in df.columns:
        # Format in CSV is "DD-MM-YY HH:MM" (e.g., "02-12-25 17:46")
        df['visit_datetime'] = pd.to_datetime(df['visit_datetime'], dayfirst=True, errors='coerce')
    
    if 'dob' in df.columns:
        df['dob'] = pd.to_datetime(df['dob'], dayfirst=True, errors='coerce')
    
    # 4. Clean Age
    if 'age_raw' in df.columns:
        df['age'] = df['age_raw'].apply(parse_age)
        # Fill missing ages with median if available
        median_age = df['age'].median()
        if pd.notna(median_age):
            df['age'] = df['age'].fillna(median_age)
        else:
            df['age'] = df['age'].fillna(0)
    else:
        df['age'] = 0
    
    # 5. Clean Numeric Columns
    if 'revenue' in df.columns:
        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce').fillna(0)
    else:
        df['revenue'] = 0
        
    if 'base_total' in df.columns:
        df['base_total'] = pd.to_numeric(df['base_total'], errors='coerce').fillna(0)
    
    if 'advance_paid' in df.columns:
        df['advance_paid'] = pd.to_numeric(df['advance_paid'], errors='coerce').fillna(0)

    # 6. Fill Missing Values
    df['doctor_name'] = df.get('doctor_name', pd.Series(['Unknown Doctor'] * len(df))).fillna("Unknown Doctor")
    df['department'] = df.get('department', pd.Series(['General'] * len(df))).fillna("General")
    df['branch'] = df.get('branch', pd.Series(['Unknown Branch'] * len(df))).fillna("Unknown Branch")
    df['gender'] = df.get('gender', pd.Series(['Unknown'] * len(df))).fillna("Unknown")
    df['payment_mode'] = df.get('payment_mode', pd.Series(['Unknown'] * len(df))).fillna("Unknown")
    df['status'] = df.get('status', pd.Series(['Unknown'] * len(df))).fillna("Unknown")
    df['patient_name'] = df.get('patient_name', pd.Series(['Unknown'] * len(df))).fillna("Unknown")

    return df


# ===================== ANALYTICS ENDPOINTS =====================
@app.get("/api/v1/analytics/doctor-patient-insights")
def get_insights():
    """Get doctor-patient analytics insights."""
    try:
        df = load_and_clean_data()
        
        insights = []
        
        # --- 1. Doctor Performance ---
        
        # Insight 1: Top 5 Busiest Doctors
        top_docs = df['doctor_name'].value_counts().head(5)
        insights.append({
            "title": "Top 5 Busiest Doctors",
            "description": "Doctors with the highest patient volume.",
            "chart_type": "bar",
            "chart_data": {"labels": top_docs.index.tolist(), "values": top_docs.values.tolist()}
        })
        
        # Insight 2: Visits by Department
        dept_counts = df['department'].value_counts()
        insights.append({
            "title": "Patient Visits by Department",
            "description": "Distribution of cases across different medical departments.",
            "chart_type": "pie",
            "chart_data": {"labels": dept_counts.index.tolist(), "values": dept_counts.values.tolist()}
        })
        
        # Insight 3: Revenue by Department (kept as requested)
        rev_dept = df.groupby('department')['revenue'].sum().sort_values(ascending=False)
        insights.append({
            "title": "Revenue by Department",
            "description": "Total revenue generated by each department.",
            "chart_type": "bar",
            "chart_data": {"labels": rev_dept.index.tolist(), "values": rev_dept.values.tolist()}
        })
        
        # Insight 4: Top 10 Doctors by Avg Revenue (kept as requested)
        avg_rev_doc = df.groupby('doctor_name')['revenue'].mean().sort_values(ascending=False).head(10)
        insights.append({
            "title": "Top 10 Doctors by Avg Revenue",
            "description": "Doctors with the highest average revenue per visit.",
            "chart_type": "bar",
            "chart_data": {"labels": avg_rev_doc.index.tolist(), "values": avg_rev_doc.values.tolist()}
        })
        
        # --- 2. Patient Demographics ---
        
        # Insight 5: Patient Age Group Distribution
        age_bins = [0, 18, 30, 50, 70, 150]
        age_labels = ['0-18', '19-30', '31-50', '51-70', '70+']
        df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)
        age_dist = df['age_group'].value_counts().sort_index()
        insights.append({
            "title": "Patient Age Group Distribution",
            "description": "Demographic breakdown of patients by age groups.",
            "chart_type": "bar",
            "chart_data": {"labels": [str(x) for x in age_dist.index.tolist()], "values": age_dist.values.tolist()}
        })
        
        # Insight 6: Gender Distribution
        gender_dist = df['gender'].value_counts()
        insights.append({
            "title": "Patient Gender Distribution",
            "description": "Split between Male and Female patients.",
            "chart_type": "pie",
            "chart_data": {"labels": gender_dist.index.tolist(), "values": gender_dist.values.tolist()}
        })
        
        # Insight 7: Top Patient Locations (Branches)
        loc_dist = df['branch'].value_counts().head(10)
        insights.append({
            "title": "Visits by Branch (Location)",
            "description": "Patient volume across different hospital branches.",
            "chart_type": "bar",
            "chart_data": {"labels": loc_dist.index.tolist(), "values": loc_dist.values.tolist()}
        })
        
        # --- 3. Clinical & Operational Trends ---
        
        # Insight 8: Revenue by Branch (kept as requested)
        rev_branch = df.groupby('branch')['revenue'].sum().sort_values(ascending=False)
        insights.append({
            "title": "Revenue by Branch",
            "description": "Total revenue generated by each branch.",
            "chart_type": "bar",
            "chart_data": {"labels": rev_branch.index.tolist(), "values": rev_branch.values.tolist()}
        })
        
        # Insight 9: Top Payment Modes
        pay_mode_counts = df['payment_mode'].value_counts().head(5)
        insights.append({
            "title": "Top Payment Modes",
            "description": "Most common methods of payment.",
            "chart_type": "bar",
            "chart_data": {"labels": pay_mode_counts.index.tolist(), "values": pay_mode_counts.values.tolist()}
        })
        
        # Insight 10: Monthly Visit Trends
        if df['visit_datetime'].notna().any():
            monthly_visits = df.set_index('visit_datetime').resample('M').size()
            monthly_labels = monthly_visits.index.strftime('%Y-%m').tolist()
            insights.append({
                "title": "Monthly Patient Visits Trend",
                "description": "Trend of patient visits over time.",
                "chart_type": "line",
                "chart_data": {"labels": monthly_labels, "values": monthly_visits.values.tolist()}
            })
        
        # Insight 11: Visits by Day of Week
        if df['visit_datetime'].notna().any():
            df['day_of_week'] = df['visit_datetime'].dt.day_name()
            days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_counts = df['day_of_week'].value_counts().reindex(days_order).fillna(0)
            insights.append({
                "title": "Visits by Day of Week",
                "description": "Patient volume distribution across the week.",
                "chart_type": "bar",
                "chart_data": {"labels": day_counts.index.tolist(), "values": day_counts.values.tolist()}
            })
        
        # Insight 12: Appointment Status Distribution
        status_counts = df['status'].value_counts().head(5)
        insights.append({
            "title": "Appointment Status Distribution",
            "description": "Breakdown of appointment statuses (e.g., Open, Closed).",
            "chart_type": "bar",
            "chart_data": {"labels": status_counts.index.tolist(), "values": status_counts.values.tolist()}
        })
        
        # Insight 13: Revenue per Visit Distribution (kept as requested)
        rev_bins = [0, 500, 1000, 2000, 5000, 10000]
        rev_labels = ['0-500', '501-1000', '1001-2000', '2001-5000', '5000+']
        df['rev_group'] = pd.cut(df['revenue'], bins=rev_bins, labels=rev_labels, right=False)
        rev_dist = df['rev_group'].value_counts().sort_index()
        insights.append({
            "title": "Revenue per Visit Distribution",
            "description": "Distribution of revenue amounts collected per visit.",
            "chart_type": "bar",
            "chart_data": {"labels": [str(x) for x in rev_dist.index.tolist()], "values": rev_dist.values.tolist()}
        })
        
        # Insight 14: Zero-Payment Visits by Department
        zero_pay = df[df['revenue'] == 0]
        zero_pay_dept = zero_pay['department'].value_counts().head(10)
        insights.append({
            "title": "Zero-Payment Visits by Department",
            "description": "Departments with the most free or unpaid visits.",
            "chart_type": "bar",
            "chart_data": {"labels": zero_pay_dept.index.tolist(), "values": zero_pay_dept.values.tolist()}
        })
        
        # Insight 15: Patient Retention (Repeat Visits)
        if 'patient_id' in df.columns:
            visit_counts = df['patient_id'].value_counts()
            repeat_patients = visit_counts[visit_counts > 1].count()
            single_visit_patients = visit_counts[visit_counts == 1].count()
            insights.append({
                "title": "Patient Retention Rate",
                "description": "Proportion of patients with repeat visits vs single visits.",
                "chart_type": "pie",
                "chart_data": {"labels": ["Repeat Patients", "One-time Patients"], "values": [int(repeat_patients), int(single_visit_patients)]}
            })

        # Insight 16: Peak Visiting Hours
        if df['visit_datetime'].notna().any():
            df['hour'] = df['visit_datetime'].dt.hour
            hour_counts = df['hour'].value_counts().sort_index()
            insights.append({
                "title": "Peak Visiting Hours",
                "description": "Patient traffic throughout the day.",
                "chart_type": "line",
                "chart_data": {"labels": [f"{int(h):02d}:00" for h in hour_counts.index.tolist()], "values": hour_counts.values.tolist()}
            })

        # Insight 17: Average Patient Age by Department
        avg_age_dept = df.groupby('department')['age'].mean().sort_values()
        insights.append({
            "title": "Average Patient Age by Department",
            "description": "Average age of patients visiting each department.",
            "chart_type": "bar",
            "chart_data": {"labels": avg_age_dept.index.tolist(), "values": [round(v, 1) for v in avg_age_dept.values.tolist()]}
        })

        # Insight 18: Gender Split in Top Department
        top_dept = df['department'].value_counts().idxmax()
        dept_gender = df[df['department'] == top_dept]['gender'].value_counts()
        insights.append({
            "title": f"Gender Distribution in {top_dept}",
            "description": f"Gender breakdown for the busiest department ({top_dept}).",
            "chart_type": "pie",
            "chart_data": {"labels": dept_gender.index.tolist(), "values": dept_gender.values.tolist()}
        })

        # Insight 19: Top Doctors in Top Department
        top_dept_docs = df[df['department'] == top_dept]['doctor_name'].value_counts().head(5)
        insights.append({
            "title": f"Top Doctors in {top_dept}",
            "description": f"Busiest doctors in {top_dept}.",
            "chart_type": "bar",
            "chart_data": {"labels": top_dept_docs.index.tolist(), "values": top_dept_docs.values.tolist()}
        })

        # Insight 20: Monthly Revenue Trend (kept as requested)
        if df['visit_datetime'].notna().any():
            monthly_rev = df.set_index('visit_datetime').resample('M')['revenue'].sum()
            insights.append({
                "title": "Monthly Revenue Trend",
                "description": "Total revenue collected over time.",
                "chart_type": "line",
                "chart_data": {"labels": monthly_rev.index.strftime('%Y-%m').tolist(), "values": monthly_rev.values.tolist()}
            })
        
        # --- ADDITIONAL INSIGHTS (New) ---
        
        # Insight 21: Doctor Workload Distribution
        doc_workload = df['doctor_name'].value_counts()
        insights.append({
            "title": "Doctor Workload Distribution",
            "description": "Distribution of patient load across all doctors.",
            "chart_type": "bar",
            "chart_data": {"labels": doc_workload.index.tolist(), "values": doc_workload.values.tolist()}
        })
        
        # Insight 22: Department by Branch Heatmap Data
        dept_branch = df.groupby(['department', 'branch']).size().reset_index(name='count')
        dept_branch_pivot = dept_branch.pivot(index='department', columns='branch', values='count').fillna(0)
        insights.append({
            "title": "Department Activity by Branch",
            "description": "Cross-tabulation of departments and branches.",
            "chart_type": "bar",
            "chart_data": {
                "labels": dept_branch_pivot.index.tolist(),
                "values": dept_branch_pivot.sum(axis=1).values.tolist()
            }
        })
        
        # Insight 23: Pediatric vs Adult Patients
        pediatric = len(df[df['age'] < 18])
        adult = len(df[df['age'] >= 18])
        insights.append({
            "title": "Pediatric vs Adult Patients",
            "description": "Ratio of patients under 18 vs adults.",
            "chart_type": "pie",
            "chart_data": {"labels": ["Pediatric (<18)", "Adult (18+)"], "values": [pediatric, adult]}
        })
        
        # Insight 24: Patient Volume per Doctor (Average)
        total_patients = len(df)
        unique_doctors = df['doctor_name'].nunique()
        avg_patients_per_doc = round(total_patients / unique_doctors, 1) if unique_doctors > 0 else 0
        insights.append({
            "title": "Average Patients per Doctor",
            "description": f"Each doctor sees approximately {avg_patients_per_doc} patients on average.",
            "chart_type": "bar",
            "chart_data": {"labels": ["Avg Patients/Doctor"], "values": [avg_patients_per_doc]}
        })
        
        # Insight 25: New Patients by Branch
        branch_patients = df.groupby('branch')['patient_id'].nunique().sort_values(ascending=False)
        insights.append({
            "title": "Unique Patients by Branch",
            "description": "Number of unique patients visiting each branch.",
            "chart_type": "bar",
            "chart_data": {"labels": branch_patients.index.tolist(), "values": branch_patients.values.tolist()}
        })
        
        return insights

    except Exception as e:
        import traceback
        traceback.print_exc()
        error_msg = f"Error processing data: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)


@app.get("/api/v1/analytics/dashboard")
def get_dashboard():
    """Dashboard endpoint - alias for doctor-patient-insights."""
    return get_insights()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
