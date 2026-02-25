import streamlit as st


def inject_custom_css():
    """
    Inject custom CSS for professional dark blue & gold theme.
    Includes styling for step indicators, cards, expanders, badges, and responsive design.
    """
    st.markdown(
        """
        <style>
        /* Color Variables */
        :root {
            --primary-blue: #1A3A52;
            --secondary-blue: #2D5A7B;
            --accent-gold: #D4AF37;
            --text-light: #ECF0F1;
            --text-muted: #BDC3C7;
            --bg-dark: #0F1419;
            --bg-card: #1A2332;
            --success: #27AE60;
            --pending: #E67E22;
        }

        /* Root styling */
        html, body {
            background-color: var(--bg-dark);
            color: var(--text-light);
        }

        .main {
            background-color: var(--bg-dark);
        }

        .stSidebar {
            background-color: var(--secondary-blue);
        }

        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-light) !important;
        }

        p {
            color: var(--text-light);
        }

        /* Progress Container and Steps */
        .progress-container {
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 2rem 1rem;
            background-color: var(--bg-card);
            border-radius: 8px;
            margin: 1.5rem 0;
            gap: 0.5rem;
        }

        .progress-step {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
            flex: 1;
        }

        .step-circle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1rem;
            transition: all 0.3s ease;
            border: 2px solid var(--text-muted);
            background-color: var(--bg-dark);
            color: var(--text-muted);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        }

        .step-circle.completed {
            background-color: var(--success);
            color: white;
            border-color: var(--success);
            box-shadow: 0 4px 8px rgba(39, 174, 96, 0.3);
        }

        .step-circle.active {
            background-color: var(--accent-gold);
            color: var(--primary-blue);
            border-color: var(--accent-gold);
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
            animation: pulse-gold 2s infinite;
        }

        .step-circle.pending {
            background-color: var(--bg-dark);
            color: var(--text-muted);
            border-color: var(--text-muted);
        }

        .step-label {
            font-size: 0.85rem;
            color: var(--text-muted);
            text-align: center;
            word-break: break-word;
            max-width: 100px;
        }

        .step-label.active {
            color: var(--accent-gold);
            font-weight: 600;
        }

        .step-label.completed {
            color: var(--success);
            font-weight: 600;
        }

        @keyframes pulse-gold {
            0%, 100% {
                box-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
            }
            50% {
                box-shadow: 0 0 25px rgba(212, 175, 55, 0.8);
            }
        }

        /* Separator line in progress indicator */
        .progress-line {
            height: 2px;
            flex-grow: 1;
            background: linear-gradient(to right, var(--text-muted), var(--text-muted));
            margin: 0 0.5rem;
        }

        .progress-line.completed {
            background: linear-gradient(to right, var(--success), var(--success));
        }

        /* Information Cards */
        .info-card {
            background-color: var(--bg-card);
            border-left: 4px solid var(--accent-gold);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }

        .info-card:hover {
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.2);
            border-left-color: var(--accent-gold);
        }

        .card-title {
            color: var(--accent-gold);
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .card-icon {
            font-size: 1.5rem;
        }

        .card-content {
            color: var(--text-light);
            line-height: 1.6;
            font-size: 0.95rem;
        }

        /* Expandable Sections */
        .streamlit-expanderHeader {
            background-color: var(--bg-card) !important;
            border-left: 4px solid var(--accent-gold) !important;
            border-radius: 4px !important;
            transition: all 0.3s ease !important;
        }

        .streamlit-expanderHeader:hover {
            background-color: var(--primary-blue) !important;
            box-shadow: 0 2px 6px rgba(212, 175, 55, 0.2) !important;
        }

        .streamlit-expanderHeader p {
            color: var(--accent-gold) !important;
            font-weight: 600 !important;
            font-size: 1.05rem !important;
        }

        .streamlit-expanderContent {
            background-color: var(--bg-card) !important;
            border: 1px solid rgba(212, 175, 55, 0.2) !important;
            border-top: none !important;
        }

        /* Status Badges */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            width: fit-content;
        }

        .status-completed {
            background-color: rgba(39, 174, 96, 0.15);
            color: var(--success);
            border: 1px solid var(--success);
        }

        .status-in-progress {
            background-color: rgba(212, 175, 55, 0.15);
            color: var(--accent-gold);
            border: 1px solid var(--accent-gold);
            animation: pulse-badge 2s infinite;
        }

        .status-pending {
            background-color: rgba(127, 140, 141, 0.15);
            color: var(--text-muted);
            border: 1px solid var(--text-muted);
        }

        @keyframes pulse-badge {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.7;
            }
        }

        /* Button Styling */
        .stButton > button {
            background-color: var(--accent-gold) !important;
            color: var(--primary-blue) !important;
            border: none !important;
            font-weight: 700 !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s ease !important;
            border-radius: 6px !important;
            padding: 0.6rem 1.5rem !important;
            font-size: 0.95rem !important;
        }

        .stButton > button:hover {
            background-color: var(--text-light) !important;
            box-shadow: 0 6px 16px rgba(212, 175, 55, 0.4) !important;
            transform: translateY(-2px) !important;
        }

        .stButton > button:active {
            transform: translateY(0px) !important;
        }

        /* Primary buttons */
        .stButton > button[kind="primary"] {
            background-color: var(--accent-gold) !important;
        }

        /* Secondary buttons */
        .stButton > button[kind="secondary"] {
            background-color: var(--bg-card) !important;
            color: var(--accent-gold) !important;
            border: 1px solid var(--accent-gold) !important;
        }

        .stButton > button[kind="secondary"]:hover {
            background-color: var(--primary-blue) !important;
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3) !important;
        }

        /* Input fields */
        .stTextInput input,
        .stTextArea textarea {
            background-color: var(--bg-card) !important;
            color: var(--text-light) !important;
            border: 1px solid var(--text-muted) !important;
            border-radius: 6px !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: var(--accent-gold) !important;
            box-shadow: 0 0 8px rgba(212, 175, 55, 0.3) !important;
        }

        /* File uploader */
        .stFileUploader {
            border: 2px dashed var(--accent-gold) !important;
            border-radius: 8px !important;
            padding: 1.5rem !important;
            background-color: var(--bg-card) !important;
        }

        /* Dividers */
        .stDivider {
            border-color: var(--accent-gold) !important;
            opacity: 0.5;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] button {
            color: var(--text-muted) !important;
            border-bottom: 2px solid transparent !important;
            transition: all 0.3s ease !important;
        }

        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            color: var(--accent-gold) !important;
            border-bottom-color: var(--accent-gold) !important;
        }

        .stTabs [data-baseweb="tab-list"] button:hover {
            color: var(--accent-gold) !important;
        }

        /* Spinners and loading */
        .stSpinner {
            color: var(--accent-gold) !important;
        }

        /* Alerts and messages */
        .stAlert {
            border-radius: 6px !important;
        }

        .AlertContainer_success {
            background-color: rgba(39, 174, 96, 0.15) !important;
            border-left: 4px solid var(--success) !important;
        }

        .AlertContainer_warning {
            background-color: rgba(230, 126, 34, 0.15) !important;
            border-left: 4px solid var(--pending) !important;
        }

        .AlertContainer_error {
            background-color: rgba(231, 76, 60, 0.15) !important;
            border-left: 4px solid #E74C3C !important;
        }

        .AlertContainer_info {
            background-color: rgba(52, 152, 219, 0.15) !important;
            border-left: 4px solid #3498DB !important;
        }

        /* Main header styling */
        .main-header {
            color: var(--text-light);
            margin: 2rem 0 1rem 0;
        }

        .main-subtitle {
            color: var(--text-muted);
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }

        /* Sidebar sections */
        .sidebar-section {
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(212, 175, 55, 0.2);
        }

        .sidebar-section:last-child {
            border-bottom: none;
        }

        .sidebar-heading {
            color: var(--accent-gold);
            font-size: 1.1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.75rem;
        }

        .sidebar-text {
            color: var(--text-light);
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* Container and spacing */
        .main-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 1rem;
        }

        /* Download section */
        .download-section {
            background: linear-gradient(135deg, var(--bg-card), var(--primary-blue) 100%);
            border: 2px solid var(--accent-gold);
            border-radius: 8px;
            padding: 2rem;
            margin: 2rem 0;
            text-align: center;
        }

        .download-title {
            color: var(--accent-gold);
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .download-description {
            color: var(--text-muted);
            margin-bottom: 1.5rem;
            font-size: 0.95rem;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .progress-container {
                flex-direction: column;
                padding: 1.5rem 1rem;
            }

            .progress-step {
                width: 100%;
                padding: 0.75rem 0;
            }

            .progress-line {
                width: 100%;
                height: 2px;
                margin: 0.5rem 0;
            }

            .step-circle {
                width: 40px;
                height: 40px;
                font-size: 0.9rem;
            }

            .step-label {
                font-size: 0.8rem;
                max-width: 80px;
            }

            .info-card {
                padding: 1rem;
                margin: 1rem 0;
            }

            .card-title {
                font-size: 1.1rem;
            }

            .card-content {
                font-size: 0.9rem;
            }

            .download-section {
                padding: 1.5rem;
            }

            .download-title {
                font-size: 1.2rem;
            }
        }

        @media (max-width: 480px) {
            .step-circle {
                width: 35px;
                height: 35px;
                font-size: 0.8rem;
            }

            .step-label {
                font-size: 0.7rem;
                max-width: 70px;
            }

            .card-title {
                font-size: 1rem;
            }

            .info-card {
                margin: 0.75rem 0;
                padding: 0.75rem;
            }

            .status-badge {
                padding: 0.4rem 0.8rem;
                font-size: 0.8rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def create_step_badge(step_num, status, label):
    """
    Create an HTML step indicator badge.
    Status: 'completed', 'active', or 'pending'
    """
    status_classes = {
        "completed": "step-circle completed",
        "active": "step-circle active",
        "pending": "step-circle pending",
    }
    label_classes = {
        "completed": "step-label completed",
        "active": "step-label active",
        "pending": "step-label",
    }

    circle_class = status_classes.get(status, "step-circle pending")
    label_class = label_classes.get(status, "step-label")

    icons = {"completed": "✓", "active": "●", "pending": "◦"}
    icon = icons.get(status, "◦")

    html = f"""
    <div class="progress-step">
        <div class="{circle_class}">{step_num if status != 'completed' else '✓'}</div>
        <div class="{label_class}">{label}</div>
    </div>
    """
    return html


def create_status_indicator(status):
    """
    Create an HTML status indicator badge.
    Status: 'completed', 'in_progress', or 'pending'
    """
    status_map = {
        "completed": ("✓ Completed", "status-completed"),
        "in_progress": ("⏳ In Progress", "status-in-progress"),
        "pending": ("○ Pending", "status-pending"),
    }

    label, css_class = status_map.get(status, ("Unknown", "status-pending"))
    return f'<span class="status-badge {css_class}">{label}</span>'


def create_divider(color="gold"):
    """
    Create a styled divider.
    """
    st.divider()
