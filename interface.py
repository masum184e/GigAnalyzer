import streamlit as st

class Interface:
    def show_welcome_screen(self):
        st.markdown("""
            <div style="width:65%;margin: auto;">
                <h2 style='text-align: center;'>Welcome to GigAnalyzer! 👋</h2>
                <p>This application helps you analyze Fiverr gigs based on keywords and provides comprehensive insights.</p>
                <h4>🚀 How to use:</h4>
                <ul>
                    <li><b>Enter Keywords</b>: Add your search terms in the sidebar</li>
                    <li><b>Configure Settings</b>: Choose number of gigs and analysis options</li>
                    <li><b>Start Analysis</b>: Click the "Start Analysis" button</li>
                    <li><b>View Results</b>: Explore charts, statistics, and download reports</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
