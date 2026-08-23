from services.college.placement_service import readiness
from services.college.resume_service import score_profile
from services.college.career_service import gap

def build(p, placements, internships, hackathons):
    r = readiness(p)
    resume, tips = score_profile(p)
    g = gap(p)
    return {
        "readiness":r,
        "resume_score":resume,
        "tips":tips,
        "gap":g,
        "applications":len(placements),
        "internships":len(internships),
        "hackathons":len(hackathons),
        "offers":sum(1 for x in placements if x.get("status") == "Offer"),
    }
