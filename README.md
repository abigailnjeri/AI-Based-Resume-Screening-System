**AI-Based Resume Screening System**

A rule-based resume screening system built with Python, Flask, and SQLite.
Filters job applicants automatically using predefined selection rules based on recruiter criteria.


**Project Structure**

AI_Based_Resume_Screening_System/
- `app.py` - Flask application and screening rules
- `requirements.txt` - Python dependencies  
- `Task4_resume_dataset_15000.csv` - Dataset (15,000 candidates)
- `resume_screener.db` - SQLite database
- `templates/index.html` - Frontend UI
- `.gitignore`
- `README.md`


**Technologies**

- Python 3
- Flask (web framework)
- SQLite (database)
- HTML, CSS, JavaScript (frontend)


**Selection Rules (Knowledge Base)**

| Rule   | Condition                                                   | Effect                  |
| ------ | ----------------------------------------------------------- | ----------------------- |
| Rule 1 | Skill is one of: Python, Java, SQL, React, Machine Learning | Required                |
| Rule 2 | experience_years >= 2                                       | Required                |
| Rule 3 | GPA >= 3.0                                                  | Required                |
| Rule 4 | Certification is AWS or Google Cloud                        | +15 score bonus         |
| Final  | Rule 1 AND Rule 2 AND Rule 3                                | SHORTLISTED or REJECTED |


**How to Run**

*Step 1 — Clone the repository*

git clone https://github.com/your-username/AI-Based-Resume-Screening-System/.git
cd resume-screener-ai

*Step 2 — Create a virtual environment*


python -m venv venv
venv\Scripts\activate


*Step 3 — Install dependencies*


pip install -r requirements.txt


*Step 4 — Run the application*


python app.py


*Step 5 — Open in browser*


**Features**

- Dashboard with live stats and charts from the 15,000-candidate dataset
- Candidate browser with filters by status, skill, degree, and certification
- Manual candidate screening with instant rule-by-rule feedback
- Knowledge base page showing all selection rules in pseudocode
