
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile

import pandas as pd
import requests
from ucimlrepo import fetch_ucirepo

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_sms_dataset():
    print("\nDownloading SMS Spam Collection...")

    url = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    with ZipFile(BytesIO(response.content)) as archive:
        with archive.open("SMSSpamCollection") as file:
            df = pd.read_csv(
                file,
                sep="\t",
                header=None,
                names=["label", "message"],
                encoding="utf-8"
            )

    output = RAW_DIR / "sms_spam.csv"
    df.to_csv(output, index=False)

    print(f"Saved: {output}")
    print(f"Rows: {len(df)}")
    print(df["label"].value_counts())


def download_phishing_dataset():
    print("\nDownloading PhiUSIIL Phishing URL dataset...")

    dataset = fetch_ucirepo(id=967)

    df = pd.concat(
        [dataset.data.features, dataset.data.targets],
        axis=1
    )

    output = RAW_DIR / "phishing_urls.csv"
    df.to_csv(output, index=False)

    print(f"Saved: {output}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")


if __name__ == "__main__":
    download_sms_dataset()
    download_phishing_dataset()

    print("\nDataset downloading completed!")
