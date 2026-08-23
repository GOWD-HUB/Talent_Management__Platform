# ==========================================================
# TALENTSPHERE ELEVATE
# COLLEGE CODING PRACTICE SERVICE
# 15 REAL CODING PROBLEMS
# ==========================================================

import subprocess
import sys
import tempfile
from pathlib import Path


# ==========================================================
# CODING PROBLEMS
# ==========================================================

CODING_PROBLEMS = [

    {
        "id": 1,
        "title": "Sum of Two Numbers",
        "difficulty": "Easy",
        "topic": "Basics",
        "description": "Read two integers and print their sum.",
        "input_format": "Two space-separated integers.",
        "output_format": "Print the sum of the two integers.",
        "sample_input": "10 20",
        "sample_output": "30",
        "starter_code": """a, b = map(int, input().split())

# Write your code here
""",
        "tests": [
            ("10 20", "30"),
            ("5 7", "12"),
            ("-5 10", "5"),
            ("100 250", "350"),
        ],
    },

    {
        "id": 2,
        "title": "Even or Odd",
        "difficulty": "Easy",
        "topic": "Conditionals",
        "description": "Read an integer and determine whether it is even or odd.",
        "input_format": "A single integer.",
        "output_format": "Print Even if the number is even, otherwise print Odd.",
        "sample_input": "8",
        "sample_output": "Even",
        "starter_code": """n = int(input())

# Write your code here
""",
        "tests": [
            ("8", "Even"),
            ("5", "Odd"),
            ("0", "Even"),
            ("101", "Odd"),
        ],
    },

    {
        "id": 3,
        "title": "Largest of Three Numbers",
        "difficulty": "Easy",
        "topic": "Conditionals",
        "description": "Read three integers and print the largest number.",
        "input_format": "Three space-separated integers.",
        "output_format": "Print the largest integer.",
        "sample_input": "10 35 20",
        "sample_output": "35",
        "starter_code": """a, b, c = map(int, input().split())

# Write your code here
""",
        "tests": [
            ("10 35 20", "35"),
            ("5 5 2", "5"),
            ("-1 -9 -4", "-1"),
            ("100 50 80", "100"),
        ],
    },

    {
        "id": 4,
        "title": "Reverse a String",
        "difficulty": "Easy",
        "topic": "Strings",
        "description": "Read a string and print it in reverse order.",
        "input_format": "A single line containing a string.",
        "output_format": "Print the reversed string.",
        "sample_input": "TalentSphere",
        "sample_output": "erehpStnelaT",
        "starter_code": """text = input()

# Write your code here
""",
        "tests": [
            ("hello", "olleh"),
            ("TalentSphere", "erehpStnelaT"),
            ("python", "nohtyp"),
            ("abc123", "321cba"),
        ],
    },

    {
        "id": 5,
        "title": "Palindrome Check",
        "difficulty": "Easy",
        "topic": "Strings",
        "description": "Check whether the given string is a palindrome.",
        "input_format": "A single string.",
        "output_format": "Print Palindrome or Not Palindrome.",
        "sample_input": "madam",
        "sample_output": "Palindrome",
        "starter_code": """text = input()

# Write your code here
""",
        "tests": [
            ("madam", "Palindrome"),
            ("level", "Palindrome"),
            ("python", "Not Palindrome"),
            ("racecar", "Palindrome"),
        ],
    },

    {
        "id": 6,
        "title": "Factorial of a Number",
        "difficulty": "Easy",
        "topic": "Loops",
        "description": "Calculate the factorial of a non-negative integer.",
        "input_format": "A single non-negative integer.",
        "output_format": "Print the factorial.",
        "sample_input": "5",
        "sample_output": "120",
        "starter_code": """n = int(input())

# Write your code here
""",
        "tests": [
            ("5", "120"),
            ("0", "1"),
            ("1", "1"),
            ("7", "5040"),
        ],
    },

    {
        "id": 7,
        "title": "Prime Number Check",
        "difficulty": "Easy",
        "topic": "Loops",
        "description": "Determine whether the given integer is prime.",
        "input_format": "A single integer.",
        "output_format": "Print Prime or Not Prime.",
        "sample_input": "17",
        "sample_output": "Prime",
        "starter_code": """n = int(input())

# Write your code here
""",
        "tests": [
            ("17", "Prime"),
            ("10", "Not Prime"),
            ("2", "Prime"),
            ("1", "Not Prime"),
        ],
    },

    {
        "id": 8,
        "title": "Fibonacci Series",
        "difficulty": "Medium",
        "topic": "Loops",
        "description": "Print the first N Fibonacci numbers.",
        "input_format": "A single positive integer N.",
        "output_format": "Print N Fibonacci numbers separated by spaces.",
        "sample_input": "6",
        "sample_output": "0 1 1 2 3 5",
        "starter_code": """n = int(input())

# Write your code here
""",
        "tests": [
            ("6", "0 1 1 2 3 5"),
            ("1", "0"),
            ("2", "0 1"),
            ("8", "0 1 1 2 3 5 8 13"),
        ],
    },

    {
        "id": 9,
        "title": "Maximum Element in Array",
        "difficulty": "Medium",
        "topic": "Arrays",
        "description": "Find the maximum element in the given array.",
        "input_format": "First line contains N. Second line contains N integers.",
        "output_format": "Print the maximum element.",
        "sample_input": "5\n10 4 25 7 18",
        "sample_output": "25",
        "starter_code": """n = int(input())
arr = list(map(int, input().split()))

# Write your code here
""",
        "tests": [
            ("5\n10 4 25 7 18", "25"),
            ("3\n-1 -5 -2", "-1"),
            ("4\n5 5 5 5", "5"),
            ("6\n1 100 3 50 70 2", "100"),
        ],
    },

    {
        "id": 10,
        "title": "Second Largest Element",
        "difficulty": "Medium",
        "topic": "Arrays",
        "description": "Find the second largest distinct element in the array.",
        "input_format": "First line contains N. Second line contains N integers.",
        "output_format": "Print the second largest distinct value.",
        "sample_input": "5\n10 20 40 30 40",
        "sample_output": "30",
        "starter_code": """n = int(input())
arr = list(map(int, input().split()))

# Write your code here
""",
        "tests": [
            ("5\n10 20 40 30 40", "30"),
            ("4\n5 1 2 3", "3"),
            ("5\n100 90 80 70 60", "90"),
            ("6\n1 5 5 4 3 2", "4"),
        ],
    },

    {
        "id": 11,
        "title": "Count Vowels",
        "difficulty": "Medium",
        "topic": "Strings",
        "description": "Count the total number of vowels in the given string.",
        "input_format": "A single line containing text.",
        "output_format": "Print the number of vowels.",
        "sample_input": "TalentSphere",
        "sample_output": "4",
        "starter_code": """text = input()

# Write your code here
""",
        "tests": [
            ("TalentSphere", "4"),
            ("hello", "2"),
            ("AEIOU", "5"),
            ("rhythm", "0"),
        ],
    },

    {
        "id": 12,
        "title": "Remove Duplicates",
        "difficulty": "Medium",
        "topic": "Arrays",
        "description": "Remove duplicate elements while preserving original order.",
        "input_format": "One line containing space-separated integers.",
        "output_format": "Print unique values in original order.",
        "sample_input": "1 2 2 3 1 4",
        "sample_output": "1 2 3 4",
        "starter_code": """arr = list(map(int, input().split()))

# Write your code here
""",
        "tests": [
            ("1 2 2 3 1 4", "1 2 3 4"),
            ("5 5 5 5", "5"),
            ("1 2 3", "1 2 3"),
            ("4 3 4 2 3 1", "4 3 2 1"),
        ],
    },

    {
        "id": 13,
        "title": "Linear Search",
        "difficulty": "Medium",
        "topic": "Searching",
        "description": "Find the zero-based index of a target using linear search.",
        "input_format": "First line contains array values. Second line contains target.",
        "output_format": "Print target index or -1.",
        "sample_input": "10 20 30 40\n30",
        "sample_output": "2",
        "starter_code": """arr = list(map(int, input().split()))
target = int(input())

# Write your code here
""",
        "tests": [
            ("10 20 30 40\n30", "2"),
            ("5 8 12\n5", "0"),
            ("1 2 3\n10", "-1"),
            ("4 7 9 11\n11", "3"),
        ],
    },

    {
        "id": 14,
        "title": "Binary Search",
        "difficulty": "Hard",
        "topic": "Searching",
        "description": "Find the index of a target in a sorted array using binary search.",
        "input_format": "First line contains sorted integers. Second line contains target.",
        "output_format": "Print target index or -1.",
        "sample_input": "10 20 30 40 50\n40",
        "sample_output": "3",
        "starter_code": """arr = list(map(int, input().split()))
target = int(input())

# Implement binary search
""",
        "tests": [
            ("10 20 30 40 50\n40", "3"),
            ("1 3 5 7 9\n1", "0"),
            ("2 4 6 8\n7", "-1"),
            ("5 10 15 20\n20", "3"),
        ],
    },

    {
        "id": 15,
        "title": "Two Sum",
        "difficulty": "Hard",
        "topic": "Arrays",
        "description": "Find two zero-based indices whose values add up to target.",
        "input_format": "First line contains integers. Second line contains target.",
        "output_format": "Print the two indices separated by a space.",
        "sample_input": "2 7 11 15\n9",
        "sample_output": "0 1",
        "starter_code": """arr = list(map(int, input().split()))
target = int(input())

# Write your code here
""",
        "tests": [
            ("2 7 11 15\n9", "0 1"),
            ("3 2 4\n6", "1 2"),
            ("3 3\n6", "0 1"),
            ("1 5 8 10\n15", "1 3"),
        ],
    },
]


# ==========================================================
# GET ALL PROBLEMS
# ==========================================================

def get_problems():
    return CODING_PROBLEMS


# ==========================================================
# GET ONE PROBLEM
# ==========================================================

def get_problem(problem_id):

    for problem in CODING_PROBLEMS:

        if problem["id"] == problem_id:
            return problem

    return None


# ==========================================================
# OUTPUT NORMALIZATION
# ==========================================================

def normalize_output(value):

    value = str(value or "").strip()

    return "\n".join(
        line.rstrip()
        for line in value.splitlines()
    )


# ==========================================================
# EXECUTE STUDENT PYTHON CODE
# ==========================================================

def execute_python(
    code,
    input_data,
    timeout=3,
):

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as temp_file:

            temp_file.write(code)

            temp_path = Path(
                temp_file.name
            )

        process = subprocess.run(
            [
                sys.executable,
                str(temp_path),
            ],
            input=str(input_data),
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if process.returncode != 0:

            return {
                "success": False,
                "output": process.stdout.strip(),
                "error": process.stderr.strip(),
            }

        return {
            "success": True,
            "output": process.stdout.strip(),
            "error": "",
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "output": "",
            "error": (
                "Time Limit Exceeded. "
                f"Your code took more than {timeout} seconds."
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "output": "",
            "error": str(error),
        }

    finally:

        if temp_path and temp_path.exists():

            try:
                temp_path.unlink()

            except Exception:
                pass


# ==========================================================
# RUN SAMPLE TEST
# ==========================================================

def run_sample(
    code,
    problem,
):

    execution = execute_python(
        code,
        problem["sample_input"],
    )

    if not execution["success"]:

        return {
            "passed": False,
            "output": execution["output"],
            "expected": problem["sample_output"],
            "error": execution["error"],
        }

    actual = normalize_output(
        execution["output"]
    )

    expected = normalize_output(
        problem["sample_output"]
    )

    return {
        "passed": actual == expected,
        "output": execution["output"],
        "expected": problem["sample_output"],
        "error": "",
    }


# ==========================================================
# EVALUATE ALL TEST CASES
# ==========================================================

def evaluate_solution(
    code,
    problem,
):

    test_results = []

    passed_count = 0

    for index, (
        test_input,
        expected_output,
    ) in enumerate(
        problem["tests"],
        start=1,
    ):

        execution = execute_python(
            code,
            test_input,
        )

        passed = False

        if execution["success"]:

            passed = (
                normalize_output(
                    execution["output"]
                )
                ==
                normalize_output(
                    expected_output
                )
            )

        if passed:
            passed_count += 1

        test_results.append(
            {
                "test": index,
                "passed": passed,
                "input": test_input,
                "expected": expected_output,
                "output": execution["output"],
                "error": execution["error"],
            }
        )

    total = len(
        problem["tests"]
    )

    percentage = (
        round(
            passed_count
            / total
            * 100
        )
        if total
        else 0
    )

    return {
        "passed": passed_count,
        "total": total,
        "percentage": percentage,
        "all_passed": passed_count == total,
        "tests": test_results,
    }