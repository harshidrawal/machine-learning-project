
import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.detector import detect_message


st.set_page_config(
    page_title="ScamShield India",
    page_icon="🛡️",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
.title {
    font-size: 42px;
    font-weight: 800;
    color: #123b70;
}
.subtitle {
    color: #52647a;
    font-size: 17px;
}
.stButton > button {
    background-color: #123b70;
    color: white;
    border-radius: 10px;
    height: 45px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# Header
st.markdown(
    '<div class="title">🛡️ ScamShield India</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered scam message and phishing URL detector</div>',
    unsafe_allow_html=True
)

st.divider()

# Main input
st.subheader("Analyze a suspicious message")

message = st.text_area(
    "Paste your SMS or WhatsApp message here:",
    height=160,
    placeholder="Example: URGENT! Your bank account will be blocked. Verify immediately..."
)

if st.button("🔍 Analyze Message", use_container_width=True):

    if not message.strip():
        st.warning("Please enter a message first.")

    else:
        with st.spinner("Analyzing message and checking URLs..."):
            result = detect_message(message)

        if "error" in result:
            st.error(result["error"])

        else:
            st.divider()
            st.subheader("Analysis Results")

            score = result["risk_score"]
            level = result["risk_level"]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Risk Score", f"{score}/100")

            with col2:
                st.metric("Risk Level", level)

            with col3:
                st.metric(
                    "URLs Detected",
                    len(result["urls_detected"])
                )

            if level == "HIGH":
                st.error("⚠️ High-risk message! Do not click suspicious links or share sensitive information.")

            elif level == "MEDIUM":
                st.warning("⚠️ Potentially suspicious message. Verify the sender independently.")

            else:
                st.success("No strong scam indicators detected. Still verify unexpected requests.")

            # Model scores
            st.subheader("Detection Breakdown")

            st.write("SMS model score")
            st.progress(int(result["text_ml_score"]))

            st.write("Rule engine score")
            st.progress(int(result["rule_score"]))

            # Rule explanations
            st.subheader("Detected Suspicious Patterns")

            if result["detected_rules"]:
                for rule in result["detected_rules"]:
                    st.warning(rule.replace("_", " ").title())
            else:
                st.info("No suspicious message patterns detected.")

            # URL analysis
            st.subheader("URL Analysis")

            if result["urls_detected"]:
                for item in result["urls_detected"]:
                    st.markdown(f"**URL:** `{item['url']}`")
                    st.write(f"ML risk: {item['ml_risk']}%")
                    st.write(
                        f"Heuristic risk: {item['heuristic_risk']}/100"
                    )

                    for flag in item["flags"]:
                        st.warning(flag)

            else:
                st.info("No URLs detected in this message.")

            # Safety recommendation
            st.subheader("Safety Recommendation")

            st.info(
                "Never share your OTP, PIN, password, banking credentials, "
                "or personal information through an unverified message. "
                "Contact the organization using its official website or number."
            )

st.divider()

st.caption(
    "ScamShield India | Explainable AI-based scam detection | "
    "Prototype version"
)
