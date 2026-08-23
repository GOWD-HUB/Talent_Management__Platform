def ats_match(resume_text, job_description):
    rw = set(str(resume_text or "").lower().replace(",", " ").split())
    jw = set(str(job_description or "").lower().replace(",", " ").split())
    if not jw:
        return 0, []
    overlap = rw & jw
    score = round(len(overlap) / len(jw) * 100)
    return min(score,100), sorted(jw-rw)[:20]
