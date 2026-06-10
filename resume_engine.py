import re

# ----------------------------------
# SKILL DATABASE (EASILY EXTENDABLE)
# ----------------------------------

SKILL_DB = {
    "python": 25,
    "java": 20,
    "javascript": 15,
    "react": 15,
    "node": 15,
    "sql": 15,
    "fastapi": 20,
    "flask": 10,
    "machine learning": 30,
    "ai": 25,
    "deep learning": 30,
    "docker": 20,
    "git": 10
}

# ----------------------------------
# TEXT CLEANING
# ----------------------------------

def clean_text(text: str) -> str:
    if not text:
        return ""
    return text.lower()

# ----------------------------------
# SKILL EXTRACTION ENGINE
# ----------------------------------

def extract_skills(text: str):
    text = clean_text(text)

    found_skills = []

    for skill in SKILL_DB.keys():
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills

# ----------------------------------
# SCORING ENGINE
# ----------------------------------

def calculate_score(skills):
    score = 0

    for skill in skills:
        score += SKILL_DB.get(skill, 0)

    return min(score, 100)

# ----------------------------------
# DECISION ENGINE (ATS LOGIC)
# ----------------------------------

def make_decision(score):
    if score >= 75:
        return "YES"
    elif score >= 50:
        return "MAYBE"
    else:
        return "NO"

# ----------------------------------
# INTERVIEW ENGINE
# ----------------------------------

def generate_questions(skills):

    base_questions = [
        "Tell me about yourself.",
        "Describe a challenging project you worked on.",
        "How do you handle debugging in production issues?",
        "Explain a system you designed end-to-end."
    ]

    dynamic_questions = []

    if "python" in skills:
        dynamic_questions.append(
            "Explain Python memory management and garbage collection."
        )

    if "java" in skills:
        dynamic_questions.append(
            "Explain OOP principles and how Java implements them."
        )

    if "machine learning" in skills:
        dynamic_questions.append(
            "Explain the difference between supervised and unsupervised learning."
        )

    if "docker" in skills:
        dynamic_questions.append(
            "How do you containerize an application using Docker?"
        )

    return base_questions + dynamic_questions

# ----------------------------------
# MAIN ENGINE FUNCTION (USED BY API)
# ----------------------------------

def analyze_resume(text: str):

    skills = extract_skills(text)
    score = calculate_score(skills)
    decision = make_decision(score)
    questions = generate_questions(skills)

    return {
        "profile": {
            "skills": skills,
            "word_count": len(text.split())
        },
        "questions": questions,
        "decision": {
            "hire": decision,
            "confidence": score
        }
    }
