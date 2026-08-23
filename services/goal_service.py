from datetime import date, datetime

CATEGORY_ICONS = {"Academic":"📚","Career":"🚀","Skill":"🛣️","Personal":"🌱"}

def calculate_goal_progress(goal):
    milestones = goal.get("milestones", [])
    completed = goal.get("completed_milestones", [])
    return round(len(completed)/len(milestones)*100) if milestones else 0

def get_days_remaining(target_date):
    if not target_date:
        return None
    try:
        target = datetime.strptime(target_date,"%Y-%m-%d").date()
    except Exception:
        return None
    return (target-date.today()).days

def get_deadline_label(target_date):
    days = get_days_remaining(target_date)
    if days is None: return "No deadline"
    if days < 0: return f"{abs(days)} days overdue"
    if days == 0: return "Due today"
    if days == 1: return "Due tomorrow"
    return f"{days} days remaining"

def get_goal_health(goal):
    if goal.get("status") == "Completed": return "Completed"
    p = calculate_goal_progress(goal)
    d = get_days_remaining(goal.get("target_date"))
    if d is not None and d < 0: return "Overdue"
    if d is not None and d <= 7 and p < 75: return "Needs Attention"
    if p >= 75: return "On Track"
    return "In Progress"

def get_goal_summary(goals):
    total = len(goals)
    completed = sum(1 for g in goals if g.get("status")=="Completed")
    active = sum(1 for g in goals if g.get("status")=="Active")
    overdue = sum(1 for g in goals if get_goal_health(g)=="Overdue")
    overall = round(sum(calculate_goal_progress(g) for g in goals)/total) if total else 0
    return {"total":total,"active":active,"completed":completed,"overdue":overdue,"overall_progress":overall}

def get_recommendation(goals):
    if not goals:
        return "Create your first academic or career goal. Start with one small target."
    active = [g for g in goals if g.get("status")=="Active"]
    if not active:
        return "All current goals are complete. Create a new goal to continue progressing."
    overdue = [g for g in active if get_goal_health(g)=="Overdue"]
    if overdue:
        return f"Review your overdue goal: {overdue[0].get('title','Goal')}."
    attention = [g for g in active if get_goal_health(g)=="Needs Attention"]
    if attention:
        return f"Focus next on: {attention[0].get('title','Goal')}."
    lowest = min(active,key=calculate_goal_progress)
    return f"Your next priority can be {lowest.get('title','your active goal')}."
