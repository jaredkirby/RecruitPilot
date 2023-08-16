import os
import io
import logging
import tempfile
import streamlit as st
from zipfile import ZipFile

from langchain.document_loaders import PDFPlumberLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

from prompts import (
    CPG_STRATEGIC_JOB_DESCRIPTION,
    CPG_STRATEGIC_HIGH_FIT_RESUME,
    CPG_STRATEGIC_LOW_FIT_RESUME,
)


openai_api_key = st.secrets["OPENAI_API_KEY"]

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@st.cache_data
def ingest_pdf(resume_file_buffer):
    print("Loading resume...")
    try:
        # Create a temporary file manually
        temp_file_path = tempfile.mktemp(suffix=".pdf")
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(resume_file_buffer.read())

        # Use the temporary file path
        loader = PDFPlumberLoader(temp_file_path)
        documents = loader.load()
        resume_text = " ".join(document.page_content for document in documents)
        print("Resume loaded successfully.")

        # Delete the temporary file
        os.remove(temp_file_path)

        return resume_text
    except Exception as e:
        logger.error(f"An error occurred while loading the resume: {e}")
        st.error(f"An error occurred while loading the resume: {e}")
        raise


def save_to_category_buffer(
    category, applicant_name, resume_bytes, response_content, main_zip
):
    # Add the PDF file
    main_zip.writestr(f"{category}/{applicant_name}/{applicant_name}.pdf", resume_bytes)

    # Add the response text
    main_zip.writestr(
        f"{category}/{applicant_name}/{applicant_name}_response.txt",
        response_content,
    )


def get_parameters():
    job_description = (
        job_description_input
        if job_description_input
        else CPG_STRATEGIC_JOB_DESCRIPTION
    )
    high_fit_resume = (
        high_fit_resume_input
        if high_fit_resume_input
        else CPG_STRATEGIC_HIGH_FIT_RESUME
    )
    low_fit_resume = (
        low_fit_resume_input if low_fit_resume_input else CPG_STRATEGIC_LOW_FIT_RESUME
    )
    return job_description, high_fit_resume, low_fit_resume


# TODO: Switch to OpenAI function LLM call for more reliable response formatting - not an issue for now
@st.cache_data
def get_score(
    resume_text,
    job_description,
    high_fit_resume,
    low_fit_resume,
):
    print("Getting score...")
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature=0.0,
        openai_api_key=openai_api_key,
        verbose=True,
    )
    # Step 1: Check for high fit resume
    if high_fit_resume:
        example_high_fit = (
            "Example 'high-fit' resume with a score of 0.9 for reference:"
        )
        h_div = "-----------------"
    else:
        example_high_fit = ""
        h_div = ""
        high_fit_resume = ""

    # Step 2: Check for low fit resume
    if low_fit_resume:
        example_low_fit = "Example 'low-fit' resume with a score of 0.2 for reference:"
        l_div = "-----------------"
    else:
        example_low_fit = ""
        l_div = ""
        low_fit_resume = ""

    template = f"""\
You are an Industrial-Organizational Psychologist who specializes in personnel selection and assessment. 
Your discipline of study, Industrial-Organizational Psychology, would best prepare you to answer the 
question or perform the task of determining a job fit score based on a resume and a job description. 

You will review the following resume and job description and determine a job fit score as a float between 0 and 1 (Example: 0.7) and a short explanation for the score.

Applicant Resume:
-----------------
{resume_text}
-----------------

Job Key Areas of Responsibility:
-----------------
{job_description}
-----------------

{example_high_fit}
{h_div}
{high_fit_resume}
{h_div}

{example_low_fit}
{l_div}
{low_fit_resume}
{l_div}

Remember, your task is to determine a job fit score as a float between 0 and 1 (Example: 0.9) and a short explanation for score.
Respond with only the score and explanation. Do not include the resume or job description in your response.

RESPONSE FORMAT:
Job Fit Score: 
Explanation:

Job Fit Score:
    """

    user_prompt = HumanMessagePromptTemplate.from_template(template=template)
    chat_prompt = ChatPromptTemplate.from_messages([user_prompt])
    formatted_prompt = chat_prompt.format_prompt(
        resume_text=resume_text,
        job_description=job_description,
        high_fit_resume=high_fit_resume,
        low_fit_resume=low_fit_resume,
        l_div=l_div,
        h_div=h_div,
    ).to_messages()
    llm = llm
    result = llm(formatted_prompt)
    return result.content


def parse_score_and_explanation(result_content):
    # Assuming the score and explanation are on separate lines
    lines = result_content.split("\n")
    score = float(lines[0])  # Assuming the score is on the first line
    explanation = lines[1] if len(lines) > 1 else ""  # Explanation on the second line
    return score, explanation


def categorize_score(score, threshold1=0.7, threshold2=0.5):
    if score > threshold1:
        return "best"
    elif score > threshold2:
        return "maybe"
    else:
        return "low"


def parse_resume_bytes(resume_bytes):
    resume_file_buffer = io.BytesIO(resume_bytes)
    resume_text = ingest_pdf(resume_file_buffer)
    return resume_text


def process_resumes(uploaded_resumes):
    # Get the values for job_description, high_fit_resume, and low_fit_resume
    job_description, high_fit_resume, low_fit_resume = get_parameters()

    zip_buffer = io.BytesIO()
    try:
        with ZipFile(zip_buffer, "a") as main_zip:
            for i, resume_file in enumerate(uploaded_resumes):
                # Check if the stop button was clicked
                if st.session_state.stop_button_clicked:
                    st.session_state.status_text = "Process stopped by user."
                    break

                # Update status text with current step
                st.session_state.status_text = (
                    f"Processing resume {i + 1}/{len(uploaded_resumes)}..."
                )

                # Read resume bytes
                resume_bytes = resume_file.getbuffer()
                resume_text = parse_resume_bytes(resume_bytes)
                result_content = get_score(
                    resume_text, job_description, high_fit_resume, low_fit_resume
                )
                score, _ = parse_score_and_explanation(result_content)
                category = categorize_score(score)

                # Assuming the applicant's name is part of the filename; adapt as needed
                applicant_name = os.path.splitext(resume_file.name)[0]

                save_to_category_buffer(
                    category, applicant_name, resume_bytes, result_content, main_zip
                )

                st.session_state.progress = (i + 1) / len(uploaded_resumes)
                progress_bar.progress(int(st.session_state.progress * 100))

        return zip_buffer.getvalue()

    except Exception as e:
        st.error(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")


# Streamlit interface

PAGE_TITLE = "RecruitPilot"
PAGE_ICON = "🧐"
SUB_TITLE = "Resume Scoring Tool"
LAYOUT = "centered"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)
st.markdown(
    f"<h1 style='text-align: center;'>{PAGE_TITLE} {PAGE_ICON} <br> {SUB_TITLE} <br></h1>",
    unsafe_allow_html=True,
)

with st.form(key="process_form"):
    uploaded_resumes = st.file_uploader(
        "Upload Resumes (PDF files)", type=["pdf"], accept_multiple_files=True
    )
    start_button = st.form_submit_button("Start Scoring")

# Initialize session state variables
if "stop_button_clicked" not in st.session_state:
    st.session_state.stop_button_clicked = False
if "status_text" not in st.session_state:
    st.session_state.status_text = ""
if "progress" not in st.session_state:
    st.session_state.progress = 0
if "processing" not in st.session_state:
    st.session_state.processing = False

status_text = st.empty()
status_text.text(st.session_state.status_text)  # Status text now updates dynamically

if start_button:
    st.session_state.stop_button_clicked = False
    st.session_state.processing = True
    st.session_state.progress = 0


with st.expander("Select custom inputs"):
    job_description_input = st.text_area("Job Description", key="job_description_input")
    high_fit_resume_input = st.text_area(
        "High-Fit Resume Example", key="high_fit_resume_input"
    )
    low_fit_resume_input = st.text_area(
        "Low-Fit Resume Example", key="low_fit_resume_input"
    )

# Display the stop button only when processing is True
if st.session_state.processing:
    # Update progress bar and status text from session state
    progress_bar = st.progress(0)
    progress_bar.progress(int(st.session_state.progress * 100))
    if uploaded_resumes:
        stop_button = st.button("Stop Process")
        if stop_button:
            st.session_state.stop_button_clicked = True
            st.session_state.status_text = "Stopping the process..."
            st.session_state.processing = False

if uploaded_resumes and start_button:
    st.session_state.status_text = "Starting the process..."
    try:
        zip_data = process_resumes(uploaded_resumes)
        if zip_data:
            st.download_button(
                label="✨ Download Scores ✨",
                data=zip_data,
                file_name="scores.zip",
                mime="application/zip",
            )
    except Exception as e:
        st.error(f"An error occurred during processing: {e}")
        logger.error(f"An error occurred during processing: {e}")
    st.session_state.status_text = "Process completed. Download the scores below."
    st.session_state.processing = False
else:
    if start_button:
        st.warning("Please upload resumes before starting the process.")

st.markdown(
    """
    ---
    Built by **Jared Kirby** :wave:

    [Twitter](https://twitter.com/Kirby_) | [GitHub](https://github.com/jaredkirby) | [LinkedIn](https://www.linkedin.com/in/jared-kirby/) | [Portfolio](https://www.jaredkirby.me)

        """
)
