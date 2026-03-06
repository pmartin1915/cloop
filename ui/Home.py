"""
Ultrathink - Unified Dashboard Homepage
Streamlined workflow: Drag code → Analyze → Get AI prompt → Paste to Amazon Q
"""
import streamlit as st
from pathlib import Path
import sys
import asyncio
import time

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ultrathink.framework import Ultrathink
from ultrathink.cli import generate_handoff_prompt

# Page config
st.set_page_config(
    page_title="Ultrathink - AI Code Improvement",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern look
st.markdown("""
<style>
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .workflow-step {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .step-number {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .step-text {
        font-size: 1.1rem;
    }
    .success-box {
        background: #10b981;
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
    .copy-button {
        background: #10b981 !important;
        color: white !important;
        font-size: 1.2rem !important;
        padding: 1rem 2rem !important;
        border-radius: 10px !important;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize framework
@st.cache_resource
def get_ultrathink():
    config_path = Path(__file__).parent.parent / "ultrathink.yaml"
    try:
        return Ultrathink(str(config_path))
    except:
        return None

# Main UI
st.markdown('<h1 class="main-title">🧠 Ultrathink</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your code with AI-powered analysis → Get perfect Amazon Q prompts in seconds</p>', unsafe_allow_html=True)

# Show workflow steps
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="workflow-step">
        <div class="step-number">1️⃣</div>
        <div class="step-text">Drop Your Code</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="workflow-step">
        <div class="step-number">2️⃣</div>
        <div class="step-text">AI Analyzes</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="workflow-step">
        <div class="step-number">3️⃣</div>
        <div class="step-text">Copy to Amazon Q</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Main input section
st.markdown("### 📁 Select Your Code")

# Initialize default path in session state
if 'selected_path' not in st.session_state:
    st.session_state.selected_path = ""
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None

# Two methods: Upload or Path
tab1, tab2 = st.tabs(["📤 Upload Files", "📂 Enter Path"])

with tab1:
    st.markdown("**Drag and drop Python files here, or click to browse:**")
    uploaded_files = st.file_uploader(
        "Choose Python files",
        type=['py'],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
        for f in uploaded_files[:5]:
            st.write(f"  • {f.name}")
        if len(uploaded_files) > 5:
            st.write(f"  • ... and {len(uploaded_files) - 5} more")
        st.session_state.uploaded_files = uploaded_files

with tab2:
    # Quick examples with clickable buttons
    st.markdown("**📚 Quick Examples** (click to use):")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Single File", use_container_width=True):
            st.session_state.selected_path = "c:\\Cloop\\flawed_demo\\calculator_v1.py"
        st.caption("Analyze one file")
    
    with col2:
        if st.button("📂 Folder", use_container_width=True):
            st.session_state.selected_path = "c:\\Cloop\\flawed_demo"
        st.caption("Analyze all files")
    
    with col3:
        if st.button("⌨️ Type Path", use_container_width=True):
            st.session_state.selected_path = ""
        st.caption("Enter custom path")
    
    # Path input with clear label
    code_path = st.text_input(
        "📂 Enter file or folder path:",
        value=st.session_state.selected_path,
        placeholder="c:\\Cloop\\flawed_demo\\calculator_v1.py",
        help="Type or paste the full path to a Python file or directory"
    )

# Determine what to analyze
if st.session_state.uploaded_files:
    code_path = "uploaded_files"
else:
    code_path = st.session_state.selected_path if st.session_state.selected_path else code_path if 'code_path' in locals() else ""

st.markdown("---")

# Analyze button - bigger and more prominent
analyze_button = st.button(
    "🚀 Analyze & Generate AI Prompt",
    type="primary",
    use_container_width=True,
    disabled=not code_path
)

# Analysis workflow
if analyze_button:
    # Handle uploaded files
    if code_path == "uploaded_files" and st.session_state.uploaded_files:
        import tempfile
        import os
        
        # Create temp directory for uploaded files
        temp_dir = tempfile.mkdtemp()
        files = []
        
        for uploaded_file in st.session_state.uploaded_files:
            file_path = Path(temp_dir) / uploaded_file.name
            file_path.write_bytes(uploaded_file.getvalue())
            files.append(file_path)
        
        path = Path(temp_dir)
    else:
        if not code_path:
            st.error("⚠️ Please enter a path or upload files")
            st.stop()
        
        path = Path(code_path)
        if not path.exists():
            st.error(f"⚠️ Path not found: {code_path}")
            st.stop()
        
        files = None
    
    # Initialize
    ultrathink = get_ultrathink()
    if not ultrathink:
        st.error("❌ Failed to initialize Ultrathink. Check your configuration.")
        st.stop()
    
    # Count files (use already set files from upload or discover from path)
    if files is None:
        if path.is_file():
            files = [path]
        else:
            files = list(path.rglob("*.py"))
    
    if not files:
        st.warning("⚠️ No Python files found at this path")
        st.stop()
    
    # Progress container
    progress_container = st.container()
    
    with progress_container:
        st.markdown("### 🔄 Analysis in Progress")
        
        # Step 1: Scanning
        with st.status("📂 Scanning files...", expanded=True) as status:
            st.write(f"Found **{len(files)}** Python file(s)")
            for f in files[:5]:
                st.write(f"  • {f.name}")
            if len(files) > 5:
                st.write(f"  • ... and {len(files) - 5} more")
            time.sleep(0.5)
            status.update(label="✅ Scan complete", state="complete")
        
        # Step 2: AI Analysis
        with st.status("🤖 Running AI analysis...", expanded=True) as status:
            st.write("This may take 1-3 minutes depending on code size")
            progress_bar = st.progress(0)
            
            try:
                # Simulate progress while analyzing
                for i in range(30):
                    progress_bar.progress(i / 30)
                    time.sleep(0.1)
                
                result = asyncio.run(ultrathink.analyze_codebase(str(path), save_findings=False))
                
                progress_bar.progress(100)
                status.update(label="✅ Analysis complete", state="complete")
                
            except Exception as e:
                status.update(label="❌ Analysis failed", state="error")
                st.error(f"Error: {e}")
                st.stop()
        
        # Step 3: Generate prompt
        with st.status("📝 Generating AI handoff prompt...", expanded=True) as status:
            prompt = generate_handoff_prompt(result, str(path))
            time.sleep(0.3)
            status.update(label="✅ Prompt ready", state="complete")
    
    # Results
    summary = result.get("summary", {})
    total_issues = summary.get("total_issues", 0)
    critical = summary.get("critical_issues", 0)
    high = summary.get("high_priority_issues", 0)
    
    st.markdown("---")
    
    # Success message
    if total_issues > 0:
        st.markdown(f"""
        <div class="success-box">
            <h2>✅ Analysis Complete!</h2>
            <p style="font-size: 1.3rem; margin: 1rem 0;">Found <strong>{total_issues}</strong> issues to improve</p>
            <p style="font-size: 1.1rem;">Critical: {critical} | High Priority: {high}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ Great! No issues found. Your code looks good!")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📄 Files", len(files))
    col2.metric("🔍 Issues", total_issues)
    col3.metric("🔴 Critical", critical)
    col4.metric("🟠 High", high)
    
    st.markdown("---")
    
    # The handoff prompt - main feature!
    if total_issues > 0:
        st.markdown("### 🎯 Your AI Handoff Prompt is Ready!")
        st.markdown("**Copy this entire prompt and paste it into Amazon Q to get fixes with explanations:**")
        
        # Display prompt in copyable text area
        st.text_area(
            "Click inside, press Ctrl+A to select all, then Ctrl+C to copy",
            prompt,
            height=400,
            label_visibility="collapsed"
        )
        
        # Action buttons
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="💾 Download as Markdown",
                data=prompt,
                file_name="ultrathink_handoff.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        with col2:
            import streamlit.components.v1 as components
            import json
            
            prompt_json = json.dumps(prompt)
            
            components.html(f"""
                <button onclick="copyText()" id="copyBtn"
                    style="width: 100%; padding: 0.75rem; background: #667eea; color: white; 
                           border: none; border-radius: 8px; font-size: 1rem; cursor: pointer; 
                           font-weight: 600;">
                    📋 Copy to Clipboard
                </button>
                <textarea id="hiddenText" style="position: absolute; left: -9999px;">{prompt}</textarea>
                <script>
                    function copyText() {{
                        const text = document.getElementById('hiddenText');
                        text.select();
                        document.execCommand('copy');
                        
                        const btn = document.getElementById('copyBtn');
                        btn.innerHTML = '✅ Copied!';
                        btn.style.background = '#10b981';
                        
                        setTimeout(() => {{
                            btn.innerHTML = '📋 Copy to Clipboard';
                            btn.style.background = '#667eea';
                        }}, 2000);
                    }}
                </script>
            """, height=60)
        
        # Instructions
        st.markdown("---")
        st.markdown("### 🚀 Next Steps")
        
        st.markdown("""
        1. **Copy the prompt above** (Ctrl+A, then Ctrl+C)
        2. **Open Amazon Q** in VSCode (or your preferred AI assistant)
        3. **Paste the prompt** (Ctrl+V)
        4. **Review Q's fixes** and apply the ones you like
        5. **Learn from the explanations** to improve your coding skills!
        """)
        
        # Tips
        with st.expander("💡 Pro Tips for Best Results"):
            st.markdown("""
            - **Ask Q to explain**: "Why is this a problem?" helps you learn
            - **Request alternatives**: "Show me 2 different ways to fix this"
            - **Get tests**: "Write unit tests for these fixes"
            - **Prioritize**: Start with critical and high-severity issues
            - **Iterate**: After applying fixes, run Ultrathink again to verify
            """)
    
    # Store in session for persistence
    st.session_state['last_result'] = result
    st.session_state['last_prompt'] = prompt
    st.session_state['copy_prompt'] = prompt

# Sidebar with stats
with st.sidebar:
    st.markdown("### 📊 Quick Stats")
    
    ultrathink = get_ultrathink()
    if ultrathink:
        try:
            ultrathink.initialize()
            kb_stats = ultrathink.knowledge_base.get_stats()
            
            st.metric("Total Findings", kb_stats.get('total_findings', 0))
            st.metric("Patterns Learned", kb_stats.get('total_patterns', 0))
            st.metric("Improvements Ready", kb_stats.get('total_improvements', 0))
            
            st.markdown("---")
            st.markdown("### 🔗 Quick Links")
            
            if st.button("🧬 Learning Dashboard", use_container_width=True):
                st.switch_page("pages/2_Learning.py")
            
            if st.button("🚀 Scaffold Project", use_container_width=True):
                st.switch_page("pages/3_Projects.py")
            
            if st.button("📚 Knowledge Base", use_container_width=True):
                st.switch_page("pages/4_Knowledge.py")
                
        except:
            st.info("Run an analysis to see stats")
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Ultrathink** helps you write better code by:
    - Finding bugs & security issues
    - Generating perfect AI prompts
    - Learning from your patterns
    - Improving over time
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>Ultrathink</strong> - Your AI-powered code improvement companion</p>
    <p>Made with ❤️ for developers who want to learn and improve</p>
</div>
""", unsafe_allow_html=True)
