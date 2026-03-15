from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine


# Initialize analyzer
analyzer = AnalyzerEngine()


# -----------------------------
# Custom Recognizer: API Key
# -----------------------------
api_key_pattern = Pattern(
    name="api_key_pattern",
    regex=r"sk-[A-Za-z0-9]{10,}",
    score=0.8
)

api_key_recognizer = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[api_key_pattern]
)

analyzer.registry.add_recognizer(api_key_recognizer)


# -----------------------------
# Custom Recognizer: Pakistani Phone
# -----------------------------
pak_phone_pattern = Pattern(
    name="pak_phone_pattern",
    regex=r"03[0-9]{9}",
    score=0.85
)

pak_phone_recognizer = PatternRecognizer(
    supported_entity="PAK_PHONE",
    patterns=[pak_phone_pattern]
)

analyzer.registry.add_recognizer(pak_phone_recognizer)


# -----------------------------
# Custom Recognizer: Employee ID
# -----------------------------
employee_id_pattern = Pattern(
    name="employee_id_pattern",
    regex=r"EMP-[0-9]{4}-[0-9]{3}",
    score=0.85
)

employee_id_recognizer = PatternRecognizer(
    supported_entity="EMPLOYEE_ID",
    patterns=[employee_id_pattern]
)

analyzer.registry.add_recognizer(employee_id_recognizer)


# Initialize anonymizer
anonymizer = AnonymizerEngine()


def detect_and_anonymize(text):

    results = analyzer.analyze(
        text=text,
        language="en"
    )

    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )

    return anonymized_result.text, results