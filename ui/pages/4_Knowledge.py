"""Knowledge page - Browse and search the knowledge base."""
import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from ultrathink.framework import Ultrathink

st.set_page_config(page_title="Knowledge - Ultrathink", page_icon="📚", layout="wide")

st.title("📚 Knowledge Base")
st.markdown("Browse, search, and manage your accumulated code intelligence.")
st.markdown("---")

# Initialize
@st.cache_resource
def get_ultrathink():
    config_path = Path(__file__).parent.parent.parent / "ultrathink.yaml"
    return Ultrathink(str(config_path))

ultrathink = get_ultrathink()
ultrathink.initialize()

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["🔍 Findings", "🧬 Patterns", "✨ Improvements"])

with tab1:
    st.subheader("All Findings")
    
    # Get all findings
    findings = ultrathink.knowledge_base.get_all_findings()
    
    if not findings:
        st.info("No findings in knowledge base. Run an analysis to get started!")
    else:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            severity_filter = st.multiselect(
                "Filter by Severity",
                options=['critical', 'high', 'medium', 'low', 'info'],
                default=['critical', 'high', 'medium', 'low', 'info']
            )
        
        with col2:
            category_filter = st.multiselect(
                "Filter by Category",
                options=list(set(f.get('category', 'unknown') for f in findings)),
                default=list(set(f.get('category', 'unknown') for f in findings))
            )
        
        with col3:
            search_term = st.text_input("🔍 Search", placeholder="Search descriptions...")
        
        # Filter findings
        filtered = [
            f for f in findings
            if f.get('severity', 'info').lower() in severity_filter
            and f.get('category', 'unknown') in category_filter
            and (not search_term or search_term.lower() in f.get('description', '').lower())
        ]
        
        st.markdown(f"**Showing {len(filtered)} of {len(findings)} findings**")
        
        # Display findings
        for i, finding in enumerate(filtered[:50], 1):  # Limit to 50 for performance
            severity = finding.get('severity', 'info').lower()
            
            severity_colors = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🔵',
                'info': '⚪'
            }
            
            icon = severity_colors.get(severity, '⚪')
            
            with st.expander(f"{icon} {finding.get('description', 'No description')[:80]}...", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Category:** `{finding.get('category', 'unknown')}`")
                    st.markdown(f"**Severity:** `{finding.get('severity', 'info')}`")
                
                with col2:
                    st.markdown(f"**File:** `{finding.get('file_path', 'unknown')}`")
                    st.markdown(f"**Line:** `{finding.get('line_number', '?')}`")
                
                st.markdown(f"**Description:** {finding.get('description', 'No description')}")
                
                if finding.get('suggestion'):
                    st.markdown(f"**💡 Suggestion:** {finding['suggestion']}")
        
        if len(filtered) > 50:
            st.info(f"Showing first 50 results. {len(filtered) - 50} more available.")

with tab2:
    st.subheader("Identified Patterns")
    
    # Get all patterns
    patterns = ultrathink.knowledge_base.get_all_patterns()
    
    if not patterns:
        st.info("No patterns identified yet. Run the learning process to identify patterns!")
        
        if st.button("🧬 Go to Learning", use_container_width=True, key="learn_patterns"):
            st.switch_page("pages/2_Learning.py")
    else:
        st.markdown(f"**Total patterns: {len(patterns)}**")
        
        # Display patterns
        for i, pattern in enumerate(patterns, 1):
            severity = pattern.get('severity', 'medium').lower()
            
            severity_colors = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🔵'
            }
            
            icon = severity_colors.get(severity, '⚪')
            
            with st.expander(f"{icon} Pattern #{i}: {pattern.get('description', 'No description')}", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Type:** `{pattern.get('pattern_type', 'unknown')}`")
                with col2:
                    st.markdown(f"**Severity:** `{pattern.get('severity', 'medium')}`")
                with col3:
                    st.markdown(f"**Frequency:** {pattern.get('frequency', 0)} times")
                
                st.markdown(f"**Description:** {pattern.get('description', 'No description')}")

with tab3:
    st.subheader("Available Improvements")
    
    # Get all improvements
    improvements = ultrathink.knowledge_base.get_all_improvements()
    
    if not improvements:
        st.info("No improvements available yet. Run the learning process to generate improvements!")
        
        if st.button("🧬 Go to Learning", use_container_width=True, key="learn_improvements"):
            st.switch_page("pages/2_Learning.py")
    else:
        st.success(f"✨ {len(improvements)} improvements ready to be applied to new projects!")
        
        # Display improvements
        for i, imp in enumerate(improvements, 1):
            with st.expander(f"✨ Improvement #{i}: {imp.get('reason', 'No description')}", expanded=False):
                st.markdown(f"**Reason:** {imp.get('reason', 'No description')}")
                
                if imp.get('template_file'):
                    st.markdown(f"**Target template:** `{imp['template_file']}`")
                
                if imp.get('line_pattern'):
                    st.markdown("**Pattern to match:**")
                    st.code(imp['line_pattern'], language="python")
                
                if imp.get('replacement'):
                    st.markdown("**Replacement:**")
                    st.code(imp['replacement'], language="python")

# Knowledge base management
st.markdown("---")
st.subheader("🛠️ Knowledge Base Management")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 View Statistics", use_container_width=True):
        stats = ultrathink.knowledge_base.get_stats()
        
        st.json(stats)

with col2:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_resource.clear()
        st.success("Data refreshed!")
        st.rerun()

with col3:
    if st.button("📍 Database Location", use_container_width=True):
        db_path = Path(__file__).parent.parent.parent / "ultrathink.db"
        st.info(f"Database: {db_path.absolute()}")
