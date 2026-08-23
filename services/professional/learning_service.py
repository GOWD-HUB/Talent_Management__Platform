TRACKS = {
    "Backend": {
        "icon": "🧱",
        "modules": [
            "API Design & REST Principles",
            "Authentication & Authorization",
            "Database Design & Query Optimization",
            "Caching & Background Jobs",
            "Microservices Fundamentals",
            "Testing & Observability",
        ],
        "project": "Build a production-ready API with authentication, caching and tests.",
        "assessment": "Backend architecture case study + implementation review.",
    },
    "System Design": {
        "icon": "🏗️",
        "modules": [
            "Scalability Fundamentals",
            "Load Balancing & Caching",
            "Database Scaling",
            "Messaging & Event-Driven Systems",
            "Reliability & Observability",
            "System Design Interviews",
        ],
        "project": "Design a scalable notification or food-delivery system.",
        "assessment": "45-minute end-to-end system design challenge.",
    },
    "Cloud": {
        "icon": "☁️",
        "modules": [
            "Cloud Fundamentals",
            "Compute & Storage",
            "Networking & IAM",
            "Managed Databases",
            "Serverless & Containers",
            "Monitoring & Cost Optimization",
        ],
        "project": "Deploy a multi-tier application to a cloud platform.",
        "assessment": "Cloud architecture and deployment assessment.",
    },
    "DevOps": {
        "icon": "⚙️",
        "modules": [
            "Linux & Shell",
            "Git Workflows",
            "Docker",
            "CI/CD",
            "Kubernetes",
            "Infrastructure as Code",
        ],
        "project": "Create an automated CI/CD pipeline for a containerized application.",
        "assessment": "DevOps pipeline + deployment review.",
    },
    "Leadership": {
        "icon": "🧭",
        "modules": [
            "Leadership Foundations",
            "Delegation",
            "Mentoring",
            "Conflict Resolution",
            "Stakeholder Management",
            "Decision Making",
        ],
        "project": "Create a team execution plan for a six-week engineering initiative.",
        "assessment": "Leadership scenario evaluation.",
    },
    "Communication": {
        "icon": "🎙️",
        "modules": [
            "Executive Communication",
            "Technical Storytelling",
            "Presentation Design",
            "Meetings & Facilitation",
            "Difficult Conversations",
            "Influencing Without Authority",
        ],
        "project": "Prepare and deliver a technical proposal for leadership.",
        "assessment": "Presentation + structured communication assessment.",
    },
}


def six_week_plan(track_name):
    track = TRACKS.get(track_name, {})

    modules = track.get("modules", [])

    plan = []

    for index, module in enumerate(modules[:6], start=1):
        plan.append(
            {
                "week": index,
                "focus": module,
                "practice": f"Complete focused exercises for {module}.",
            }
        )

    return plan
