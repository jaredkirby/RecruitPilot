import os
import logging
import tempfile
import streamlit as st

from langchain.callbacks.base import BaseCallbackHandler
from langchain.document_loaders import PDFPlumberLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

from prompts.prompts_config import PROMPTS_MAPPING
from config.interview_questions_config import (
    MODEL,
    SUB_TITLE,
    INSTRUCTIONS,
)
from config.site_config import (
    LAYOUT,
    PAGE_TITLE,
    PAGE_ICON,
    #FOOTER,
)

openai_api_key = st.secrets["OPENAI_API_KEY"]

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


def create_chat(stream_handler):
    try:
        _chat = ChatOpenAI(
            temperature=0.0,
            model=MODEL,
            openai_api_key=openai_api_key,
            request_timeout=250,
            streaming=True,
            callbacks=[stream_handler],
        )
    except Exception as e:
        st.error(f"An error occurred while creating the chat session: {str(e)}")
        _chat = None
    return _chat


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


def get_parameters(selected_job, job_description_input):
    if selected_job == "Input your own":
        job_description = job_description_input
    else:
        selected_prompts = PROMPTS_MAPPING[selected_job]
        job_description = (
            job_description_input
            if job_description_input
            else selected_prompts["job_description"]
        )
    return job_description


# TODO: Switch to OpenAI function LLM call for more reliable response formatting
# not an issue for now
@st.cache_data
def Analyzing_Resume(
    _chat,
    resume_text,
    job_description,
):
    print("Getting score...")

    template = f"""\
You are an Industrial/Organizational Psychologist who is preparing to analyze an 
applicant based on a job description and resume, 
and create a selection of interview questions specific to the applicant in order to 
determine their potential success in the role.

Applicant Resume:
-----------------
{resume_text}
-----------------

Job Key Areas of Responsibility:
-----------------
{job_description}
-----------------

Based on the job description and the information provided in the resume, please 
respond with an analysis of this applicant and a 
selection of interview questions specific to this applicant and designed to understand 
better if this person will succeed in this role.

Your Response Format:
Applicant Name

Position Name

List of positive attributes for the position

List of negative attributes for the position

List of questions for the interview
    """

    user_prompt = HumanMessagePromptTemplate.from_template(template=template)
    chat_prompt = ChatPromptTemplate.from_messages([user_prompt])
    formatted_prompt = chat_prompt.format_prompt(
        resume_text=resume_text,
        job_description=job_description,
    ).to_messages()
    # print(formatted_prompt)
    llm = _chat
    result = llm(formatted_prompt)
    return result.content


# Streamlit interface
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

st.markdown(
    f"<h1 style='text-align: center;'>{PAGE_TITLE} {PAGE_ICON} <br> {SUB_TITLE}</h1>",
    unsafe_allow_html=True,
)

st.divider()


selected_job = st.selectbox(
    "Select an open position or add your own",
    (
        "CEMM - Senior CPG Account Strategist",
        "CEMM - Advertising Assistant",
        "Input your own",
    ),
    index=0,
    key="job_selection",
)

# Initialize the variables outside the conditional block
job_description_file = None

if selected_job == "Input your own":
    with st.expander("Custom Job", expanded=True):
        st.text_area(
            "Job Description Text",
            placeholder="""Summary of Position:
This in-house position is crucial for supporting our client's ...
            """,
            key="job_description_input",
        )
        job_description_file = st.file_uploader("Or upload a PDF", type=["pdf"])

uploaded_resumes = st.file_uploader(
    "Upload Resumes (PDF files)", type=["pdf"], accept_multiple_files=True
)

start_button = st.button("Generate Questions")

if uploaded_resumes and start_button:
    try:
        for uploaded_resume in uploaded_resumes:
            resume_text = ingest_pdf(uploaded_resume)
            chat = create_chat(StreamHandler(st.empty()))
            result = Analyzing_Resume(chat, resume_text, selected_job)
    except Exception as e:
        st.error(f"An error occurred during processing: {e}")
        logger.error(f"An error occurred during processing: {e}")
else:
    if start_button:
        st.warning("Please upload resumes before starting the process.")

with st.expander("🤔 How to Use"):
    st.info(INSTRUCTIONS)

# st.markdown(FOOTER)
