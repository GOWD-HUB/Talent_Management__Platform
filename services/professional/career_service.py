from .profile_service import split_items


ROLE_SKILLS = {
    "Senior Software Engineer": [
        "DSA", "System Design", "APIs", "Git", "SQL",
        "Cloud", "Testing", "Architecture"
    ],
    "Engineering Lead": [
        "System Design", "Architecture", "Leadership",
        "Mentoring", "Cloud", "DevOps", "Communication"
    ],
    "Backend Engineer": [
        "Python", "Java", "Node.js", "SQL", "REST API",
        "Microservices", "Docker", "Cloud"
    ],
    "Full Stack Engineer": [
        "JavaScript", "React", "Node.js", "SQL",
        "MongoDB", "REST API", "Git", "Cloud"
    ],
    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "Pandas", "NumPy", "TensorFlow", "PyTorch", "MLOps"
    ],
    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "NLP", "Computer Vision", "LLMs", "APIs", "Cloud"
    ],
    "Data Scientist": [
        "Python", "SQL", "Statistics", "Machine Learning",
        "Pandas", "Visualization", "Experimentation"
    ],
    "Data Engineer": [
        "Python", "SQL", "ETL", "Spark", "Kafka",
        "Cloud", "Data Warehousing", "Airflow"
    ],
    "Cloud Engineer": [
        "AWS", "Azure", "GCP", "Linux", "Networking",
        "Docker", "Kubernetes", "Terraform"
    ],
    "DevOps Engineer": [
        "Linux", "Git", "Docker", "Kubernetes",
        "CI/CD", "Jenkins", "Cloud", "Terraform"
    ],
    "Product Manager - Technology": [
        "Product Strategy", "Communication", "Analytics",
        "Roadmapping", "Stakeholder Management", "Leadership"
    ],
}


ALIASES = {
    "rest api": {"api", "apis", "rest", "rest api", "fastapi"},
    "cloud": {"aws", "azure", "gcp", "cloud", "cloud computing"},
    "javascript": {"javascript", "js"},
    "node.js": {"node", "nodejs", "node.js"},
    "machine learning": {"machine learning", "ml"},
    "deep learning": {"deep learning", "dl"},
    "llms": {"llm", "llms", "generative ai", "genai"},
    "communication": {"communication", "presentation", "public speaking"},
    "leadership": {"leadership", "team lead", "mentoring"},
}


def _normalize(value):
    return str(value or "").strip().lower()


def _match(required, current):
    r = _normalize(required)
    c = _normalize(current)

    if r == c or r in c or c in r:
        return True

    aliases = ALIASES.get(r, set())

    return c in aliases


def role_matches(profile):
    skills = split_items(profile.get("tech_stack"))

    # Include leadership/communication profile evidence.
    if str(profile.get("leadership_exposure") or "") in {"Moderate", "High"}:
        skills.append("Leadership")

    if str(profile.get("communication_level") or "") in {"Good", "Excellent"}:
        skills.append("Communication")

    matches = []

    for role, requirements in ROLE_SKILLS.items():
        present = []
        missing = []

        for requirement in requirements:
            found = any(
                _match(requirement, skill)
                for skill in skills
            )

            if found:
                present.append(requirement)
            else:
                missing.append(requirement)

        score = round(
            len(present) / len(requirements) * 100
        ) if requirements else 0

        matches.append(
            {
                "role": role,
                "score": score,
                "present": present,
                "missing": missing,
            }
        )

    matches.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return matches


def transition_suggestions(profile):
    matches = role_matches(profile)
    current = _normalize(profile.get("current_role"))

    suggestions = [
        item
        for item in matches
        if _normalize(item["role"]) != current
    ]

    return suggestions[:5]
