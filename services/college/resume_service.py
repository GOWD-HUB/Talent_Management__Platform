def score_profile(p):
    checks = [p.get("college_name"),p.get("technical_skills"),p.get("projects"),p.get("internships"),p.get("certifications"),p.get("github_url"),p.get("linkedin_url"),p.get("preferred_role")]
    score = round(sum(1 for x in checks if str(x or "").strip()) / len(checks) * 100)
    tips = []
    if not p.get("projects"): tips.append("Add 2-3 strong projects.")
    if not p.get("internships"): tips.append("Add internship or training experience.")
    if not p.get("github_url"): tips.append("Add GitHub profile.")
    if not p.get("linkedin_url"): tips.append("Add LinkedIn profile.")
    if not tips: tips.append("Core sections are present. Improve impact statements and measurable results.")
    return score, tips
