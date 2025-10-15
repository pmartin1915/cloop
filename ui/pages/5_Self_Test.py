"""Self-Test page - Run automated tests on Ultrathink."""
import streamlit as st
from pathlib import Path
import sys
import asyncio

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from ultrathink.framework import Ultrathink
from ultrathink.self_test import SelfTester, AIErrorDetector

st.set_page_config(page_title="Self-Test - Ultrathink", page_icon="🧪", layout="wide")

st.title("🧪 Self-Test & Health Monitor")
st.markdown("Automated testing and health monitoring for Ultrathink")
st.markdown("---")

# Initialize
@st.cache_resource
def get_ultrathink():
    config_path = Path(__file__).parent.parent.parent / "ultrathink.yaml"
    return Ultrathink(str(config_path))

ultrathink = get_ultrathink()

# Tabs
tab1, tab2, tab3 = st.tabs(["🧪 Run Tests", "🏥 Health Monitor", "📊 Test History"])

with tab1:
    st.subheader("Automated Test Suite")
    st.markdown("""
    Run comprehensive tests to verify all Ultrathink components are working correctly.
    
    **Tests include:**
    - Framework initialization
    - File analysis
    - Handoff generation
    - Knowledge base operations
    - Error recovery
    """)
    
    if st.button("🚀 Run Full Test Suite", type="primary", use_container_width=True):
        # Clear cache to reload test module
        import importlib
        import sys
        if 'ultrathink.self_test' in sys.modules:
            importlib.reload(sys.modules['ultrathink.self_test'])
        
        from ultrathink.self_test import SelfTester
        
        with st.spinner("Running tests..."):
            tester = SelfTester(ultrathink)
            
            # Run tests
            results = asyncio.run(tester.run_full_test_suite())
            
            # Display results
            col1, col2, col3 = st.columns(3)
            col1.metric("Tests Run", results['tests_run'])
            col2.metric("Passed", results['tests_passed'], delta=results['tests_passed'])
            col3.metric("Failed", results['tests_failed'], delta=-results['tests_failed'] if results['tests_failed'] > 0 else 0)
            
            st.markdown("---")
            
            # Detailed results
            for test in results['details']:
                if test['passed']:
                    st.success(f"✓ {test['test']} - Passed ({test['duration']:.2f}s)")
                else:
                    st.error(f"✗ {test['test']} - Failed ({test['duration']:.2f}s)")
                    if test['error']:
                        st.code(test['error'], language="text")
            
            # Overall status
            if results['tests_failed'] == 0:
                st.balloons()
                st.success("🎉 All tests passed! System is healthy.")
            else:
                st.warning(f"⚠️ {results['tests_failed']} test(s) failed. Review errors above.")
            
            # Store results
            st.session_state['last_test_results'] = results

with tab2:
    st.subheader("System Health Monitor")
    st.markdown("Real-time health status of all Ultrathink components")
    
    if st.button("🔄 Check Health", use_container_width=True):
        with st.spinner("Checking system health..."):
            detector = AIErrorDetector(ultrathink)
            health = asyncio.run(detector.monitor_health())
            
            # Overall status
            if health['status'] == 'healthy':
                st.success(f"✓ System Status: {health['status'].upper()}")
            else:
                st.warning(f"⚠ System Status: {health['status'].upper()}")
            
            st.markdown("---")
            
            # Component checks
            st.markdown("### Component Status")
            
            for check_name, check_result in health['checks'].items():
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    if check_result['healthy']:
                        st.success(f"✓ {check_name.replace('_', ' ').title()}")
                    else:
                        st.error(f"✗ {check_name.replace('_', ' ').title()}")
                
                with col2:
                    st.write(check_result['message'])
            
            # Auto-refresh option
            st.markdown("---")
            auto_refresh = st.checkbox("Auto-refresh every 30 seconds")
            if auto_refresh:
                import time
                time.sleep(30)
                st.rerun()

with tab3:
    st.subheader("Test History")
    
    if 'last_test_results' in st.session_state:
        results = st.session_state['last_test_results']
        
        st.markdown(f"**Last run:** {results.get('timestamp', 'Unknown')}")
        st.markdown(f"**Results:** {results['tests_passed']}/{results['tests_run']} passed")
        
        # Chart
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[
            go.Bar(name='Passed', x=['Tests'], y=[results['tests_passed']], marker_color='green'),
            go.Bar(name='Failed', x=['Tests'], y=[results['tests_failed']], marker_color='red')
        ])
        
        fig.update_layout(
            title="Test Results",
            yaxis_title="Count",
            barmode='stack',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Download report
        report = SelfTester(ultrathink).generate_test_report(results)
        st.download_button(
            label="📥 Download Test Report",
            data=report,
            file_name="ultrathink_test_report.txt",
            mime="text/plain"
        )
    else:
        st.info("No test results yet. Run tests in the 'Run Tests' tab.")

# Sidebar
with st.sidebar:
    st.markdown("### 🧪 Self-Test Info")
    st.markdown("""
    **What is Self-Test?**
    
    Ultrathink can test itself automatically to ensure all components are working correctly.
    
    **Features:**
    - Automated test suite
    - Health monitoring
    - Error detection
    - Self-healing capabilities
    
    **When to use:**
    - After updates
    - When experiencing issues
    - Regular health checks
    - Before important analyses
    """)
