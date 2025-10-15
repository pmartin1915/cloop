"""Projects page - Scaffold new projects with improvements."""
import streamlit as st
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from ultrathink.framework import Ultrathink
from ultrathink.scaffolding import PythonScaffolder

st.set_page_config(page_title="Projects - Ultrathink", page_icon="🚀", layout="wide")

st.title("🚀 Project Scaffolding")
st.markdown("Generate new FastAPI projects with learned improvements automatically applied.")
st.markdown("---")

# Initialize
@st.cache_resource
def get_ultrathink():
    config_path = Path(__file__).parent.parent.parent / "ultrathink.yaml"
    return Ultrathink(str(config_path))

ultrathink = get_ultrathink()
ultrathink.initialize()

# Check available improvements
kb_stats = ultrathink.knowledge_base.get_stats()
improvements_count = kb_stats.get('total_improvements', 0)

if improvements_count > 0:
    st.success(f"✨ {improvements_count} learned improvements will be automatically applied!")
else:
    st.info("ℹ️ No improvements learned yet. Projects will use base templates.")

st.markdown("---")

# Project configuration form
st.subheader("⚙️ Project Configuration")

with st.form("scaffold_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input(
            "Project Name *",
            value="my_fastapi_project",
            help="Name for your new project (lowercase, underscores allowed)"
        )
        
        author_name = st.text_input(
            "Author Name",
            value="Your Name",
            help="Your name for project metadata"
        )
    
    with col2:
        output_dir = st.text_input(
            "Output Directory",
            value=str(Path.cwd()),
            help="Where to create the project"
        )
        
        author_email = st.text_input(
            "Author Email",
            value="you@example.com",
            help="Your email for project metadata"
        )
    
    description = st.text_area(
        "Project Description",
        value="A FastAPI application",
        help="Brief description of your project"
    )
    
    submitted = st.form_submit_button("🚀 Generate Project", type="primary", use_container_width=True)

if submitted:
    if not project_name:
        st.error("Project name is required!")
    elif not project_name.replace('_', '').replace('-', '').isalnum():
        st.error("Project name must contain only letters, numbers, underscores, and hyphens")
    else:
        # Create progress indicators
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.info("📂 Creating project structure...")
            progress_bar.progress(0.2)
            
            # Create scaffolder with knowledge base
            scaffolder = PythonScaffolder(knowledge_base=ultrathink.knowledge_base)
            
            status_text.info("📦 Loading improvements from knowledge base...")
            progress_bar.progress(0.4)
            
            status_text.info(f"✨ Generating {project_name} with learned improvements...")
            progress_bar.progress(0.6)
            
            # Generate project
            project_path = scaffolder.scaffold(
                project_name=project_name,
                output_dir=output_dir,
                author_name=author_name,
                author_email=author_email,
                description=description
            )
            
            status_text.info("📝 Applying code improvements...")
            progress_bar.progress(0.9)
            
            st.session_state['last_project'] = {
                'path': str(project_path.absolute()),
                'name': project_name,
                'improvements': scaffolder.get_applied_improvements()
            }
            
            progress_bar.progress(1.0)
            status_text.success(f"✅ Project '{project_name}' generated successfully!")
            
            import time
            time.sleep(1)
            
            progress_bar.empty()
            status_text.empty()
            st.rerun()
            
        except FileExistsError:
            progress_bar.empty()
            status_text.error(f"❌ Project '{project_name}' already exists in {output_dir}")
        except Exception as e:
            import traceback
            progress_bar.empty()
            status_text.error(f"❌ Failed to generate project: {e}")
            with st.expander("Error details"):
                st.code(traceback.format_exc())

# Display last generated project
if 'last_project' in st.session_state:
    project = st.session_state['last_project']
    
    st.markdown("---")
    st.subheader("✅ Project Generated Successfully!")
    
    st.markdown(f"**📁 Location:** `{project['path']}`")
    st.markdown(f"**📦 Name:** `{project['name']}`")
    
    # Show applied improvements
    improvements = project.get('improvements', [])
    if improvements:
        st.markdown(f"### ✨ Applied {len(improvements)} Improvements")
        
        for imp in improvements[:10]:  # Show first 10
            st.markdown(f"- **{imp['file']}**: {imp['reason']}")
        
        if len(improvements) > 10:
            st.markdown(f"*... and {len(improvements) - 10} more*")
    else:
        st.info("No improvements were applied (none available in knowledge base)")
    
    # Next steps
    st.markdown("---")
    st.markdown("### 🎯 Next Steps")
    
    st.code(f"""
# Navigate to project
cd {project['name']}

# Install dependencies
poetry install

# Run the application
poetry run {project['name']}

# View API docs
# Open http://localhost:8000/docs in your browser
    """, language="bash")
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📂 Open in VS Code", use_container_width=True):
            import subprocess
            try:
                subprocess.run(['code', project['path']], check=True)
                st.success("Opening in VS Code...")
            except Exception as e:
                st.error(f"Failed to open VS Code: {e}")
                st.info(f"Manually open: {project['path']}")
    
    with col2:
        if st.button("🚀 Generate Another Project", use_container_width=True):
            del st.session_state['last_project']
            st.rerun()

else:
    # Help section
    st.markdown("### 💡 What You'll Get")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📦 Project Structure:**
        - Modern FastAPI application
        - Poetry dependency management
        - Docker & Docker Compose
        - GitHub Actions CI/CD
        - Comprehensive test suite
        """)
    
    with col2:
        st.markdown("""
        **✨ Automatic Improvements:**
        - Type hints added
        - Security fixes applied
        - Code quality enhancements
        - Best practices enforced
        - Documentation included
        """)
    
    if improvements_count == 0:
        st.markdown("---")
        st.warning("⚠️ No improvements in knowledge base yet!")
        st.markdown("To get the most value, analyze some code and learn patterns first:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Analyze Code", use_container_width=True):
                st.switch_page("pages/1_Analysis.py")
        
        with col2:
            if st.button("🧬 Learn Patterns", use_container_width=True):
                st.switch_page("pages/2_Learning.py")
