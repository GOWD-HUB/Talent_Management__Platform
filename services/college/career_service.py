ROLE_SKILLS = {
    "Software Development Engineer":["Python","Java","C++","DSA","DBMS","Git"],
    "Full Stack Developer":["HTML","CSS","JavaScript","React","Node.js","MongoDB"],
    "Data Analyst":["Python","SQL","Excel","Pandas","Power BI","Statistics"],
    "Machine Learning Engineer":["Python","Machine Learning","Deep Learning","SQL","Git"],
    "Cloud Engineer":["Linux","Networking","AWS","Docker","Git"]
}

def _skills(v):
    return {x.strip().lower() for x in str(v or "").split(",") if x.strip()}

def gap(p):
    role = p.get("preferred_role") or "Software Development Engineer"
    req = ROLE_SKILLS.get(role, ROLE_SKILLS["Software Development Engineer"])
    current = _skills(p.get("technical_skills"))
    present = [s for s in req if s.lower() in current]
    missing = [s for s in req if s.lower() not in current]
    return {"role":role,"present":present,"missing":missing,"fit":round(len(present)/len(req)*100)}

def matches(p):
    current = _skills(p.get("technical_skills"))
    out = []
    for role, req in ROLE_SKILLS.items():
        fit = round(sum(1 for s in req if s.lower() in current) / len(req) * 100)
        out.append((role, fit))
    return sorted(out, key=lambda x:x[1], reverse=True)
