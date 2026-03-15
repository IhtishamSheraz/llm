
import streamlit as st
import time

from injection_detector import detect_injection
from presidio_filter import detect_and_anonymize
from policy_engine import decide_policy
from ollama_client import query_llm

st.title("🔒 LLM Security Gateway")
st.write("Secure interface for interacting with a local LLM.")

prompt = st.text_area("Enter your prompt:")

if st.button("Submit") and prompt:

    # -------------------------
    # Injection Detection
    # -------------------------
    start = time.time()
    is_attack, score = detect_injection(prompt)
    injection_time = time.time() - start

    # -------------------------
    # Presidio Detection
    # -------------------------
    start = time.time()
    anonymized_text, entities = detect_and_anonymize(prompt)
    presidio_time = time.time() - start

    # -------------------------
    # Policy Decision
    # -------------------------
    decision = decide_policy(is_attack, entities)

    st.subheader("Security Analysis")
    st.write("Injection Score:", score)
    st.write("Policy Decision:", decision)

    llm_time = 0
    response = ""

    if decision == "BLOCK":

        st.error("Request blocked due to security risk.")

    elif decision == "MASK":

        st.warning("Sensitive data detected. Prompt masked.")
        st.write("Filtered Prompt:", anonymized_text)

        start = time.time()
        response = query_llm(anonymized_text)
        llm_time = time.time() - start

    else:

        st.success("Prompt allowed. Sending to LLM...")

        start = time.time()
        response = query_llm(prompt)
        llm_time = time.time() - start

    # -------------------------
    # Latency Display
    # -------------------------
    st.subheader("Latency Measurements")

    st.write(f"Injection Detection Time: {injection_time:.4f} seconds")
    st.write(f"Presidio Analysis Time: {presidio_time:.4f} seconds")
    st.write(f"LLM Response Time: {llm_time:.4f} seconds")

    # -------------------------
    # LLM Output
    # -------------------------
    if response:
        st.subheader("LLM Response")
        st.write(response)

