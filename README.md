# Task-4-APT3020B
AI-Based Resume Screening System, used to filter job applicants based on predefined criteria.

Research & Rule Identification
1. Research: What Recruiters Look For

Recruiters typically evaluate job applicants using several key criteria to determine whether a candidate is suitable for a particular role. These criteria help organizations efficiently filter large numbers of resumes and identify candidates who meet the required qualifications.

For this project, the AI-based resume screening system will be designed using common recruitment criteria that many recruiters consider during the initial screening stage. The system will therefore apply rules based on factors such as technical skills, educational background, GPA, work experience, certifications, and project experience.

2. Technical Skills

Technical skills are one of the primary factors that recruiters use when evaluating candidates. These skills indicate whether the applicant has the necessary technical abilities required for the role.

Examples include:

Python

Java

SQL

React

Machine Learning

3. Education Background

Recruiters also consider the candidate’s field of study to ensure it aligns with the job requirements.

Examples include:

Computer Science

Information Technology

Software Engineering

Data Science

4. GPA

Some organizations use GPA as an indicator of academic performance and commitment. A commonly used threshold is a minimum GPA of 3.0.


5. Work Experience

Work experience helps recruiters determine whether the candidate has practical exposure to real-world work environments. This may include internships, previous employment, or freelance projects.


6. Certifications

Professional certifications demonstrate specialized knowledge and additional training in specific technologies or platforms.

Examples include:

AWS Certification

Google Cloud Certification

Cisco Certification


7. Projects

Projects provide evidence of a candidate’s ability to apply theoretical knowledge to real-world problems. These may include software development projects, GitHub repositories, or academic capstone projects.

Based on these commonly used recruitment criteria, the system will apply a set of rule-based conditions to automatically evaluate and shortlist candidates.


8. Rule Identification (Knowledge Representation)

Based on the identified recruiter criteria, a set of selection rules can be defined to automatically filter candidates.

These rules will form the knowledge base of the AI screening system.

Rule 1: Skill Requirement
IF candidate has skill "Python"
THEN candidate meets technical skill requirement
Rule 2: Experience Requirement
IF experience_years >= 2
THEN candidate meets experience requirement
Rule 3: Academic Requirement
IF GPA >= 3.0
THEN candidate meets academic requirement
Rule 4: Certification Advantage
IF certification = AWS OR Google Cloud
THEN candidate receives higher ranking
Rule 5: Final Shortlisting Rule
IF skill requirement is satisfied
AND experience >= 2 years
AND GPA >= 3.0
THEN candidate is shortlisted
ELSE candidate is rejected

These rules allow the system to automatically evaluate resumes and shortlist suitable candidates.
