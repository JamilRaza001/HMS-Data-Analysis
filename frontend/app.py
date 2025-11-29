import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="HMS Analytics", layout="wide", page_icon="🏥")

st.title("🏥 HMS Doctor-Patient Analytics Dashboard")
st.markdown("Real-time insights into Doctor Performance, Patient Demographics, and Clinical Demand.")

# --- Configuration ---
# Production: Use Vercel URL as default, can be overridden by secrets
try:
    API_URL = st.secrets["api_url"]
except Exception:
    # Default to Vercel deployment
    API_URL = "https://hms-data-analysis.vercel.app/api/v1/analytics/doctor-patient-insights"

# Sidebar
st.sidebar.header("Dashboard Settings")
st.sidebar.text(f"API: {API_URL.split('/api/')[0]}")
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# --- Data Fetching ---
@st.cache_data(ttl=600)
def fetch_data():
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Connection Error: Could not connect to the backend API.")
        st.info("💡 Please check your internet connection and ensure the backend is deployed.")
        return []
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ HTTP Error: {e}")
        st.error("The backend returned an error. Please contact support.")
        return []
    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")
        return []

data = fetch_data()

if not data:
    st.warning("⚠️ No data available. Please ensure the backend API is running.")
    st.stop()

# --- Visualization Helper ---
def render_insight(insight):
    with st.container():
        st.subheader(insight['title'])
        st.caption(insight['description'])
        
        chart_type = insight.get('chart_type', 'bar')
        chart_data = insight.get('chart_data', {})
        
        if not chart_data:
            st.warning("No data available for this insight.")
            return

        df = pd.DataFrame({
            'Label': chart_data['labels'],
            'Value': chart_data['values']
        })
        
        if chart_type == 'bar':
            fig = px.bar(df, x='Label', y='Value', text='Value', template="plotly_white", color='Value')
            fig.update_layout(xaxis_title=None, yaxis_title=None, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == 'pie':
            fig = px.pie(df, names='Label', values='Value', template="plotly_white", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == 'line':
            fig = px.line(df, x='Label', y='Value', markers=True, template="plotly_white")
            fig.update_layout(xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)

# --- Layout & Categorization ---
# Categorize insights based on keywords
doc_keywords = ['Doctor', 'Revenue', 'Pediatricians', 'Fee']
patient_keywords = ['Patient', 'Age', 'Gender', 'City', 'Locations', 'Retention']
clinical_keywords = ['OPD', 'Emergency', 'Medicine', 'Diagnosis', 'Visits', 'Prescription', 'Hours']

doc_insights = []
patient_insights = []
clinical_insights = []

for item in data:
    title = item['title']
    if any(k in title for k in doc_keywords):
        doc_insights.append(item)
    elif any(k in title for k in patient_keywords):
        patient_insights.append(item)
    else:
        clinical_insights.append(item)

# Tabs
tab1, tab2, tab3 = st.tabs(["👨‍⚕️ Doctor Performance", "🏥 Clinical Demand", "👥 Patient Demographics"])

with tab1:
    st.header("Doctor Performance & Revenue")
    if doc_insights:
        cols = st.columns(2)
        for i, insight in enumerate(doc_insights):
            with cols[i % 2]:
                render_insight(insight)
    else:
        st.info("No doctor performance insights available.")

with tab2:
    st.header("Clinical Demand & Trends")
    if clinical_insights:
        cols = st.columns(2)
        for i, insight in enumerate(clinical_insights):
            with cols[i % 2]:
                render_insight(insight)
    else:
        st.info("No clinical demand insights available.")

with tab3:
    st.header("Patient Demographics")
    if patient_insights:
        cols = st.columns(2)
        for i, insight in enumerate(patient_insights):
            with cols[i % 2]:
                render_insight(insight)
    else:
        st.info("No patient demographic insights available.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("HMS Analytics Microservice v1.0")
st.sidebar.caption(f"Total Insights: {len(data)}")
