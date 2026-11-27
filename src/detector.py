
import joblib
from pathlib import Path

from src.rule_engine import analyze_message
from src.url_analysis import analyze_url


BASE_DIR = Path(__file__).resolve().parent.parent

TEXT_MODEL_PATH = BASE_DIR / "models" / "logistic_regression.pkl"
URL_MODEL_PATH = BASE_DIR / "models" / "url_model.pkl"

text_model = joblib.load(TEXT_MODEL_PATH)
url_model = joblib.load(URL_MODEL_PATH)


def detect_message(message):
    message = str(message).strip()

    if not message:
        return {"error": "Please enter a message."}

    # 1. SMS machine-learning prediction
    text_probability = text_model.predict_proba([message])[0][1]

    # 2. Rule-based message analysis
    rule_result = analyze_message(message)
    rule_score = rule_result["risk_score"]

    # 3. Extract URLs from the message
    import re

    urls = re.findall(
        r"https?://[^\s]+|www\.[^\s]+",
        message,
        flags=re.IGNORECASE
    )

    url_results = []

    for url in urls:
        cleaned_url = url.rstrip(".,!?;:)")

        url_probability = url_model.predict_proba([cleaned_url])[0][1]
        heuristic_result = analyze_url(cleaned_url)

        url_results.append({
            "url": cleaned_url,
            "ml_risk": round(float(url_probability) * 100, 2),
            "heuristic_risk": heuristic_result["risk_score"],
            "flags": heuristic_result["flags"]
        })

    # 4. Combine the risk scores
    text_score = float(text_probability) * 100

    highest_url_score = max(
        [
            max(item["ml_risk"], item["heuristic_risk"])
            for item in url_results
        ],
        default=0
    )

    final_score = max(
        text_score,
        rule_score,
        highest_url_score
    )

    final_score = round(min(final_score, 100), 2)

    if final_score >= 70:
        risk_level = "HIGH"
    elif final_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "message": message,
        "risk_score": final_score,
        "risk_level": risk_level,
        "text_ml_score": round(text_score, 2),
        "rule_score": rule_score,
        "urls_detected": url_results,
        "detected_rules": rule_result["detected_rules"],
        "flags": rule_result["flags"]
    }
