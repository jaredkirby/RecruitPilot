from prompts.cpg_strategic import (
    CPG_STRATEGIC_JOB_DESCRIPTION,
    CPG_STRATEGIC_HIGH_FIT_RESUME,
    CPG_STRATEGIC_LOW_FIT_RESUME,
)
from prompts.advertising_assistant import (
    ADVERTISING_ASSISTANT_JOB_DESCRIPTION,
    ADVERTISING_ASSISTANT_HIGH_FIT_RESUME,
    ADVERTISING_ASSISTANT_LOW_FIT_RESUME,
)

# Page Config
PAGE_TITLE = "RecruitPilot"
PAGE_ICON = "🎯"
SUB_TITLE = "Resume Scoring Tool"
DESCRIPTION = "This tool uses AI to score (with an explanation) and categorize resumes based on a job description. Then provides a downloadable folder with the original resumes in their respective categories."
LAYOUT = "centered"

# LLM & Category Config
MODEL = "gpt-3.5-turbo-16k"

# Prompt Config
PROMPTS_MAPPING = {
    "CEMM - Senior CPG Account Strategist": {
        "folder": "cpg_strategic",
        "job_description": CPG_STRATEGIC_JOB_DESCRIPTION,
        "high_fit_resume": CPG_STRATEGIC_HIGH_FIT_RESUME,
        "low_fit_resume": CPG_STRATEGIC_LOW_FIT_RESUME,
    },
    "CEMM - Advertising Assistant": {
        "folder": "advertising_assistant",
        "job_description": ADVERTISING_ASSISTANT_JOB_DESCRIPTION,
        "high_fit_resume": ADVERTISING_ASSISTANT_HIGH_FIT_RESUME,
        "low_fit_resume": ADVERTISING_ASSISTANT_LOW_FIT_RESUME,
    },
}
