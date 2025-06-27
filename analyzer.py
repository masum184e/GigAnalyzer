from fetcher import Fetcher
import streamlit as st

class Analyzer:

    def run_analysis(self, keywords):

        fetcher = Fetcher()
        try:
            if '\n' in keywords:
                keywords = [k.strip() for k in keywords.split('\n') if k.strip()]
            else:
                keywords = [k.strip() for k in keywords.split(',') if k.strip()]
        
            if not keywords:
                st.error("Please enter at least one keyword!")
                return

            
            progress_bar = st.progress(0)
            status_text = st.empty()
            status_text.text("Fetching gig data...")
            progress_bar.progress(20)
            gigs_data = fetcher.fetch_mock_data(keywords)
            st.session_state.gigs_data = gigs_data
            print(gigs_data[0])
            status_text.text("Processing data...")
            progress_bar.progress(40)
            
            st.session_state.analysis_complete = True

            st.success("🎉 Analysis completed successfully! Check the results below.")
            st.rerun()
        except Exception as exception:
            st.error(f"An error occurred during analysis: {str(exception)}")
            st.exception(e)