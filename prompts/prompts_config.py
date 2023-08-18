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
