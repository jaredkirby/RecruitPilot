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
LAYOUT = "centered"
FOOTER = """
    ---
    Built by **Jared Kirby** :wave:

    [Twitter](https://twitter.com/Kirby_) | [GitHub](https://github.com/jaredkirby) | [LinkedIn](https://www.linkedin.com/in/jared-kirby/) | [Portfolio](https://www.jaredkirby.me)

        """

# LLM
MODEL = "gpt-3.5-turbo-16k"
MODEL_QUESTIONS = "gpt-4"

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
