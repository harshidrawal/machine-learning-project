ScamShield India

An Explainable Machine Learning System for Scam Message and Phishing URL Detection

ScamShield India is a machine-learning-based security prototype designed to identify suspicious SMS/WhatsApp messages and phishing URLs. It combines text classification, URL classification, and rule-based analysis to generate a risk score, identify suspicious patterns, and provide safety recommendations.

The system is developed using Python, Scikit-learn, TF-IDF, Logistic Regression, and Streamlit.

1. Project Objectives

Detect scam and spam messages using machine learning.

Identify potentially malicious and phishing URLs.

Analyze suspicious patterns such as urgency, account threats, credential requests, and reward-based fraud.

Generate an explainable risk score and risk category.

Provide an interactive web interface for message analysis.

2. System Architecture

The project follows this processing pipeline:

Input: User enters an SMS or WhatsApp message.

Text analysis: A trained text classification model evaluates the message.

Rule-based analysis: Suspicious language patterns are identified.

URL extraction: URLs are extracted from the submitted message.

URL analysis: The URL classification model and heuristic analyzer evaluate extracted links.

Risk aggregation: The highest component risk score is used to calculate the final risk score.

Output: The application displays the risk score, risk category, detected indicators, and safety recommendations.

3. Datasets

The project uses two publicly available datasets.

Dataset

Source

Purpose

SMS Spam Collection

UCI Repository

SMS spam/scam classification

PhiUSIIL Phishing URL Dataset

UCI Repository

Phishing URL classification

Dataset preparation

SMS Spam Collection

Original records: 5,572

Cleaned records: 5,169

Safe messages: 4,516

Scam/spam messages: 653

PhiUSIIL Phishing URL Dataset

Original records: 235,795

Sampled and cleaned records: 20,000

Safe URLs: 10,000

Phishing URLs: 10,000

Preprocessing

Removal of missing and duplicate records.

Text normalization and label mapping.

URL extraction and normalization.

Sampling of URL records using random_state=42.

Stratified training and testing splits.

Dataset distribution policy: Dataset CSV files are excluded from the final Git repository. They are publicly available from the UCI Machine Learning Repository and can be downloaded using the project's dataset download script.

4. Machine Learning Methodology

SMS Classification

Feature extraction: Word-level and character-level TF-IDF.

Word n-grams: (1, 2).

Character n-grams: (2, 5).

Maximum features: 30,000 for each TF-IDF representation.

Classifier: Logistic Regression.

Class balancing: Enabled.

Phishing URL Classification

Feature extraction: Character-level TF-IDF.

Character n-grams: (3, 5).

Maximum features: 50,000.

Classifier: Logistic Regression.

Class balancing: Enabled.

Rule-Based Detection

The rule engine checks for suspicious indicators, including:

Urgency and pressure tactics.

Account threats.

Credential requests.

Reward and lottery bait.

Suspicious payment requests.

URL Heuristic Analysis

The URL analyzer checks characteristics such as:

Excessive URL length.

Unusual numbers of subdomains.

IP-address-based hosts.

URL shorteners.

Suspicious top-level domains.

Special characters and encoding.

Hyphenated domain names.

The final risk score is derived from the maximum of the text model score, rule-based score, and URL risk score.

Note: The risk score is a prototype detection score, not a calibrated probability of fraud.

5. Model Evaluation

The following results were obtained using a stratified 70:30 train-test split with random_state=42.

SMS Classification

Metric

Result

Accuracy

98.45%

Scam Precision

93.88%

Scam Recall

93.88%

Scam F1-score

93.88%

URL Classification

Metric

Result

Accuracy

99.10%

Scam Precision

100.00%

Scam Recall

98.20%

Scam F1-score

99.09%

Evaluation disclaimer: These are preliminary results from single random train-test splits. They should not be interpreted as guaranteed real-world detection performance. Further validation, duplicate/leakage checks, independent testing, and India-specific scam datasets are required.

6. Technology Stack

Category

Technology

Programming language

Python 3.10

Data processing

Pandas, NumPy

Machine learning

Scikit-learn

Feature extraction

TF-IDF

Classification

Logistic Regression

Model serialization

Joblib / Pickle

URL analysis

Python Regex, URL parsing

Web interface

Streamlit

Version control

Git and GitHub

7. Repository Structure

ScamShield_India/
│
├── app/
│   ├── app.py
│   └── ppt
│
├── data/
│   ├── raw/                 # Downloaded datasets (not tracked)
│   └── processed/           # Processed datasets (not tracked)
│
├── models/
│   ├── logistic_regression.pkl
│   └── url_model.pkl
│
├── src/
│   ├── download_datasets.py
│   ├── preprocess_sms.py
│   ├── preprocess_urls.py
│   ├── train_text_model.py
│   ├── train_url_model.py
│   ├── rule_engine.py
│   ├── url_analysis.py
│   └── detector.py
│
├── .gitignore
├── requirements.txt
└── README.md

8. Environment Requirements

macOS, Linux, or Windows.

Python 3.10 or compatible version.

pip package manager.

Git.

Internet connection for dataset downloads and package installation.

Installation

Clone the repository:

git clone https://github.com/harshidrawal/machine-learning-project.git

Navigate to the project directory:

cd machine-learning-project

Create a virtual environment:

python3 -m venv .venv

Activate the environment on macOS/Linux:

source .venv/bin/activate

On Windows:

.venv\Scripts\activate

Install the required dependencies:

python -m pip install -r requirements.txt

9. Reproducing the Project

Follow these steps to reproduce the machine learning pipeline.

Step 1: Download datasets

python src/download_datasets.py

This downloads the source datasets into the project's data directory.

Step 2: Preprocess SMS data

python src/preprocess_sms.py

Step 3: Preprocess URL data

python src/preprocess_urls.py

Step 4: Train the SMS classification model

python src/train_text_model.py

Expected output checkpoint:

models/logistic_regression.pkl

Step 5: Train the phishing URL classification model

python src/train_url_model.py

Expected output checkpoint:

models/url_model.pkl

Step 6: Launch the application

streamlit run app/app.py

Open the URL displayed in the terminal, usually:

http://localhost:8501

Reproduction note: The repository includes the trained model checkpoints, so the application can be run directly after installing dependencies without retraining, provided the checkpoints are present. To reproduce training, execute the dataset preparation and training steps in order.

10. Reproducibility Artifacts

The following artifacts are provided:

Artifact

Purpose

requirements.txt

Python dependency specification

src/download_datasets.py

Dataset acquisition

src/preprocess_sms.py

SMS preprocessing

src/preprocess_urls.py

URL preprocessing

src/train_text_model.py

SMS model training

src/train_url_model.py

URL model training

models/logistic_regression.pkl

Trained SMS classifier

models/url_model.pkl

Trained URL classifier

src/detector.py

Integrated detection pipeline

app/app.py

Streamlit interface

Random-state configuration is set to 42 in the training and URL sampling workflows to support reproducible experiments.

Declaration of Reproducibility

I declare that ScamShield India is developed using documented Python source code, publicly accessible datasets, and specified machine-learning methods. The repository provides the implementation, environment dependency file, dataset acquisition and preprocessing scripts, training scripts, and serialized model checkpoints required to reproduce the prototype.

The reported evaluation results correspond to the specified experimental train-test splits. Exact reproducibility may depend on the Python and library versions, source dataset versions, and execution environment. The project is an academic research prototype and has not yet undergone comprehensive independent real-world validation.

11. Model Checkpoints

The trained model files are included in the repository:

Checkpoint

Description

models/logistic_regression.pkl

Trained SMS text classifier

models/url_model.pkl

Trained phishing URL classifier

These serialized checkpoints are retained in Git because they are required for direct application execution and are small enough for the current repository upload.

If the checkpoints are regenerated, the training scripts can recreate them from the processed datasets.

12. Git Commit Information

The initial repository commit is:

Commit

Hash

Description

Timestamp

Initial commit

7266c62

Initial commit: ScamShield India ML project

See exact Git timestamp below

Retrieve the complete commit hash and timestamp using:

git show -s --format=fuller 7266c62

To inspect the complete repository history:

git log --format="%H | %an | %aI | %s"

The Git history is maintained in the repository and can be inspected using these commands.

13. Limitations and Future Work

Expand the dataset with India-specific scam messages and Hinglish content.

Evaluate performance on independent datasets.

Investigate duplicate records and possible data leakage.

Improve risk-score calibration and decision thresholds.

Explore transformer-based NLP models such as DistilBERT.

Improve explainability and URL reputation analysis.

Perform extensive real-world testing before deployment.

