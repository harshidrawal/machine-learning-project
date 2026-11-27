
from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/raw/phishing_urls.csv")
OUTPUT_FILE = Path("data/processed/urls_clean.csv")


def main():
    df = pd.read_csv(INPUT_FILE)

    df = df[["URL", "label"]].copy()
    df = df.dropna(subset=["URL", "label"])

    df["URL"] = df["URL"].astype(str).str.strip()
    df = df[df["URL"] != ""]
    df = df.drop_duplicates(subset=["URL"])

    # PhiUSIIL: 1 = legitimate, 0 = phishing
    # ScamShield: 1 = scam, 0 = safe
    df["label"] = df["label"].map({1: 0, 0: 1})

    df = df.dropna(subset=["label"])
    df["label"] = df["label"].astype(int)

    # Balance the dataset
    df = (
        df.groupby("label", group_keys=False)
        .apply(
            lambda group: group.sample(
                n=min(len(group), 10000),
                random_state=42
            )
        )
        .reset_index(drop=True)
    )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("URL preprocessing completed!")
    print("Total URLs:", len(df))
    print(df["label"].value_counts())
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
