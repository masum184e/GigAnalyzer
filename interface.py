import streamlit as st
import pandas as pd
from datetime import datetime
import os
from visualizer import Visualizer
import io
import zipfile

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
    
    def show_analysis_results(self):
        if not st.session_state.processor:
            st.error("No analysis data available. Please run the analysis first.")
            return

        processor = st.session_state.processor
        visualizer = Visualizer(processor)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Total Gigs",
                value=len(st.session_state.gigs_data),
                delta=None
            )
    
        with col2:
            avg_price = processor.get_average_price()
            st.metric(
                label="Average Price",
                value=f"${avg_price:.2f}",
                delta=None
            )
    
        with col3:
            gigs_summary = processor.get_summary_statistics()
            st.metric(
                label="Total Tags",
                value=f"{gigs_summary['total_tags']:,}",
                delta=None
            )
    
        with col4:
            unique_tags = len(processor.get_unique_tags())
            st.metric(
                label="Unique Tags",
                value=unique_tags,
                delta=None
            )


        st.subheader("Analysis Summary")
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Overview", "🏷️ Keywords", "💰 Pricing", "✨ Intelligence","📥 Downloads"
        ])

        with tab1:
            self._show_overview_tab(processor)
        with tab2:
            self._show_keywords_tab(processor, visualizer)
        with tab3:
            self._show_price_analysis(processor, visualizer)
        with tab4:
            st.subheader("AI Recommendation")
        with tab5:
            self._show_downloads_tab()

    def _show_overview_tab(self, processor):
        st.subheader("Data Overview")
        df = processor.get_dataframe()
        st.dataframe(df.head(10), use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Price Statistics")
            price_stats = processor.get_price_statistics()
            for key, value in price_stats.items():
                st.write(f"**{key.title()}**: ${value:.2f}")

        with col2:
            st.subheader("Order Statistics")
            order_stats = processor.get_order_statistics()
            for key, value in order_stats.items():
                st.write(f"**{key.title()}**: {value:,.0f}")
    
    def _show_keywords_tab(self, processor, visualizer):
        st.subheader("Keyword Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top 10 Keywords")
            top_keywords_fig = visualizer.create_top_keywords_chart(top_n=10)
            st.plotly_chart(top_keywords_fig, use_container_width=True)
    
        with col2:
            st.subheader("Keyword Distribution")
            keyword_dist_fig = visualizer.create_keyword_distribution_pie()
            st.plotly_chart(keyword_dist_fig, use_container_width=True)
    
        st.subheader("Keyword Correlations")
        correlation_fig = visualizer.create_keyword_correlation_chart()
        st.plotly_chart(correlation_fig, use_container_width=True)

        st.subheader("Keyword Frequency Table")
        keyword_freq = processor.get_keyword_frequency()
        keyword_df = pd.DataFrame(list(keyword_freq.items()), columns=['Keyword', 'Frequency'])
        st.dataframe(keyword_df, use_container_width=True)
    
    def _show_downloads_tab(self):
        st.subheader("Download Reports")
    
        if 'export_files' not in st.session_state:
            st.info("No export files available. Please run the analysis first.")
            return
    
        for file_path in st.session_state.export_files:
            if os.path.exists(file_path):
                file_name = os.path.basename(file_path)
                with open(file_path, 'rb') as f:
                    st.download_button(
                        label=f"📄 Download {file_name}",
                        data=f.read(),
                        file_name=file_name,
                        mime='application/octet-stream'
                    )
    
        if st.button("📦 Download All Files (ZIP)"):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for file_path in st.session_state.export_files:
                    if os.path.exists(file_path):
                        zip_file.write(file_path, os.path.basename(file_path))

            zip_buffer.seek(0)
            st.download_button(
                label="📦 Download ZIP File",
                data=zip_buffer.getvalue(),
                file_name=f"gig_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                mime='application/zip'
            )

    def _show_price_analysis(self, processor, visualizer):
        st.subheader("Pricing Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Price Distribution")
            price_dist_fig = visualizer.create_price_distribution_chart()
            st.plotly_chart(price_dist_fig, use_container_width=True)

        with col2:
            st.subheader("Price vs Orders")
            price_orders_fig = visualizer.create_price_vs_orders_scatter()
            st.plotly_chart(price_orders_fig, use_container_width=True)
