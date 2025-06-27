import streamlit as st
from interface import Interface
from analyzer import Analyzer

st.set_page_config(
    page_title="GigAnalyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        width: 100%;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
        [data-testid="collapsedControl"] {
            display: none;
        }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'gigs_data' not in st.session_state:
        st.session_state.gigs_data = []
    if 'processor' not in st.session_state:
        st.session_state.processor = None

def main():
    interface = Interface()
    analyzer = Analyzer()
    initialize_session_state()

    st.markdown('<h1 class="main-header">GigAnalyzer</h1>', unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Search Keywords")
        keywords_input = st.text_area(
            "Enter keywords (one per line or comma-separated):",
            value="web design\nlogo design\ndigital marketing",
            height=100,
            help="Enter the keywords you want to search for gigs"
        )

        st.subheader("Analysis Options")
        include_price_analysis = st.checkbox("Price Trend Analysis", value=True)
        include_correlation = st.checkbox("Keyword Correlation", value=True)
        include_advanced_charts = st.checkbox("Advanced Visualizations", value=True)

        st.subheader("Export Options")
        export_excel = st.checkbox("Excel Report", value=True)
        export_txt = st.checkbox("Text Reports", value=True)
        
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            analyzer.run_analysis(keywords_input)

    if not st.session_state.analysis_complete:
        interface.show_welcome_screen()
    else:
        interface.show_analysis_results()

if __name__ == "__main__":
    main()
