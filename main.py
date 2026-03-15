import time

from injection_detector import detect_injection
from presidio_filter import detect_and_anonymize
from policy_engine import decide_policy
from ollama_client import query_llm


def main():
    prompt = input("Enter your prompt: ")

    # Injection Detection
    start = time.time()
    is_attack, score = detect_injection(prompt)
    injection_time = time.time() - start

    # Presidio Sensitive Data Detection
    start = time.time()
    anonymized_text, entities = detect_and_anonymize(prompt)
    presidio_time = time.time() - start

    # Policy Decision
    decision = decide_policy(is_attack, entities)

    llm_time = 0
    response = ""

    print("\nSecurity Analysis")
    print("-----------------------------")
    print("Injection Score:", score)
    print("Policy Decision:", decision)

    # Handle decision
    if decision == "BLOCK":
        print("\nRequest blocked due to security risk.")

    elif decision == "MASK":
        print("\nSensitive data detected. Sending masked prompt to LLM...")

        start = time.time()
        response = query_llm(anonymized_text)
        llm_time = time.time() - start

    else:
        print("\nPrompt allowed. Sending to LLM...")

        start = time.time()
        response = query_llm(prompt)
        llm_time = time.time() - start

    # Latency Measurements
    print("\nLatency Measurements")
    print("-----------------------------")
    print(f"Injection Detection Time: {injection_time:.4f} seconds")
    print(f"Presidio Analysis Time: {presidio_time:.4f} seconds")
    print(f"LLM Response Time: {llm_time:.4f} seconds")

    # LLM Response
    if response:
        print("\nLLM Response")
        print("-----------------------------")
        print(response)


if __name__ == "__main__":
    main()