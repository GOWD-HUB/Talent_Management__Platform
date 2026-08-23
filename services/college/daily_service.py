CHALLENGES = [
    ("Python","Write a function to reverse a string without slicing."),
    ("DSA","Find the maximum element in an array in one traversal."),
    ("DBMS","Write a SQL query to find the second highest salary."),
    ("Logic","Check whether a number is prime efficiently."),
    ("Web","Explain how frontend and backend communicate using APIs.")
]
def challenge_for_day(index):
    return CHALLENGES[index % len(CHALLENGES)]
