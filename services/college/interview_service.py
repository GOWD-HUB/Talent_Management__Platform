BANK = {
    "HR":["Tell me about yourself.","Why should we hire you?","What are your strengths?"],
    "Technical":["Explain your best project.","Explain OOP concepts.","What is normalization in DBMS?"],
    "Behavioural":["Tell me about a team conflict.","Describe a failure and lesson.","Give an example of leadership."]
}

def evaluate(answer):
    words = len(str(answer or "").split())
    if words >= 80: return 90, "Detailed answer; keep it structured."
    if words >= 45: return 75, "Good answer; add measurable results."
    if words >= 20: return 60, "Add situation, action and result."
    return 40, "Too brief; expand with a specific example."
