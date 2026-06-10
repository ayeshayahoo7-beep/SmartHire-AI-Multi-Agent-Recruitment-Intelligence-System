from fastapi import FastAPI, UploadFile, File
from utils.pdf_utils import extract_text_from_pdf

app = FastAPI(title="SmartOps ATS API")

# ----------------------------------
# HEALTH CHECK
# ----------------------------------

@app.get("/")
def health():
    return {
        "status": "running",
        "service": "SmartOps ATS Backend"
    }

# ----------------------------------
# CORE ATS ENGINE (SAFE + STABLE)
# ----------------------------------

def analyze_text(text: str):

    text_lower = text.lower()

    # ----------------------------------
    # SIMPLE SKILL ENGINE
    # ----------------------------------

    skill_weights = {
        "python": 25,
        "java": 20,
        "javascript": 15,
        "react": 15,
        "sql": 15,
        "machine learning": 30,
        "ai": 25,
        "flask": 10,
        "fastapi": 15
    }

    skills_found = []
    score = 0

    for skill, weight in skill_weights.items():
        if skill in text_lower:
            skills_found.append(skill)
            score += weight

    score = min(score, 100)

    # ----------------------------------
    # DECISION ENGINE
    # ----------------------------------

    if score >= 75:
        decision = "YES"
    elif score >= 50:
        decision = "MAYBE"
    else:
        decision = "NO"

    # ----------------------------------
    # INTERVIEW QUESTIONS ENGINE
    # ----------------------------------

    base_questions = [
        "Tell me about yourself.",
        "Describe your most challenging project.",
        "How do you debug issues in your code?",
        "Explain a system you built end-to-end.",
    ]

    dynamic_questions = []

    if skills_found:
        dynamic_questions.append(
            f"Explain your experience with {skills_found[0]} in detail."
        )

    if "python" in skills_found:
        dynamic_questions.append(
            "What are Python decorators and where have you used them?"
        )

    if "java" in skills_found:
        dynamic_questions.append(
            "Explain OOP principles in Java with examples."
        )

    questions = base_questions + dynamic_questions

    # ----------------------------------
    # RESPONSE FORMAT (MATCH FRONTEND)
    # ----------------------------------

    return {
        "profile": {
            "skills": skills_found,
            "word_count": len(text.split())
        },
        "questions": questions,
        "decision": {
            "hire": decision,
            "confidence": score
        }
    }

# ----------------------------------
# MAIN ENDPOINT
# ----------------------------------

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    try:
        file_bytes = await file.read()
        text = extract_text_from_pdf(file_bytes)

        if not text:
            return {
                "profile": {"skills": [], "word_count": 0},
                "questions": [],
                "decision": {
                    "hire": "NO",
                    "confidence": 0
                }
            }

        result = analyze_text(text)
        return result

    except Exception as e:
        return {
            "error": str(e),
            "profile": {"skills": [], "word_count": 0},
            "questions": [],
            "decision": {
                "hire": "NO",
                "confidence": 0
            }
        }
