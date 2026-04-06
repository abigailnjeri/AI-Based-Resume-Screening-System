from flask import Flask, render_template, request, jsonify, g
from resume_parser import read_pdf, read_docx, clean_text
from matcher import calculate_match

import sqlite3
import csv
import os

app = Flask(__name__)
DB_PATH = "resume_screener.db"

# 
#  KNOWLEDGE BASE: Selection Rules
# 
REQUIRED_SKILLS = {"python", "java", "sql", "react", "machine learning", "javascript"}
REQUIRED_DEGREES = {"computer science", "information technology",
                    "software engineering", "data science"}
MIN_GPA = 3.0
MIN_EXPERIENCE = 2
PREFERRED_CERTS = {"aws", "google cloud"}


def apply_rules(candidate: dict) -> dict:
    skills_raw = (candidate.get("skills") or "").lower()
    degree_raw = (candidate.get("degree") or "").lower()
    cert_raw   = (candidate.get("certification") or "").lower()
    gpa        = float(candidate.get("gpa") or 0)
    exp        = int(candidate.get("experience_years") or 0)

    has_skill = any(s in skills_raw for s in REQUIRED_SKILLS)
    has_experience = exp >= MIN_EXPERIENCE
    has_gpa = gpa >= MIN_GPA
    has_cert_advantage = any(c in cert_raw for c in PREFERRED_CERTS)
    has_relevant_degree = any(d in degree_raw for d in REQUIRED_DEGREES)

    shortlisted = has_skill and has_experience and has_gpa

    score = 0
    if has_skill:        score += 30
    if has_experience:   score += 25
    if has_gpa:          score += 25
    if has_cert_advantage: score += 15
    if has_relevant_degree: score += 5

    reasons = []
    if not has_skill:       reasons.append("Missing required technical skill")
    if not has_experience:  reasons.append(f"Experience < {MIN_EXPERIENCE} years")
    if not has_gpa:         reasons.append(f"GPA < {MIN_GPA}")

    return {
        "shortlisted":        shortlisted,
        "score":              score,
        "rule1_skill":        has_skill,
        "rule2_experience":   has_experience,
        "rule3_gpa":          has_gpa,
        "rule4_cert":         has_cert_advantage,
        "rejection_reasons":  "; ".join(reasons) if reasons else ""
    }


# 
#  DATABASE SETUP
# 
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id     TEXT,
            degree           TEXT,
            gpa              REAL,
            skills           TEXT,
            experience_years INTEGER,
            certification    TEXT,
            projects         INTEGER,
            soft_skill       TEXT,
            location         TEXT,
            shortlisted      INTEGER,
            score            INTEGER,
            rule1_skill      INTEGER,
            rule2_experience INTEGER,
            rule3_gpa        INTEGER,
            rule4_cert       INTEGER,
            rejection_reasons TEXT
        )
    """)
    db.commit()
    db.close()


def load_csv(path: str):
    db = sqlite3.connect(DB_PATH)
    db.execute("DELETE FROM candidates")

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []

        for row in reader:
            result = apply_rules(row)

            rows.append((
                row.get("candidate_id"),
                row.get("degree"),
                row.get("gpa"),
                row.get("skills"),
                row.get("experience_years"),
                row.get("certification"),
                row.get("projects"),
                row.get("soft_skill"),
                row.get("location"),
                1 if result["shortlisted"] else 0,
                result["score"],
                1 if result["rule1_skill"]      else 0,
                1 if result["rule2_experience"] else 0,
                1 if result["rule3_gpa"]        else 0,
                1 if result["rule4_cert"]       else 0,
                result["rejection_reasons"]
            ))

    db.executemany("""
        INSERT INTO candidates
            (candidate_id, degree, gpa, skills, experience_years,
             certification, projects, soft_skill, location,
             shortlisted, score, rule1_skill, rule2_experience,
             rule3_gpa, rule4_cert, rejection_reasons)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, rows)

    db.commit()
    db.close()
    return len(rows)


# 
#  ROUTES
# 
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stats")
def stats():
    db = get_db()
    total       = db.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]
    shortlisted = db.execute("SELECT COUNT(*) FROM candidates WHERE shortlisted=1").fetchone()[0]
    rejected    = total - shortlisted
    avg_score   = db.execute("SELECT ROUND(AVG(score),1) FROM candidates").fetchone()[0] or 0

    top_skills  = db.execute("""
        SELECT skills, COUNT(*) as cnt FROM candidates
        GROUP BY skills ORDER BY cnt DESC LIMIT 6
    """).fetchall()

    by_degree   = db.execute("""
        SELECT degree, COUNT(*) as total,
               SUM(shortlisted) as passed
        FROM candidates GROUP BY degree
    """).fetchall()

    return jsonify({
        "total":        total,
        "shortlisted":  shortlisted,
        "rejected":     rejected,
        "avg_score":    avg_score,
        "top_skills":   [dict(r) for r in top_skills],
        "by_degree":    [dict(r) for r in by_degree],
    })


@app.route("/api/screen", methods=["POST"])
def screen_single():
    """Screen a single candidate submitted via the manual form."""
    data = request.get_json()

    # ✅ NEW: Name validation (TASK 1)
    name = data.get("name")

    if not name or str(name).strip() == "":
        return jsonify({
            "error": "Name is required for screening"
        }), 400

    result = apply_rules(data)

    return jsonify({**data, **result})


@app.route("/api/filters")
def filters():
    db      = get_db()

    skills  = db.execute("SELECT DISTINCT skills FROM candidates ORDER BY skills").fetchall()
    degrees = db.execute("SELECT DISTINCT degree FROM candidates ORDER BY degree").fetchall()
    certs   = db.execute("SELECT DISTINCT certification FROM candidates WHERE certification IS NOT NULL ORDER BY certification").fetchall()

    return jsonify({
        "skills":  [r[0] for r in skills],
        "degrees": [r[0] for r in degrees],
        "certs":   [r[0] for r in certs],
    })


# 
#  STARTUP
# 
if __name__ == "__main__":
    init_db()

    csv_file = "Task4_resume_dataset_15000.csv"
    if os.path.exists(csv_file):
        n = load_csv(csv_file)
        print(f"Loaded {n} candidates from {csv_file}")
    else:
        print(f"CSV not found at {csv_file} — place it next to app.py and restart.")
    app.run(debug=True, port=5000)
