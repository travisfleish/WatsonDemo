import streamlit as st
import os
import json
import time
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from dotenv import load_dotenv
import threading
import uuid
import pandas as pd

# Import our research proposal generation system
from main import main as generate_proposals
from utils.helpers import validate_json_output

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("streamlit_app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Email Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# Set page configuration
st.set_page_config(
    page_title="Research Proposal Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2563EB;
        margin-bottom: 0.5rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .status-running {
        background-color: #DBEAFE;
        border-left: 5px solid #3B82F6;
    }
    .status-complete {
        background-color: #DCFCE7;
        border-left: 5px solid #22C55E;
    }
    .status-error {
        background-color: #FEE2E2;
        border-left: 5px solid #EF4444;
    }
    .paper-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    .proposal-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #F0F9FF;
        border: 1px solid #BAE6FD;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)


def send_email_with_proposals(recipient_email, proposals, session_id):
    """
    Send email with research proposals as HTML content.

    Args:
        recipient_email (str): Email address to send to
        proposals (list): List of research proposal dictionaries
        session_id (str): Unique session identifier

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        if not EMAIL_SENDER or not EMAIL_PASSWORD:
            logger.error("Email credentials not configured")
            return False

        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = recipient_email
        msg['Subject'] = f"Research Proposals Generated - Session {session_id[:8]}"

        # Create HTML for each proposal
        proposals_html = ""
        for i, proposal in enumerate(proposals, 1):
            title = proposal.get("proposal_title", f"Proposal {i}")
            introduction = proposal.get("introduction", "No introduction provided")
            methodology = proposal.get("methodology", "No methodology provided")
            outcomes = proposal.get("expected_outcomes", "No outcomes specified")

            # Format research questions
            questions_html = "<ul>"
            for q in proposal.get("research_questions", []):
                questions_html += f"<li>{q}</li>"
            questions_html += "</ul>"

            proposals_html += f"""
            <div style="margin-bottom: 30px; border: 1px solid #ccc; padding: 20px; border-radius: 5px;">
                <h2 style="color: #1E3A8A;">{title}</h2>
                <h3>Introduction</h3>
                <p>{introduction}</p>

                <h3>Research Questions</h3>
                {questions_html}

                <h3>Methodology</h3>
                <p>{methodology[:500]}...</p>

                <h3>Expected Outcomes</h3>
                <p>{outcomes[:500]}...</p>
            </div>
            """

        # Email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h1 style="color: #1E3A8A;">Research Proposals Generated</h1>
            <p>Your research proposal generation process has completed.</p>
            <p>Session ID: {session_id}</p>
            <hr>

            <h2>Generated Proposals</h2>
            {proposals_html}

            <hr>
            <p>Thank you for using our Research Proposal Generator!</p>
            <p><em>Note: For the complete proposals with all details, please use the app's download functionality.</em></p>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html'))

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        logger.info(f"Email sent successfully to {recipient_email}")
        return True

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return False


def run_proposal_generation(input_paper, recipient_email, session_id):
    """
    Run the research proposal generation process in a separate thread.

    Args:
        input_paper (str): Title of the input paper
        recipient_email (str): Email to send results to
        session_id (str): Unique session identifier
    """
    try:
        # Update session state
        st.session_state.current_stage = "paper_finding"
        st.session_state.status = "running"
        st.session_state.progress = 10
        time.sleep(1)  # Let the UI update

        # Generate output directory based on session ID
        output_dir = f"output_{session_id}"

        # Run the main process with custom logging for UI updates
        proposals = generate_proposals(input_paper, output_dir)

        # Store results in session state
        st.session_state.proposals = proposals
        st.session_state.status = "complete"
        st.session_state.progress = 100

        # Send email with results if email is provided
        if recipient_email:
            email_sent = send_email_with_proposals(recipient_email, proposals, session_id)
            st.session_state.email_sent = email_sent

    except Exception as e:
        logger.error(f"Error in proposal generation: {str(e)}", exc_info=True)
        st.session_state.status = "error"
        st.session_state.error_message = str(e)


def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "status" not in st.session_state:
        st.session_state.status = "idle"

    if "current_stage" not in st.session_state:
        st.session_state.current_stage = None

    if "progress" not in st.session_state:
        st.session_state.progress = 0

    if "proposals" not in st.session_state:
        st.session_state.proposals = None

    if "email_sent" not in st.session_state:
        st.session_state.email_sent = None

    if "error_message" not in st.session_state:
        st.session_state.error_message = None


def main():
    """Main Streamlit application."""
    initialize_session_state()

    # Header
    st.markdown('<h1 class="main-header">Research Proposal Generator</h1>', unsafe_allow_html=True)
    st.markdown("""
    This application generates novel research proposals based on existing scientific papers using a multi-agent AI system.
    Enter a research paper title below to start the generation process.
    """)

    # Sidebar
    st.sidebar.markdown('<h2 class="sub-header">Configuration</h2>', unsafe_allow_html=True)

    # Input form
    with st.sidebar.form("input_form"):
        input_paper = st.text_input(
            "Research Paper Title",
            value="Advanced Machine Learning Techniques for Scientific Discovery",
            help="Enter the title of a research paper to base new proposals on"
        )

        recipient_email = st.text_input(
            "Email Address (Optional)",
            help="Enter your email to receive the proposals"
        )

        submit_button = st.form_submit_button("Generate Proposals")

    # Handle form submission
    if submit_button:
        # Reset state for new run
        st.session_state.status = "starting"
        st.session_state.progress = 0
        st.session_state.proposals = None
        st.session_state.email_sent = None
        st.session_state.error_message = None

        # Start generation in a separate thread
        thread = threading.Thread(
            target=run_proposal_generation,
            args=(input_paper, recipient_email, st.session_state.session_id)
        )
        thread.daemon = True
        thread.start()

    # Display current status
    st.markdown('<h2 class="sub-header">Generation Status</h2>', unsafe_allow_html=True)

    # Status indicator and progress bar
    if st.session_state.status == "idle":
        st.info("Enter a research paper title and click 'Generate Proposals' to start.")

    elif st.session_state.status == "starting":
        st.markdown('<div class="status-box status-running">Starting proposal generation...</div>',
                    unsafe_allow_html=True)
        st.progress(0)

    elif st.session_state.status == "running":
        # Determine progress based on current stage
        progress_map = {
            "paper_finding": 20,
            "paper_analysis": 40,
            "idea_generation": 60,
            "idea_refinement": 80,
            "proposal_development": 90
        }
        current_progress = progress_map.get(st.session_state.current_stage, st.session_state.progress)

        # Update progress in session state
        st.session_state.progress = max(st.session_state.progress, current_progress)

        # Display stage-specific message
        stage_messages = {
            "paper_finding": "Finding relevant research papers...",
            "paper_analysis": "Analyzing research papers...",
            "idea_generation": "Generating initial research ideas...",
            "idea_refinement": "Refining research ideas...",
            "proposal_development": "Developing complete research proposals..."
        }
        current_message = stage_messages.get(st.session_state.current_stage, "Processing...")

        st.markdown(f'<div class="status-box status-running">{current_message}</div>', unsafe_allow_html=True)
        st.progress(st.session_state.progress / 100)

    elif st.session_state.status == "complete":
        st.markdown('<div class="status-box status-complete">Proposal generation complete!</div>',
                    unsafe_allow_html=True)
        st.progress(1.0)

        # Email status if email was provided
        if recipient_email:
            if st.session_state.email_sent:
                st.success(f"Proposals sent to {recipient_email}")
            else:
                st.warning(
                    f"Failed to send email to {recipient_email}. You can still view and download the proposals below.")

    elif st.session_state.status == "error":
        st.markdown('<div class="status-box status-error">Error in proposal generation!</div>', unsafe_allow_html=True)
        st.error(st.session_state.error_message)

    # Display results if available
    if st.session_state.proposals:
        st.markdown('<h2 class="sub-header">Generated Research Proposals</h2>', unsafe_allow_html=True)

        proposals = st.session_state.proposals

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Proposal Cards", "Detailed View", "Download Options"])

        with tab1:
            # Display proposal cards
            for i, proposal in enumerate(proposals, 1):
                title = proposal.get("proposal_title", f"Proposal {i}")
                methodology = proposal.get("methodology", "No methodology provided")
                outcomes = proposal.get("expected_outcomes", "No outcomes specified")

                st.markdown(f"""
                <div class="proposal-card">
                    <h3>{title}</h3>
                    <p><strong>Methodology:</strong> {methodology[:200]}...</p>
                    <p><strong>Expected Outcomes:</strong> {outcomes[:200]}...</p>
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            # Create a selection dropdown for proposals
            proposal_titles = [prop.get("proposal_title", f"Proposal {i}") for i, prop in enumerate(proposals, 1)]
            selected_title = st.selectbox("Select a proposal to view", proposal_titles)

            # Find the selected proposal
            selected_index = proposal_titles.index(selected_title)
            selected_proposal = proposals[selected_index]

            # Display detailed proposal
            st.markdown(f"## {selected_title}")

            # Create expandable sections for each part
            with st.expander("Introduction", expanded=True):
                st.write(selected_proposal.get("introduction", "No introduction provided"))

            with st.expander("Research Questions"):
                questions = selected_proposal.get("research_questions", [])
                for q in questions:
                    st.markdown(f"- {q}")

            with st.expander("Hypotheses"):
                hypotheses = selected_proposal.get("hypotheses", [])
                for h in hypotheses:
                    st.markdown(f"- {h}")

            with st.expander("Methodology"):
                st.write(selected_proposal.get("methodology", "No methodology provided"))

            with st.expander("Expected Outcomes"):
                st.write(selected_proposal.get("expected_outcomes", "No outcomes specified"))

            with st.expander("Potential Challenges"):
                st.write(selected_proposal.get("potential_challenges", "No challenges specified"))

            with st.expander("Ethical Considerations"):
                st.write(selected_proposal.get("ethical_considerations", "No ethical considerations specified"))

            with st.expander("Resource Requirements"):
                st.write(selected_proposal.get("resource_requirements", "No resource requirements specified"))

            with st.expander("Timeline"):
                st.write(selected_proposal.get("timeline", "No timeline specified"))

            with st.expander("References"):
                references = selected_proposal.get("references", [])
                for r in references:
                    st.markdown(f"- {r}")

        with tab3:
            st.markdown("### Download Options")

            # Download all proposals as JSON
            st.markdown("#### Download All Proposals (JSON)")
            json_data = json.dumps(proposals, indent=2)
            st.download_button(
                label="Download All Proposals (JSON)",
                data=json_data,
                file_name="research_proposals.json",
                mime="application/json",
            )

            # Download each proposal as text
            st.markdown("#### Download Individual Proposals (Text)")
            for i, proposal in enumerate(proposals, 1):
                title = proposal.get("proposal_title", f"Proposal {i}")
                # Create clean filename
                filename = "".join(c if c.isalnum() else "_" for c in title).lower()

                # Format proposal as text
                proposal_text = f"# {title}\n\n"
                proposal_text += f"## Introduction\n{proposal.get('introduction', '')}\n\n"

                proposal_text += "## Research Questions\n"
                for q in proposal.get("research_questions", []):
                    proposal_text += f"- {q}\n"
                proposal_text += "\n"

                proposal_text += "## Hypotheses\n"
                for h in proposal.get("hypotheses", []):
                    proposal_text += f"- {h}\n"
                proposal_text += "\n"

                proposal_text += f"## Methodology\n{proposal.get('methodology', '')}\n\n"
                proposal_text += f"## Expected Outcomes\n{proposal.get('expected_outcomes', '')}\n\n"
                proposal_text += f"## Potential Challenges\n{proposal.get('potential_challenges', '')}\n\n"
                proposal_text += f"## Ethical Considerations\n{proposal.get('ethical_considerations', '')}\n\n"
                proposal_text += f"## Resource Requirements\n{proposal.get('resource_requirements', '')}\n\n"
                proposal_text += f"## Timeline\n{proposal.get('timeline', '')}\n\n"

                proposal_text += "## References\n"
                for r in proposal.get("references", []):
                    proposal_text += f"- {r}\n"

                st.download_button(
                    label=f"Download {title} (Text)",
                    data=proposal_text,
                    file_name=f"{filename}.txt",
                    mime="text/plain",
                )


if __name__ == "__main__":
    main()