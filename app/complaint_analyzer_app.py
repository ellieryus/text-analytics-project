# app/complaint_analyzer_app.py
"""
Consumer Complaint Analyzer - Streamlit App
Real-time complaint analysis with automatic risk flagging
"""

import streamlit as st
import pandas as pd
from analyzer import ComplaintAnalyzer
from database import ComplaintDatabase

# Page config
st.set_page_config(
    page_title="Complaint Analyzer",
    page_icon="🚨",
    layout="wide"
)

# Initialize
analyzer = ComplaintAnalyzer()
db = ComplaintDatabase()

# Title
st.title("Consumer Complaint Risk Analyzer")
st.markdown("*Real-time analysis with automatic risk flagging*")
st.markdown("---")

# Sidebar - Statistics
with st.sidebar:
    st.header("Database Statistics")
    
    stats = db.get_statistics()
    
    if stats:
        st.metric("Total Complaints", stats['total'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("High", stats['high_risk'])
        with col2:
            st.metric("Medium", stats['medium_risk'])
        with col3:
            st.metric("Low", stats['low_risk'])
        
        st.metric("Avg Sentiment", f"{stats['avg_sentiment']:.3f}")
        st.metric("Avg Emphasis", f"{stats['avg_emphasis']:.3f}")
    else:
        st.info("No complaints analyzed yet")
    
    st.markdown("---")
    
    if st.button("Export Database"):
        df = db.get_all_complaints()
        csv = df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            csv,
            "complaints_database.csv",
            "text/csv"
        )

# Main content - Two tabs
tab1, tab2 = st.tabs(["Analyze New Complaint", "View Database"])

# TAB 1: ANALYZE NEW COMPLAINT
with tab1:
    st.header("Enter Complaint for Analysis")
    
    # Input form
    with st.form("complaint_form"):
        # Complaint text
        complaint_text = st.text_area(
            "Complaint Text:",
            height=150,
            placeholder="Enter the customer complaint here...",
            help="Paste or type the complaint narrative"
        )
        
        # Optional metadata
        col1, col2 = st.columns(2)
        with col1:
            product = st.text_input("Product (optional)", placeholder="e.g., Credit Card")
            company = st.text_input("Company (optional)", placeholder="e.g., Bank of America")
        with col2:
            notes = st.text_area("Notes (optional)", height=100, placeholder="Any additional notes...")
        
        # Submit button
        submitted = st.form_submit_button("Analyze Complaint", use_container_width=True)
    
    # Process on submit
    if submitted:
        if not complaint_text.strip():
            st.error("Please enter a complaint text!")
        else:
            with st.spinner("Analyzing complaint..."):
                # Analyze
                result = analyzer.analyze(complaint_text)
                
                # Display results
                st.success("Analysis Complete!")
                
                # Risk Level Display
                st.markdown("### Risk Assessment")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Original Risk Level",
                        f"{result['risk_level_original']}",
                        f"Score: {result['emphasis_score']}"
                    )
                
                with col2:
                    st.metric(
                        "Sentiment",
                        result['sentiment_category'],
                        f"{result['sentiment_polarity']:+.3f}"
                    )
                
                with col3:
                    st.metric(
                        "Final Risk Level",
                        f"{result['risk_level_final']}",
                        f"Score: {result['sentiment_aware_score']}"
                    )
                
                # Detailed Analysis
                st.markdown("### Detailed Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Emphasis Features:**")
                    features_df = pd.DataFrame({
                        'Feature': [
                            'ALL-CAPS Words',
                            'Exclamation Marks',
                            'Question Marks',
                            'Repeated Punctuation',
                            'Urgent Keywords'
                        ],
                        'Count': [
                            result['features']['caps_words'],
                            result['features']['exclamations'],
                            result['features']['questions'],
                            'Yes' if result['features']['repeated_punct'] else 'No',
                            result['features']['urgent_keywords']
                        ]
                    })
                    st.dataframe(features_df, use_container_width=True, hide_index=True)
                
                with col2:
                    st.markdown("**Text Statistics:**")
                    stats_df = pd.DataFrame({
                        'Metric': [
                            'Word Count',
                            'Character Count',
                            'Emphasis Score',
                            'Sentiment Polarity',
                            'Sentiment Subjectivity',
                            'Final Score'
                        ],
                        'Value': [
                            result['features']['word_count'],
                            result['features']['char_count'],
                            f"{result['emphasis_score']:.3f}",
                            f"{result['sentiment_polarity']:.3f}",
                            f"{result['sentiment_subjectivity']:.3f}",
                            f"{result['sentiment_aware_score']:.3f}"
                        ]
                    })
                    st.dataframe(stats_df, use_container_width=True, hide_index=True)
                
                # Action Recommendation
                st.markdown("### Recommended Action")
                
                if result['risk_level_final'] == 'High':
                    st.error("""
                    URGENT - Immediate Action Required
                    - Assign to priority queue
                    - Response target: 24 hours
                    - Escalate to management
                    - Flag for legal review if needed
                    """)
                elif result['risk_level_final'] == 'Medium':
                    st.warning("""
                    Priority Handling
                    - Assign to experienced agent
                    - Response target: 48-72 hours
                    - Monitor for escalation
                    """)
                else:
                    st.info("""
                    Standard Processing
                    - Route to standard queue
                    - Response target: 5-7 business days
                    - Standard procedures apply
                    """)
                
                # Save to database
                st.markdown("---")
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown("**Save this complaint to database?**")
                
                with col2:
                    if st.button("Save to Database", use_container_width=True):
                        metadata = {
                            'product': product,
                            'company': company,
                            'notes': notes
                        }
                        
                        complaint_id = db.save_complaint(result, metadata)
                        st.success(f"Saved! Complaint ID: {complaint_id}")
                        st.rerun()

# TAB 2: VIEW DATABASE
with tab2:
    st.header("Complaint Database")
    
    df = db.get_all_complaints()
    
    if len(df) == 0:
        st.info("No complaints in database yet. Analyze and save some complaints in the 'Analyze' tab!")
    else:
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_filter = st.multiselect(
                "Filter by Risk Level:",
                options=['High', 'Medium', 'Low'],
                default=['High', 'Medium', 'Low']
            )
        
        with col2:
            sentiment_filter = st.multiselect(
                "Filter by Sentiment:",
                options=['Positive', 'Neutral', 'Negative'],
                default=['Positive', 'Neutral', 'Negative']
            )
        
        with col3:
            sort_by = st.selectbox(
                "Sort by:",
                options=['timestamp', 'emphasis_score', 'sentiment_aware_score', 'sentiment_polarity']
            )
        
        # Apply filters
        filtered_df = df[
            (df['risk_level_final'].isin(risk_filter)) &
            (df['sentiment_category'].isin(sentiment_filter))
        ].sort_values(sort_by, ascending=False)
        
        st.markdown(f"**Showing {len(filtered_df)} of {len(df)} complaints**")
        
        # Display table
        display_cols = [
            'id', 'timestamp', 'risk_level_final', 'emphasis_score',
            'sentiment_category', 'sentiment_aware_score',
            'complaint_text', 'product', 'company'
        ]
        
        st.dataframe(
            filtered_df[display_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "complaint_text": st.column_config.TextColumn("Complaint", width="large"),
                "timestamp": st.column_config.DatetimeColumn("Date/Time", format="DD/MM/YYYY HH:mm"),
                "emphasis_score": st.column_config.NumberColumn("Emphasis", format="%.3f"),
                "sentiment_aware_score": st.column_config.NumberColumn("Final Score", format="%.3f")
            }
        )
        
        # Statistics
        st.markdown("---")
        st.markdown("### Filtered Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total", len(filtered_df))
        with col2:
            st.metric("High", len(filtered_df[filtered_df['risk_level_final'] == 'High']))
        with col3:
            st.metric("Medium", len(filtered_df[filtered_df['risk_level_final'] == 'Medium']))
        with col4:
            st.metric("Low", len(filtered_df[filtered_df['risk_level_final'] == 'Low']))

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <small>Consumer Complaint Risk Analyzer | INSY 669 Project | 
    Team: Yanxin Li, Yasmine Zhao, Ellie Ha, Maral Vahedi</small>
</div>
""", unsafe_allow_html=True)