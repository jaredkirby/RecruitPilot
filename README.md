# README

## Resume Scoring and Interview Questions Generator

This repository contains two Python scripts, `📈_Resume_Scoring.py` and `🤨_Interview_Questions.py`, that leverage OpenAI's GPT-3 model to automate the process of resume scoring and generating interview questions based on a job description and a candidate's resume.

### 📈 Resume Scoring

The `📈_Resume_Scoring.py` script is a Streamlit application that allows users to upload multiple resumes (in PDF or Word format) and score them based on a job description. The script uses OpenAI's GPT-3.5-Turbo-16k model to analyze each resume and assign a score between 0 and 1, indicating how well the candidate's skills and experiences match the job description. The resumes are then categorized into 'best', 'better', 'good', and 'rest' based on the score thresholds set by the user.

### 🤨 Interview Questions Generator

The `🤨_Interview_Questions.py` script is another Streamlit application that generates a set of interview questions specific to an applicant based on their resume and a job description. The script uses OpenAI's GPT-4 model to analyze the resume and job description, and then generates a list of positive and negative attributes and interview questions designed to understand better if the person will succeed in the role.

### Installation

1. Clone this repository.
2. Install the required Python packages using pip:
```
streamlit run <script_name>.py
```

### Usage

1. Run the Streamlit application:
```
streamlit run <script_name>.py
```
2. Open the provided URL in your web browser.
3. Follow the instructions in the application to upload resumes and/or job descriptions, and start the process.

### Note

These scripts require an OpenAI API key to function. Please make sure to provide your OpenAI API key in the `st.secrets["OPENAI_API_KEY"]` variable in both scripts.

### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### License

[MIT](https://choosealicense.com/licenses/mit/)