"""Learning page - Identify patterns and generate improvements."""
import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from ultrathink.framework import Ultrathink
from ultrathink.learning_engine import LearningEngine

st.set_page_config(page_title="Learning - Ultrathink", page_icon="🧬", layout="wide")

st.title("🧬 Pattern Learning")
st.markdown("Identify recurring patterns in your code and generate automatic fixes.")
st.markdown("---")

# Initialize
@st.cache_resource
def get_ultrathink():
    config_path = Path(__file__).parent.parent.parent / "ultrathink.yaml"
    return Ultrathink(str(config_path))

ultrathink = get_ultrathink()
ultrathink.initialize()

# Get current stats
kb_stats = ultrathink.knowledge_base.get_stats()

# Info section
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📋 Total Findings", kb_stats.get('total_findings', 0))
with col2:
    st.metric("🧬 Patterns Identified", kb_stats.get('total_patterns', 0))
with col3:
    st.metric("✨ Improvements Ready", kb_stats.get('total_improvements', 0))

st.markdown("---")

# Learning controls
st.subheader("⚙️ Learning Configuration")

col1, col2 = st.columns([2, 1])

with col1:
    threshold = st.slider(
        "Minimum occurrences for pattern detection",
        min_value=1,
        max_value=10,
        value=2,
        help="Issues must appear this many times to be considered a pattern"
    )

with col2:
    st.markdown("")
    st.markdown("")
    if st.button("🚀 Learn Patterns", type="primary", use_container_width=True):
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.info("📊 Loading findings from knowledge base...")
            progress_bar.progress(0.2)
            
            # Create learning engine
            learning_engine = LearningEngine(
                knowledge_base=ultrathink.knowledge_base,
                similarity_threshold=ultrathink.config.get('learning', {}).get('pattern_similarity_threshold', 0.8)
            )
            
            status_text.info("🧬 Analyzing patterns and similarities...")
            progress_bar.progress(0.5)
            
            # Learn from findings
            result = learning_engine.learn_from_findings(occurrence_threshold=threshold)
            
            status_text.info("🔧 Generating code patches...")
            progress_bar.progress(0.8)
            
            # Store in session state
            st.session_state['learning_result'] = result
            
            progress_bar.progress(1.0)
            status_text.success(f"✅ Learning complete! Found {result['patterns_identified']} patterns, generated {result['patches_generated']} patches")
            
            import time
            time.sleep(1)
            
            progress_bar.empty()
            status_text.empty()
            st.rerun()
            
        except Exception as e:
            import traceback
            progress_bar.empty()
            status_text.error(f"❌ Learning failed: {e}")
            with st.expander("Error details"):
                st.code(traceback.format_exc())

# Display results
if 'learning_result' in st.session_state:
    result = st.session_state['learning_result']
    
    st.markdown("---")
    st.subheader("📊 Learning Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("🧬 Patterns Identified", result['patterns_identified'])
    with col2:
        st.metric("🔧 Patches Generated", result['patches_generated'])
    
    # Show patterns
    if result['patterns']:
        st.markdown("---")
        st.subheader("🔍 Identified Patterns")
        
        for i, pattern in enumerate(result['patterns'], 1):
            severity = pattern['severity'].lower()
            
            # Color code by severity
            severity_colors = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🔵'
            }
            
            icon = severity_colors.get(severity, '⚪')
            
            with st.expander(f"{icon} Pattern #{i}: {pattern['description']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"**Category:** `{pattern['pattern_type']}`")
                with col2:
                    st.markdown(f"**Severity:** `{pattern['severity']}`")
                with col3:
                    st.markdown(f"**Frequency:** {pattern['frequency']} times")
                
                st.markdown(f"**Affected files:** {len(pattern['affected_files'])}")
                
                if pattern['affected_files'][:3]:
                    st.markdown("**Examples:**")
                    for file in pattern['affected_files'][:3]:
                        st.code(file, language="text")
    
    # Show patches
    if result['patches']:
        st.markdown("---")
        st.subheader("🔧 Generated Patches")
        
        for i, patch in enumerate(result['patches'], 1):
            with st.expander(f"✨ Patch #{i}: {patch['reason']}", expanded=True):
                if patch.get('template_file'):
                    st.markdown(f"**Target template:** `{patch['template_file']}`")
                
                if patch.get('line_pattern'):
                    st.markdown("**Pattern to match:**")
                    st.code(patch['line_pattern'], language="python")
                
                if patch.get('replacement'):
                    st.markdown("**Replacement:**")
                    st.code(patch['replacement'], language="python")
    
    # Learning stats
    learning_engine = LearningEngine(
        knowledge_base=ultrathink.knowledge_base,
        similarity_threshold=0.8
    )
    stats = learning_engine.get_learning_stats()
    
    st.markdown("---")
    st.subheader("📈 Learning Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Findings", stats['total_findings'])
    with col2:
        st.metric("Total Patterns", stats['total_patterns'])
    with col3:
        st.metric("Total Patches", stats['total_patches'])
    with col4:
        st.metric("Learning Rate", f"{stats['learning_rate']:.1%}")
    
    # Top issues
    if stats['top_issues']:
        st.markdown("### 🎯 Most Common Issues")
        
        for issue in stats['top_issues'][:5]:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{issue['description']}**")
            with col2:
                st.markdown(f"`{issue['count']} times`")
    
    # Next steps
    st.markdown("---")
    st.markdown("### Next Steps")
    
    if result['patches_generated'] > 0:
        st.success(f"✅ {result['patches_generated']} improvements are now ready to be applied to new projects!")
        
        if st.button("🚀 Create a new project with improvements", use_container_width=True):
            st.switch_page("pages/3_Projects.py")
    else:
        st.info("ℹ️ No new patterns found. Analyze more code to enable learning.")
        
        if st.button("🔍 Run more analysis", use_container_width=True):
            st.switch_page("pages/1_Analysis.py")

else:
    st.info("👆 Configure settings and click 'Learn Patterns' to get started")
    
    # Help text
    st.markdown("### 💡 How It Works")
    
    st.markdown("""
    1. **Pattern Detection**: Ultrathink analyzes stored findings to identify recurring issues
    2. **Similarity Matching**: Similar issues are grouped together using fuzzy matching
    3. **Patch Generation**: For each pattern, a code patch is automatically generated
    4. **Auto-Application**: Patches are applied to new projects during scaffolding
    """)
    
    if kb_stats.get('total_findings', 0) == 0:
        st.warning("⚠️ No findings in knowledge base. Run an analysis first!")
        
        if st.button("🔍 Go to Analysis", use_container_width=True):
            st.switch_page("pages/1_Analysis.py")
