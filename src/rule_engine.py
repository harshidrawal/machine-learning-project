
import re

SCAM_RULES = {
    "urgency": [
        r"\b(urgent|immediately|act now|hurry|expires today)\b",
        r"\b(verify now|within 24 hours|final warning)\b"
    ],
    "account_threat": [
        r"\b(account|bank|card)\b.{0,40}\b(blocked|suspended|frozen|closed)\b",
        r"\b(kyc|re-?kyc)\b.{0,40}\b(expired|update|verify)\b"
    ],
    "credential_request": [
        r"\b(otp|pin|password|cvv)\b",
        r"\b(share|send|provide|enter)\b.{0,30}\b(otp|pin|password|cvv)\b"
    ],
    "reward_bait": [
        r"\b(lottery|winner|prize|reward|cashback|free gift)\b",
        r"\b(claim your|you have won|congratulations)\b"
    ],
    "payment_request": [
        r"\b(send money|pay now|transfer money|processing fee)\b",
        r"\b(refund|cash prize)\b.{0,40}\b(fee|payment|upi)\b"
    ]
}


def analyze_message(message):
    message = str(message).lower()

    detected_rules = []
    flags = []

    for rule_name, patterns in SCAM_RULES.items():
        for pattern in patterns:
            if re.search(pattern, message):
                detected_rules.append(rule_name)
                flags.append(
                    f"Suspicious pattern: {rule_name.replace('_', ' ')}"
                )
                break

    score = min(len(detected_rules) * 20, 100)

    return {
        "risk_score": score,
        "detected_rules": detected_rules,
        "flags": flags
    }


if __name__ == "__main__":
    test_message = (
        "URGENT! Your bank account will be blocked. "
        "Share your OTP immediately to claim your reward."
    )

    print("Message:", test_message)
    print("Analysis:", analyze_message(test_message))
