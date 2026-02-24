import streamlit as st
from pdf_utils import extract_text_from_pdf
from legal_agent import (
    summarize_notice,
    research_support,
    draft_final_document,
    create_word_document,
)

st.title("GST Notice Assistant – Summarise, Research, Draft")

uploaded_pdf = st.file_uploader("Upload GST Notice PDF", type=["pdf"])

# Session state
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None
if "notice_summary" not in st.session_state:
    st.session_state.notice_summary = None
if "research_note" not in st.session_state:
    st.session_state.research_note = None
if "final_draft" not in st.session_state:
    st.session_state.final_draft = None

# STEP 1 & 2: Auto-summarize on upload
if uploaded_pdf:
    pdf_text = extract_text_from_pdf(uploaded_pdf)
    st.session_state.pdf_text = pdf_text

    if not pdf_text:
        st.error("Could not extract any text from the PDF. It may be a scanned image without embedded text.")
    else:
        with st.spinner("Summarising notice..."):
            summary = summarize_notice(pdf_text)
        st.session_state.notice_summary = summary

# Show summary
if st.session_state.notice_summary:
    st.write("### Notice Summary")
    st.write(st.session_state.notice_summary)

# STEP 3: Ask user what they want to do
if st.session_state.notice_summary:
    st.write("---")
    st.write("Step 3: Tell the assistant what you want to do.")
    instructions = st.text_area(
        "Describe what you want (e.g., draft reply to SCN, adjournment request, retraction, etc.)"
    )

    # STEP 4 & 5: Research + Draft
    if instructions and st.button("Generate Draft"):
        with st.spinner("Researching relevant case laws and references..."):
            research_note = research_support(instructions, st.session_state.notice_summary)
        st.session_state.research_note = research_note

        with st.spinner("Drafting final document..."):
            final_draft = draft_final_document(
                instructions,
                st.session_state.notice_summary,
                st.session_state.research_note,
            )
        st.session_state.final_draft = final_draft

# STEP 6 & 7: Show final draft
if st.session_state.final_draft:
    st.write("---")
    st.write("### Final Draft")
    st.write(st.session_state.final_draft)

    # STEP 8: Download as Word
    docx_buffer = create_word_document(st.session_state.final_draft)
    st.download_button(
        label="Download Draft as Word Document",
        data=docx_buffer,
        file_name="gst_draft.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
