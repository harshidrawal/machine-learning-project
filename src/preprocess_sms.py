
import re
from pathlib import Path

import pandas as pd

INPUT_FILE = Path("data/raw/sms_spam.csv")
OUTPUT_FILE = Path("data/processed/sms_clean.csv")


def clean_message(message):
    message = str(message).lower()

    # Replace URLs with a common token
    message = re.sub(r"https?://\S+|www\.\S+", " URL ", message)

    # Replace phone numbers
    message = re.sub(r"\b\d{10,13}\b", " PHONE ", message)

    # Replace remaining numbers
    message = re.sub(r"\d+", " NUMBER ", message)

    # Normalize whitespace
    message = re.sub(r"\s+", " ", message).strip()

    return message


def main():
    df = pd.read_csv(INPUT_FILE)

    df = df.dropna(subset=["message", "label"])
    df = df.drop_duplicates(subset=["message"])

    df["message_clean"] = df["message"].apply(clean_message)

    # ham = safe (0), spam = scam (1)
    df["label_binary"] = df["label"].map({
        "ham": 0,
        "spam": 1
    })

    df = df.dropna(subset=["label_binary"])
    df["label_binary"] = df["label_binary"].astype(int)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("SMS preprocessing completed!")
    print("Total records:", len(df))
    print("\nClass distribution:")
    print(df["label_binary"].value_counts())
    print("\nSaved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
