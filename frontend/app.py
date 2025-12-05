import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(
    page_title="HMS Analytics Dashboard",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Modern UI (Light & Dark Mode) ---
st.markdown("""
<style>
    /* =============== CSS Variables for Theming =============== */
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-card: linear-gradient(135deg, #f5f7fa 0%, #e4e8ed 100%);
        --text-primary: #1a1a2e;
        --text-secondary: #4a5568;
        --accent-primary: #0f4c75;
        --accent-secondary: #3282b8;
        --border-color: #e2e8f0;
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Dark mode variables */
    @media (prefers-color-scheme: dark) {
        :root {
            --bg-primary: #0e1117;
            --bg-secondary: #1a1a2e;
            --bg-card: linear-gradient(135deg, #1e2030 0%, #262b40 100%);
            --text-primary: #fafafa;
            --text-secondary: #a0aec0;
            --accent-primary: #3282b8;
            --accent-secondary: #5cacee;
            --border-color: #2d3748;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
        }
    }
    
    /* Streamlit dark mode detection */
    [data-theme="dark"], .stApp[data-theme="dark"] {
        --bg-primary: #0e1117;
        --bg-secondary: #1a1a2e;
        --bg-card: linear-gradient(135deg, #1e2030 0%, #262b40 100%);
        --text-primary: #fafafa;
        --text-secondary: #a0aec0;
        --accent-primary: #3282b8;
        --accent-secondary: #5cacee;
        --border-color: #2d3748;
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
    }

    /* =============== Main Container =============== */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* =============== Headers =============== */
    h1 {
        text-align: center;
        padding-bottom: 1rem;
        border-bottom: 3px solid var(--accent-primary);
        margin-bottom: 1.5rem;
    }
    
    h2, h3 {
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 0.5rem;
    }

    /* =============== Metric Cards =============== */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        box-shadow: var(--shadow);
    }
    
    div[data-testid="metric-container"] label {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700;
    }
    
    /* =============== Tab Styling =============== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--bg-secondary);
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        border: 1px solid var(--border-color);
        border-bottom: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--accent-secondary);
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0f4c75 0%, #3282b8 100%) !important;
        color: white !important;
        border-color: var(--accent-primary);
    }
    
    /* =============== Sidebar =============== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        border-color: rgba(255,255,255,0.2);
    }
    
    /* Sidebar button */
    section[data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #3282b8 0%, #0f4c75 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        font-weight: 600;
        transition: transform 0.2s ease;
    }
    
    section[data-testid="stSidebar"] button:hover {
        transform: scale(1.02);
    }
    
    /* =============== Charts Container =============== */
    div[data-testid="stVerticalBlock"] > div:has(div.js-plotly-plot) {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
    }
    
    /* =============== Info/Warning/Error Boxes =============== */
    .stAlert {
        border-radius: 8px;
    }
    
    /* =============== Subheader Styling =============== */
    .stSubheader {
        font-weight: 600;
    }
    
    /* =============== Caption Text =============== */
    .stCaption {
        opacity: 0.8;
    }
    
    /* =============== Scrollbar Styling =============== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent-primary);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-secondary);
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🏥 HMS Doctor-Patient Analytics Dashboard")
st.markdown("**Real-time insights** into Doctor Performance, Patient Demographics, Clinical Demand & Operations")

# --- Configuration ---
# Local development URL - change to Vercel URL for production
try:
    API_URL = st.secrets["api_url"]
except Exception:
    # Default to local development
    API_URL = "http://127.0.0.1:8000/api/v1/analytics/doctor-patient-insights"

# --- Sidebar ---
st.sidebar.image("https://img.icons8.com/fluency/96/hospital-3.png", width=80)
st.sidebar.header("⚙️ Dashboard Settings")

# API Status indicator
api_base = API_URL.split('/api/')[0] if '/api/' in API_URL else API_URL
st.sidebar.info(f"🔗 API: `{api_base}`")

if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")

# --- Data Fetching ---
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_data():
    """Fetch analytics data from the backend API."""
    if not API_URL:
        st.error("❌ API URL not configured. Set it in Streamlit secrets or update the code.")
        return []
    
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ **Connection Error**: Could not connect to the backend API.")
        st.info("💡 Start the backend with: `python -m uvicorn main:app --reload --port 8000`")
        return []
    except requests.exceptions.Timeout:
        st.error("❌ **Timeout**: The API took too long to respond.")
        return []
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ **HTTP Error**: {e}")
        return []
    except Exception as e:
        st.error(f"❌ **Unexpected Error**: {e}")
        return []

# Fetch data
with st.spinner("Loading analytics data..."):
    data = fetch_data()

if not data:
    st.warning("⚠️ No data available. Please ensure the backend API is running.")
    st.code("cd backend && python -m uvicorn main:app --reload --port 8000", language="bash")
    st.stop()

# --- Show KPI Metrics ---
st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

# Extract some key metrics from insights
total_insights = len(data)
doctor_count = 0
patient_count = 0
department_count = 0

for item in data:
    if item['title'] == 'Doctor Workload Distribution':
        doctor_count = len(item['chart_data']['labels'])
    elif item['title'] == 'Patient Visits by Department':
        patient_count = sum(item['chart_data']['values'])
        department_count = len(item['chart_data']['labels'])

with col1:
    st.metric("📈 Total Insights", total_insights)
with col2:
    st.metric("👨‍⚕️ Doctors", doctor_count)
with col3:
    st.metric("👥 Total Visits", patient_count)
with col4:
    st.metric("🏥 Departments", department_count)

st.markdown("---")

# --- Visualization Helper ---
def render_insight(insight, height=400, unique_key=None):
    """Render a single insight with appropriate chart type."""
    with st.container():
        st.subheader(insight['title'])
        st.caption(insight['description'])
        
        chart_type = insight.get('chart_type', 'bar')
        chart_data = insight.get('chart_data', {})
        
        if not chart_data or not chart_data.get('labels') or not chart_data.get('values'):
            st.warning("No data available for this insight.")
            return
        
        # Check if all values are zero
        if all(v == 0 for v in chart_data['values']):
            st.info("📊 All values are zero for this metric.")

        df = pd.DataFrame({
            'Label': chart_data['labels'],
            'Value': chart_data['values']
        })
        
        # Dark mode compatible color palette
        colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', 
                  '#00f2fe', '#43e97b', '#38f9d7', '#fa709a', '#fee140']
        
        # Generate unique key for chart
        chart_key = unique_key or insight['title'].replace(' ', '_').lower()
        
        # Common layout settings for dark mode compatibility
        layout_settings = dict(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#a0aec0'),
            height=height,
            margin=dict(t=30, b=30, l=20, r=20),
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(128,128,128,0.2)',
                title=None
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(128,128,128,0.2)',
                title=None
            )
        )
        
        if chart_type == 'bar':
            fig = px.bar(
                df, x='Label', y='Value', 
                text='Value',
                color='Label',
                color_discrete_sequence=colors
            )
            fig.update_traces(
                texttemplate='%{text:.1f}', 
                textposition='outside',
                textfont=dict(color='#a0aec0')
            )
            fig.update_layout(
                **layout_settings,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True, key=f"bar_{chart_key}")
            
        elif chart_type == 'pie':
            fig = px.pie(
                df, names='Label', values='Value',
                hole=0.4,
                color_discrete_sequence=colors
            )
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont=dict(color='white')
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#a0aec0'),
                height=height,
                margin=dict(t=30, b=50, l=20, r=20),
                showlegend=True,
                legend=dict(
                    orientation="h", 
                    yanchor="bottom", 
                    y=-0.3,
                    font=dict(color='#a0aec0')
                )
            )
            st.plotly_chart(fig, use_container_width=True, key=f"pie_{chart_key}")
            
        elif chart_type == 'line':
            fig = px.line(
                df, x='Label', y='Value',
                markers=True,
                line_shape='spline'
            )
            fig.update_traces(
                line=dict(width=3, color='#667eea'),
                marker=dict(size=10, color='#764ba2', line=dict(width=2, color='#667eea'))
            )
            fig.update_layout(**layout_settings)
            st.plotly_chart(fig, use_container_width=True, key=f"line_{chart_key}")
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)

# --- Categorize Insights ---
# Updated keywords to match new backend insights
doc_keywords = ['Doctor', 'Revenue', 'Workload', 'Practitioner', 'Top 5', 'Top 10', 'Avg Revenue']
patient_keywords = ['Patient', 'Age', 'Gender', 'Retention', 'Pediatric', 'Adult', 'Unique Patients']
clinical_keywords = ['Department', 'Branch', 'Visits', 'Status', 'Activity']
operational_keywords = ['Hours', 'Payment', 'Day of Week', 'Monthly', 'Trend', 'Zero-Payment']

doc_insights = []
patient_insights = []
clinical_insights = []
operational_insights = []

for item in data:
    title = item['title']
    if any(k in title for k in doc_keywords):
        doc_insights.append(item)
    elif any(k in title for k in patient_keywords):
        patient_insights.append(item)
    elif any(k in title for k in operational_keywords):
        operational_insights.append(item)
    else:
        clinical_insights.append(item)

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs([
    f"👨‍⚕️ Doctor Performance ({len(doc_insights)})",
    f"👥 Patient Demographics ({len(patient_insights)})",
    f"🏥 Clinical Demand ({len(clinical_insights)})",
    f"� Operations & Trends ({len(operational_insights)})"
])

with tab1:
    st.header("👨‍⚕️ Doctor Performance & Revenue")
    if doc_insights:
        cols = st.columns(2)
        for i, insight in enumerate(doc_insights):
            with cols[i % 2]:
                render_insight(insight)
    else:
        st.info("No doctor performance insights available.")

with tab2:
    st.header("👥 Patient Demographics")
    if patient_insights:
        cols = st.columns(2)
        for i, insight in enumerate(patient_insights):
            with cols[i % 2]:
                render_insight(insight)
    else:
        st.info("No patient demographic insights available.")

with tab3:
    st.header("🏥 Clinical Demand & Distribution")
    if clinical_insights:
        cols = st.columns(2)
        for i, insight in enumerate(clinical_insights):
            with cols[i % 2]:
                render_insight(insight)
    else:
        st.info("No clinical demand insights available.")

with tab4:
    st.header("📈 Operations & Trends")
    if operational_insights:
        cols = st.columns(2)
        for i, insight in enumerate(operational_insights):
            with cols[i % 2]:
                render_insight(insight)
    else:
        st.info("No operational insights available.")

# --- Sidebar Footer ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Insight Summary")
st.sidebar.write(f"- 👨‍⚕️ Doctor: **{len(doc_insights)}**")
st.sidebar.write(f"- 👥 Patient: **{len(patient_insights)}**")
st.sidebar.write(f"- 🏥 Clinical: **{len(clinical_insights)}**")
st.sidebar.write(f"- 📈 Operations: **{len(operational_insights)}**")
st.sidebar.markdown("---")
st.sidebar.caption("HMS Analytics Microservice v2.0")
st.sidebar.caption(f"Total Insights: **{len(data)}**")
