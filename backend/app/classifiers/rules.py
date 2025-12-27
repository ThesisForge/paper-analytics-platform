from typing import List, Tuple
import re

DOMAIN_RULES = {
    "Information Technology": [r"computer", r"software", r"data", r"network"],
    "Medicine": [r"medical", r"clinic", r"patient", r"therapy"],
    "Biology": [r"genome", r"cell", r"protein"],
    "Physics": [r"quantum", r"particle", r"physics"],
    "Mathematics": [r"theorem", r"proof", r"algebra"],
}

SUBTOPIC_RULES = {
    "AI": [r"artificial intelligence", r"machine learning", r"deep learning", r"neural"],
    "IoT": [r"internet of things", r"iot", r"sensor network"],
    "Cybersecurity": [r"security", r"cyber", r"cryptography"],
    "Data Science": [r"data", r"analytics", r"statistics"],
    "Robotics": [r"robot", r"autonomous"],
    "Medical Imaging": [r"imaging", r"radiology", r"ct scan"],
    "Genomics": [r"genomic", r"dna", r"rna"],
}


def classify_text(text: str) -> Tuple[str, List[str]]:
    lower_text = text.lower()
    domain = "Other"
    for dom, patterns in DOMAIN_RULES.items():
        if any(re.search(p, lower_text) for p in patterns):
            domain = dom
            break

    subtopics: List[str] = []
    for topic, patterns in SUBTOPIC_RULES.items():
        if any(re.search(p, lower_text) for p in patterns):
            subtopics.append(topic)
    if not subtopics and domain == "Information Technology":
        subtopics.append("Data Science")
    return domain, subtopics
