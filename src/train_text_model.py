
from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

DATA_FILE = Path("data/processed/sms_clean.csv")
MODEL_FILE = Path("models/logistic_regression.pkl")


def main():
    df = pd.read_csv(DATA_FILE)

    X = df["message_clean"].astype(str)
    y = df["label_binary"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=42,
        stratify=y
    )

    features = FeatureUnion([
        (
            "word_tfidf",
            TfidfVectorizer(
                analyzer="word",
                ngram_range=(1, 2),
                max_features=30000,
                sublinear_tf=True
            )
        ),
        (
            "char_tfidf",
            TfidfVectorizer(
                analyzer="char",
                ngram_range=(2, 5),
                max_features=30000,
                sublinear_tf=True
            )
        )
    ])

    model = Pipeline([
        ("features", features),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42
            )
        )
    ])

    print("Training TF-IDF + Logistic Regression...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\nMODEL EVALUATION")
    print("-------------------------")
    print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
    print("Precision:", round(
        precision_score(y_test, predictions, zero_division=0), 4
    ))
    print("Recall:", round(
        recall_score(y_test, predictions, zero_division=0), 4
    ))
    print("F1 Score:", round(
        f1_score(y_test, predictions, zero_division=0), 4
    ))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        predictions,
        target_names=["Safe", "Scam"],
        zero_division=0
    ))

    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_FILE)

    print("\nModel saved to:", MODEL_FILE)


if __name__ == "__main__":
    main()
