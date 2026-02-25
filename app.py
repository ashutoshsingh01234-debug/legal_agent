import streamlit as st
from pdf_utils import extract_text_from_pdf
from legal_agent import (
    summarize_notice,
    research_support,
    draft_final_document,
    create_word_document,
)
from styles import inject_custom_css
from ui_components import (
    render_sidebar_navigation,
    render_step_progress,
    render_info_card,
    render_expandable_section,
    render_status_badge,
    render_main_header,
    init_session_state,
)

# Page configuration
st.set_page_config(
    page_title="Legal Agent - GST Notice Assistant",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom styling
inject_custom_css()

# Initialize session state
init_session_state()

# SIDEBAR NAVIGATION
with st.sidebar:
    render_sidebar_navigation()

# MAIN CONTENT
# Header
render_main_header()

st.divider()

# Progress Indicator
col1, col2 = st.columns([0.1, 0.9])
with col2:
    render_step_progress(
        current_step=st.session_state.current_step,
        completed_steps=st.session_state.steps_completed,
    )

st.divider()

# Main workflow tabs
tab1, tab2, tab3, tab4 = st.tabs(
    ["📄 Upload & Summarize", "✍ Instructions", "🔍 Research & Draft", "📥 Download"]
)

# ==================== TAB 1: UPLOAD & SUMMARIZE ====================
with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📄 Upload GST Notice")
        st.markdown(
            "Select your PDF file to begin automatic analysis and summarization.\n\n"
            "**Supports:**\n"
            "- 📄 Text-based PDFs (instant)\n"
            "- 🖼️ Scanned image PDFs (using OCR)"
        )
        uploaded_pdf = st.file_uploader("Choose PDF file", type=["pdf"])

    if uploaded_pdf:
        with col2:
            st.markdown("### ⚙️ Processing...")

            # Option to force OCR for scanned documents
            force_ocr = st.checkbox(
                "Force OCR processing (for scanned notices)",
                value=False,
                help="Check this if your PDF is a scanned image"
            )

            with st.spinner("📖 Reading PDF and extracting text (this may take a moment for scanned PDFs)..."):
                extraction_result = extract_text_from_pdf(uploaded_pdf, use_ocr_first=force_ocr)

            if extraction_result['success']:
                st.session_state.pdf_text = extraction_result['text']
                if extraction_result['method'] == 'fitz':
                    method_text = "PyMuPDF (text extraction)"
                elif extraction_result['method'] == 'ocr':
                    method_text = "EasyOCR (scanned document recognition)"
                else:
                    method_text = "text extraction"
                st.success(f"✓ Text extracted successfully\n**Method:** {method_text}")
            else:
                st.session_state.pdf_text = None
                st.error(
                    f"⚠️ **Could not extract text from PDF**\n\n"
                    f"**Error:** {extraction_result['error']}\n\n"
                    f"**What you can try:**\n"
                    f"1. ☑️ Check the 'Force OCR processing' option above if this is a scanned PDF\n"
                    f"2. 🔄 Ensure the PDF file is not corrupted\n"
                    f"3. 📋 Use the manual input option below to paste the notice text"
                )

    # Manual text input option
    st.markdown("---")
    st.markdown("### 📝 Or manually enter the GST notice text")
    st.markdown("If you prefer, you can paste your notice text directly:")

    manual_text = st.text_area(
        "Paste GST notice text here",
        value=st.session_state.pdf_text or "",
        height=200,
        placeholder="Paste the text content of your GST notice here...",
        key="manual_notice_input"
    )

    if manual_text and manual_text != (st.session_state.pdf_text or ""):
        st.session_state.pdf_text = manual_text
        st.success("✓ Notice text updated")

    # Auto-summarize on upload
    if st.session_state.pdf_text and st.session_state.notice_summary is None:
        with st.spinner("🔄 Analyzing notice and generating summary..."):
            summary = summarize_notice(st.session_state.pdf_text)
        st.session_state.notice_summary = summary
        st.session_state.current_step = 2
        st.session_state.steps_completed.add(1)

    # Show summary
    if st.session_state.notice_summary:
        st.divider()

        render_expandable_section(
            title="Notice Summary",
            content=st.session_state.notice_summary,
            icon="📋",
        )

        render_status_badge("completed", "Summarization Complete")


# ==================== TAB 2: INSTRUCTIONS ====================
with tab2:
    if not st.session_state.notice_summary:
        st.info(
            "📌 Please upload and summarize a notice first in the 'Upload & Summarize' tab."
        )
    else:
        st.markdown("### Specify Your Legal Requirement")
        st.markdown(
            "Tell the assistant what action you want to take regarding this notice."
        )

        instructions = st.text_area(
            "What would you like to do?",
            value=st.session_state.instructions or "",
            placeholder="Examples:\n- Draft a reply to the Show Cause Notice\n- Request adjournment\n- File a retraction\n- Prepare for personal hearing",
            height=150,
        )

        if instructions:
            st.session_state.instructions = instructions
            st.session_state.current_step = 3

            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📝 Your request: {instructions[:100]}...")
            with col2:
                st.success("✓ Ready to generate draft in next tab")


# ==================== TAB 3: RESEARCH & DRAFT ====================
with tab3:
    if not st.session_state.instructions:
        st.info(
            "📌 Please specify your legal requirement in the 'Instructions' tab first."
        )
    else:
        st.markdown("### Generate Legal Document")
        st.markdown(
            "The AI will research relevant case laws and draft your legal response."
        )

        if st.button("🚀 Generate Draft", type="primary", use_container_width=True):
            # Progress indicators
            progress_placeholder = st.empty()
            status_placeholder = st.empty()
            progress_bar = st.progress(0)

            # Step 1: Research
            status_placeholder.markdown(
                "### 🔍 Step 1/2: Researching Case Laws & Provisions"
            )
            progress_bar.progress(10)

            with st.spinner("Querying legal databases..."):
                research_note = research_support(
                    st.session_state.instructions, st.session_state.notice_summary
                )
            st.session_state.research_note = research_note
            progress_bar.progress(50)

            # Step 2: Draft
            status_placeholder.markdown(
                "### 📝 Step 2/2: Drafting Legal Document"
            )
            progress_bar.progress(75)

            with st.spinner("Generating professional response..."):
                final_draft = draft_final_document(
                    st.session_state.instructions,
                    st.session_state.notice_summary,
                    st.session_state.research_note,
                )
            st.session_state.final_draft = final_draft
            st.session_state.current_step = 4
            st.session_state.steps_completed.add(3)
            st.session_state.steps_completed.add(4)

            progress_bar.progress(100)
            status_placeholder.markdown("### ✅ Draft Generation Complete!")
            st.balloons()

        st.divider()

        # Display research
        if st.session_state.research_note:
            render_expandable_section(
                title="Research & Case Laws",
                content=st.session_state.research_note,
                icon="🔍",
            )

        # Display final draft
        if st.session_state.final_draft:
            render_expandable_section(
                title="Draft Document",
                content=st.session_state.final_draft,
                icon="📝",
            )
            render_status_badge("completed", "Draft Generation Complete")


# ==================== TAB 4: DOWNLOAD ====================
with tab4:
    if not st.session_state.final_draft:
        st.info(
            "📌 Please generate the draft document in the 'Research & Draft' tab first."
        )
    else:
        st.markdown("### Download Your Legal Document")
        st.markdown("Your draft is ready for download and further editing.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📥 Word Document")
            st.markdown(
                "Download as .docx file for editing in Microsoft Word or other editors."
            )
            docx_buffer = create_word_document(st.session_state.final_draft)
            st.download_button(
                label="⬇️ Download as Word Document",
                data=docx_buffer,
                file_name="gst_notice_response.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
            st.session_state.steps_completed.add(5)

        with col2:
            st.markdown("#### 📋 Preview")
            with st.expander("View Full Text", expanded=False):
                st.text(st.session_state.final_draft)

        st.divider()
        st.markdown("""
        #### ⚠️ Important Notes
        - **Review carefully** before submitting to authorities
        - **Consult a qualified lawyer** for final approval
        - **Customize** the document as per your specific requirements
        - **Keep records** of all communications and documents
        """)

        render_status_badge("completed", "Ready for Download")
