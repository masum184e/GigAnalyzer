from exporter import DataExporter
from fetcher import Fetcher
from processor import DataProcessor
import streamlit as st

class Analyzer:

    def run_analysis(self, keywords, options):
        fetcher = Fetcher()
        try:
            # split keywords
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

            # fetch gigs data
            progress_bar.progress(20)
            gigs_data = fetcher.fetch_mock_data(keywords)
            st.session_state.gigs_data = gigs_data
            status_text.text("Processing data...")

            # process data to dataframes
            progress_bar.progress(40)
            processor = DataProcessor(gigs_data)
            st.session_state.processor = processor
            status_text.text("Creating visualizations...")

            progress_bar.progress(60)
            status_text.text("Exporting data...")
            
            # export data
            progress_bar.progress(80)
            exporter = DataExporter(processor)
            export_files = []

            # handle export options
            if options['export_excel']:
                excel_file = exporter.export_to_excel()
                export_files.append(excel_file)

            if options['export_txt']:
                txt_files = exporter.export_text_reports()
                export_files.extend(txt_files)
            status_text.text("Analysis complete!")
    
            progress_bar.progress(100)        
            st.session_state.analysis_complete = True
            st.session_state.export_files = export_files
            
            progress_bar.empty()
            status_text.empty()

            st.success("🎉 Analysis completed successfully! Check the results below.")
            st.rerun()
        except Exception as exception:
            st.error(f"An error occurred during analysis: {str(exception)}")
            st.exception(exception)