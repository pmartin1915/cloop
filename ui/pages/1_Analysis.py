"""Analysis page - Scan code for issues."""
import streamlit as st
from pathlib import Path
import sys
import asyncio

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from ultrathink.framework import Ultrathink

st.set_page_config(page_title="Analysis - Ultrathink", page_icon="🔍", layout="wide")

st.title("🔍 Code Analysis")
st.markdown("Analyze your code to identify bugs, security issues, and quality problems.")
st.markdown("---")

# Initialize framework
@st.cache_resource
def get_ultrathink():
    config_path = Path(__file__).parent.parent.parent / "ultrathink.yaml"
    return Ultrathink(str(config_path))

ultrathink = get_ultrathink()

# Input section
col1, col2 = st.columns([3, 1])

with col1:
    analysis_path = st.text_input(
        "📁 Path to analyze",
        value=str(Path.cwd()),
        help="Enter the path to a file or directory to analyze"
    )

with col2:
    save_findings = st.checkbox("💾 Save to KB", value=True, help="Save findings to knowledge base")

if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
    if not Path(analysis_path).exists():
        st.error(f"Path does not exist: {analysis_path}")
    else:
        try:
            # Get list of files to analyze
            path = Path(analysis_path)
            if path.is_file():
                files_to_analyze = [path]
            else:
                files_to_analyze = list(path.rglob("*.py"))
            
            total_files = len(files_to_analyze)
            
            if total_files == 0:
                st.warning("No Python files found to analyze")
                st.stop()
            
            # Show file count and list
            st.info(f"📊 Found {total_files} Python file(s) to analyze")
            
            with st.expander("📄 Files to analyze", expanded=False):
                for f in files_to_analyze[:20]:
                    st.text(f"  • {f.relative_to(path.parent if path.is_file() else path)}")
                if total_files > 20:
                    st.text(f"  ... and {total_files - 20} more")
            
            # Run analysis with spinner
            with st.spinner(f"🔍 Analyzing {total_files} files with AI... This may take several minutes for large codebases."):
                result = asyncio.run(ultrathink.analyze_codebase(analysis_path, save_findings=save_findings))
            
            # Success
            st.success(f"✅ Successfully analyzed {total_files} file(s) - Found {result.get('summary', {}).get('total_issues', 0)} issues")
            
            # Store in session state
            st.session_state['last_analysis'] = result
            
        except Exception as e:
            import traceback
            st.error(f"❌ Analysis failed: {e}")
            with st.expander("Error details"):
                st.code(traceback.format_exc())
            st.stop()

# Display results
if 'last_analysis' in st.session_state:
    result = st.session_state['last_analysis']
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Results", "📋 Handoff Prompt", "🔎 Details"])
    
    with tab1:
        st.subheader("Analysis Summary")
        
        summary = result.get("summary", {})
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Files Analyzed", summary.get('files_analyzed', 0))
    with col2:
        st.metric("Total Issues", summary.get('total_issues', 0))
    with col3:
        st.metric("Critical", summary.get('critical_issues', 0), delta_color="inverse")
    with col4:
        st.metric("High Priority", summary.get('high_priority_issues', 0), delta_color="inverse")
    
    # Severity breakdown
    severity_breakdown = summary.get('severity_breakdown', {})
    if severity_breakdown:
        st.markdown("### Severity Distribution")
        
        import plotly.graph_objects as go
        
        colors = {
            'critical': '#dc2626',
            'high': '#ea580c',
            'medium': '#eab308',
            'low': '#3b82f6',
            'info': '#6366f1'
        }
        
        fig = go.Figure(data=[go.Pie(
            labels=list(severity_breakdown.keys()),
            values=list(severity_breakdown.values()),
            marker=dict(colors=[colors.get(k, '#6366f1') for k in severity_breakdown.keys()]),
            hole=0.4
        )])
        
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
        # Action buttons
        st.markdown("### Next Steps")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧬 Learn from these findings", use_container_width=True, key="learn_tab1"):
                st.switch_page("pages/2_Learning.py")
        
        with col2:
            if st.button("🔄 Run another analysis", use_container_width=True, key="rerun_tab1"):
                del st.session_state['last_analysis']
                st.rerun()
    
    with tab2:
        st.subheader("📋 AI Handoff Prompt")
        st.markdown("Copy this prompt to hand off to Amazon Q or another AI assistant:")
        
        # Generate handoff prompt
        summary = result.get("summary", {})
        total_issues = summary.get('total_issues', 0)
        critical = summary.get('critical_issues', 0)
        high = summary.get('high_priority_issues', 0)
        
        handoff_prompt = f"""# Code Quality Analysis - Handoff Prompt

## Context
I've analyzed my codebase using Ultrathink and found {total_issues} issues that need attention.

## Coding Standards & Best Practices
When fixing these issues, please follow these principles:

1. **Type Safety**: Add type hints to all functions and variables
2. **Error Handling**: Implement proper exception handling with specific error types
3. **Security**: Avoid eval(), use parameterized queries, validate all inputs
4. **Documentation**: Add docstrings to all functions and classes
5. **Code Quality**: Follow PEP 8, keep functions small and focused
6. **Testing**: Write unit tests for all fixes
7. **Performance**: Consider time/space complexity, avoid unnecessary loops

## Issues Found

### Summary
- **Total Issues**: {total_issues}
- **Critical**: {critical}
- **High Priority**: {high}

### Severity Breakdown
"""
        
        severity_breakdown = summary.get('severity_breakdown', {})
        for severity, count in severity_breakdown.items():
            if count > 0:
                handoff_prompt += f"- {severity.title()}: {count}\n"
        
        handoff_prompt += "\n### Detailed Findings\n\n"
        
        # Add findings by file
        for file_result in result.get("results", []):
            file_path = file_result.get("file", "Unknown")
            
            if 'error' in file_result:
                continue
            
            analysis = file_result.get("analysis", {})
            findings = analysis.get("findings", [])
            
            if not findings:
                continue
            
            handoff_prompt += f"#### File: `{Path(file_path).name}`\n\n"
            
            for i, finding in enumerate(findings, 1):
                severity = finding.get("severity", "info").upper()
                category = finding.get("category", "unknown")
                line = finding.get("line_number", "?")
                description = finding.get("description", "No description")
                suggestion = finding.get("suggestion", "")
                
                handoff_prompt += f"**{i}. [{severity}] Line {line} - {category}**\n"
                handoff_prompt += f"- Issue: {description}\n"
                if suggestion:
                    handoff_prompt += f"- Suggested Fix: {suggestion}\n"
                handoff_prompt += "\n"
        
        handoff_prompt += """## Your Task

Please help me fix these issues following the coding standards above. For each fix:
1. Explain what the issue is and why it's a problem
2. Show the corrected code
3. Explain what you changed and why
4. Suggest any additional improvements

Let's start with the critical and high-priority issues first.
"""
        
        # Display in text area for easy copying
        st.text_area(
            "Handoff Prompt (click to select all, then copy)",
            handoff_prompt,
            height=400,
            help="Copy this entire prompt and paste it into your next AI chat session"
        )
        
        # Download button
        st.download_button(
            label="💾 Download Handoff Prompt",
            data=handoff_prompt,
            file_name="ultrathink_handoff.md",
            mime="text/markdown",
            use_container_width=True
        )
        
        st.info("💡 **Tip**: This prompt includes best practices and all findings. Paste it into Amazon Q, Claude, or any AI assistant to get help fixing the issues.")
    
    with tab3:
        st.subheader("🔎 Detailed Findings")
        
        for file_result in result.get("results", []):
            file_path = file_result.get("file", "Unknown")
            
            with st.expander(f"📄 {Path(file_path).name}", expanded=False):
                if 'error' in file_result:
                    st.error(f"Error: {file_result['error']}")
                    continue
                
                analysis = file_result.get("analysis", {})
                findings = analysis.get("findings", [])
                
                if not findings:
                    st.success("✅ No issues found")
                    continue
                
                for i, finding in enumerate(findings, 1):
                    severity = finding.get("severity", "info").lower()
                    category = finding.get("category", "unknown")
                    line = finding.get("line_number", "?")
                    description = finding.get("description", "No description")
                    suggestion = finding.get("suggestion", "")
                    
                    severity_colors = {
                        'critical': '🔴',
                        'high': '🟠',
                        'medium': '🟡',
                        'low': '🔵',
                        'info': '⚪'
                    }
                    
                    icon = severity_colors.get(severity, '⚪')
                    
                    st.markdown(f"**{icon} Finding #{i}** - Line {line} - `{category}`")
                    st.markdown(f"**Issue:** {description}")
                    
                    if suggestion:
                        st.markdown(f"**💡 Suggestion:** {suggestion}")
                    
                    st.markdown("---")

else:
    st.info("👆 Enter a path and click 'Run Analysis' to get started")
    
    # Quick examples
    st.markdown("### 💡 Quick Examples")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Analyze a single file:**")
        st.code("c:\\Cloop\\flawed_demo\\calculator_v1.py")
    
    with col2:
        st.markdown("**Analyze a directory:**")
        st.code("c:\\Cloop\\flawed_demo")
