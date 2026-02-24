import streamlit as st
from gst_ai_agent import gst_ai_agent


st.title("GST Legal Drafting AI Assistant")

task = st.selectbox("Select Task", [
    "Adjournment Application",
    "Retraction of Statement",
    "SCN Summary",
    "SCN Reply"
])

details = st.text_area("Enter case details")

if st.button("Generate Draft"):
    mapping = {
        "Adjournment Application": "adjournment",
        "Retraction of Statement": "retraction",
        "SCN Summary": "scn_summary",
        "SCN Reply": "scn_reply"
    }
    result = gst_ai_agent(mapping[task], details)
    st.write(result)
