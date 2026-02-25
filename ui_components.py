import streamlit as st
from styles import create_status_indicator, create_step_badge


def render_sidebar_navigation():
    """
    Render professional sidebar navigation with app info and guides.
    """
    st.markdown(
        """
        <div class="sidebar-section">
            <div class="sidebar-heading">⚖ Legal Agent</div>
            <p class="sidebar-text">Professional GST Notice Analysis & Drafting Assistant</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📖 How to Use", expanded=False):
        st.markdown(
            """
            **Step-by-step guide:**

            1. **Upload PDF** - Select your GST notice PDF file
            2. **Summarize** - AI automatically extracts key information
            3. **Instructions** - Tell us what action you need (e.g., draft reply)
            4. **Research** - AI finds relevant case laws and provisions
            5. **Draft** - AI generates a professional legal response
            6. **Download** - Get your draft as a Word document

            **Tips:**
            - Ensure your PDF has selectable text (not scanned images)
            - Be specific in your instructions for better results
            - Review the AI-generated content before use
            - Consult a lawyer for final approval
            """
        )

    with st.expander("💡 Sample Use Cases", expanded=False):
        st.markdown(
            """
            - Draft a reply to Show Cause Notice (SCN)
            - Request adjournment of proceedings
            - File a retraction/rectification
            - Prepare for personal hearing
            - Challenge provisional assessment
            - Request stay of demand
            """
        )

    st.markdown(
        """
        <div class="sidebar-section">
            <div class="sidebar-heading">ℹ About</div>
            <p class="sidebar-text">
            This tool leverages advanced AI to help lawyers analyze GST notices
            and draft professional legal responses efficiently.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("⚙ Settings", expanded=False):
        st.markdown("**Theme**: Dark Mode (Professional)")
        st.markdown("**API**: OpenAI + Perplexity")
        st.markdown("**Version**: 1.0")

    st.markdown(
        """
        <div class="sidebar-section">
            <p class="sidebar-text" style="text-align: center; font-size: 0.85rem; color: var(--text-muted);">
            Developed with ⚖ for Legal Professionals
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_step_progress(current_step, completed_steps):
    """
    Render visual step progress indicator for the workflow.
    Steps: 1=Upload, 2=Summarize, 3=Instructions, 4=Research, 5=Draft, 6=Download
    """
    steps = [
        (1, "Upload"),
        (2, "Summarize"),
        (3, "Instructions"),
        (4, "Research"),
        (5, "Draft"),
        (6, "Download"),
    ]

    progress_html = '<div class="progress-container">'

    for idx, (step_num, step_label) in enumerate(steps):
        if step_num in completed_steps:
            status = "completed"
        elif step_num == current_step:
            status = "active"
        else:
            status = "pending"

        progress_html += create_step_badge(step_num, status, step_label)

        # Add line between steps (not after last step)
        if idx < len(steps) - 1:
            line_class = (
                "progress-line completed"
                if step_num in completed_steps
                else "progress-line"
            )
            progress_html += f'<div class="{line_class}"></div>'

    progress_html += "</div>"
    st.markdown(progress_html, unsafe_allow_html=True)


def render_info_card(title, content, icon="📋", status="neutral"):
    """
    Render a professional information card.
    """
    html = f"""
    <div class="info-card">
        <div class="card-title">
            <span class="card-icon">{icon}</span>
            <span>{title}</span>
        </div>
        <div class="card-content">
            {content}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_expandable_section(title, content, icon="📋"):
    """
    Render a custom expandable section with professional styling.
    """
    with st.expander(f"{icon} {title}", expanded=False):
        st.markdown(content)


def render_status_badge(status, label):
    """
    Render a status indicator badge.
    Status: 'completed', 'in_progress', or 'pending'
    """
    status_map = {
        "completed": "completed",
        "in_progress": "in_progress",
        "pending": "pending",
    }
    badge_status = status_map.get(status, "pending")
    st.markdown(
        create_status_indicator(badge_status), unsafe_allow_html=True
    )


def render_loading_message(step_name, substeps):
    """
    Enhanced loading indicator with step details.
    """
    with st.spinner(f"**{step_name}**"):
        # Display substeps as they would happen
        progress_placeholder = st.empty()
        for idx, substep in enumerate(substeps):
            progress_placeholder.markdown(
                f"**Step {idx + 1}/{len(substeps)}:** {substep}"
            )


def render_download_section(draft_content, file_name="gst_draft"):
    """
    Render professional download section with options.
    """
    st.markdown(
        """
        <div class="download-section">
            <div class="download-title">📥 Download Your Draft</div>
            <div class="download-description">
            Your legal document is ready. Download in Word format for further editing.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Copy to Clipboard**")
        st.code(draft_content, language="text")

    with col2:
        st.markdown("**Download as Word**")
        st.info(
            "Use the download button below to save as .docx file"
        )


def render_main_header():
    """
    Render the main app header with professional styling.
    """
    st.markdown(
        """
        <div style="text-align: center; margin: 2rem 0;">
            <h1 style="color: #ECF0F1; margin-bottom: 0.5rem;">⚖ Legal Notice Assistant</h1>
            <p style="color: #BDC3C7; font-size: 1.1rem;">Professional GST Notice Analysis, Research & Drafting</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def init_session_state():
    """
    Initialize all required session state variables.
    """
    defaults = {
        "pdf_text": None,
        "notice_summary": None,
        "research_note": None,
        "final_draft": None,
        "instructions": None,
        "current_step": 1,
        "steps_completed": set(),
        "ui_expand_states": {},
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
