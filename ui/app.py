"""
Ultrathink Streamlit Dashboard - Main Entry Point
"""
import streamlit as st
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ultrathink.framework import Ultrathink
from ultrathink.knowledge_base import KnowledgeBase

# Page config
st.set_page_config(
    page_title="Ultrathink Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize framework in session state
@st.cache_resource
def get_ultrathink():
    """Initialize Ultrathink framework (cached)."""
    try:
        config_path = Path(__file__).parent.parent / "ultrathink.yaml"
        return Ultrathink(str(config_path))
    except Exception as e:
        st.error(f"Failed to initialize Ultrathink: {e}")
        return None

# Sidebar navigation
st.sidebar.markdown("# 🧠 Ultrathink")
st.sidebar.markdown("*Self-Improving Development Framework*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "🔍 Analysis", "🧬 Learning", "🚀 Projects", "📚 Knowledge"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Actions")

if st.sidebar.button("🔄 Refresh Stats", use_container_width=True):
    st.cache_resource.clear()
    st.rerun()

# Redirect to new Home page
if page == "🏠 Dashboard":
    st.switch_page("Home.py")

if False:  # Old dashboard code (kept for reference)
    st.markdown('<h1 class="main-header">🧠 Ultrathink Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("*Your AI-powered code quality companion*")
    st.markdown("---")
    
    ultrathink = get_ultrathink()
    if not ultrathink:
        st.stop()
    
    # Get stats
    ultrathink.initialize()
    stats = ultrathink.get_stats()
    kb_stats = ultrathink.knowledge_base.get_stats()
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{kb_stats.get('total_findings', 0)}</div>
            <div class="stat-label">Total Findings</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{kb_stats.get('total_patterns', 0)}</div>
            <div class="stat-label">Patterns Learned</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{kb_stats.get('total_improvements', 0)}</div>
            <div class="stat-label">Improvements Ready</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        learning_rate = kb_stats.get('learning_rate', 0)
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{learning_rate:.1%}</div>
            <div class="stat-label">Learning Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent activity
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Severity Breakdown")
        severity_data = kb_stats.get('severity_breakdown', {})
        if severity_data:
            import plotly.graph_objects as go
            
            colors = {
                'critical': '#dc2626',
                'high': '#ea580c',
                'medium': '#eab308',
                'low': '#3b82f6'
            }
            
            fig = go.Figure(data=[go.Bar(
                x=list(severity_data.keys()),
                y=list(severity_data.values()),
                marker_color=[colors.get(k, '#6366f1') for k in severity_data.keys()],
                text=list(severity_data.values()),
                textposition='auto',
            )])
            
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis_title="Severity",
                yaxis_title="Count",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No findings yet. Run an analysis to get started!")
    
    with col2:
        st.subheader("🎯 Top Issues")
        top_issues = kb_stats.get('top_issues', [])
        if top_issues:
            for i, issue in enumerate(top_issues[:5], 1):
                st.markdown(f"**{i}.** {issue['description']}")
                st.caption(f"Found {issue['count']} times")
        else:
            st.info("No patterns identified yet.")
    
    st.markdown("---")
    
    # Quick start guide
    st.subheader("🚀 Quick Start")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1️⃣ Analyze")
        st.markdown("Go to **Analysis** tab to scan your code for issues")
        if st.button("→ Go to Analysis", key="goto_analysis"):
            st.switch_page("pages/1_Analysis.py")
    
    with col2:
        st.markdown("### 2️⃣ Learn")
        st.markdown("Visit **Learning** tab to identify patterns and generate fixes")
        if st.button("→ Go to Learning", key="goto_learning"):
            st.switch_page("pages/2_Learning.py")
    
    with col3:
        st.markdown("### 3️⃣ Build")
        st.markdown("Use **Projects** tab to scaffold new projects with improvements")
        if st.button("→ Go to Projects", key="goto_projects"):
            st.switch_page("pages/3_Projects.py")

elif page == "🔍 Analysis":
    st.switch_page("pages/1_Analysis.py")
elif page == "🧬 Learning":
    st.switch_page("pages/2_Learning.py")
elif page == "🚀 Projects":
    st.switch_page("pages/3_Projects.py")
elif page == "📚 Knowledge":
    st.switch_page("pages/4_Knowledge.py")
