# ==========================================================
# TALENTSPHERE ELEVATE
# COLLEGE REAL CODING PRACTICE
# ==========================================================

import streamlit as st

from services.college.coding_service import (
    get_problems,
    run_sample,
    evaluate_solution,
)

from styles.college.theme import (
    apply_college_theme,
)


# ==========================================================
# HELPERS
# ==========================================================

def difficulty_icon(
    difficulty,
):

    icons = {
        "Easy": "🟢",
        "Medium": "🟡",
        "Hard": "🔴",
    }

    return icons.get(
        difficulty,
        "⚪",
    )


# ==========================================================
# PAGE
# ==========================================================

def render():

    apply_college_theme()

    problems = get_problems()


    # ======================================================
    # INITIAL SESSION STATE
    # ======================================================

    if (
        "college_completed_problems"
        not in st.session_state
    ):

        st.session_state[
            "college_completed_problems"
        ] = []


    completed = st.session_state[
        "college_completed_problems"
    ]


    # ======================================================
    # HERO
    # ======================================================

    st.html(
        """
<div class="college-hero">

    <div class="college-hero-badge">
        💻 TALENTSPHERE CODING LAB
    </div>

    <div class="college-hero-title">
        Coding Practice
    </div>

    <div class="college-hero-description">
        Solve real programming challenges,
        run Python code, test your solution
        against multiple test cases and
        prepare for placement coding rounds.
    </div>

</div>
"""
    )


    # ======================================================
    # SUMMARY
    # ======================================================

    progress_percentage = round(
        (
            len(
                completed
            )
            / len(
                problems
            )
        )
        * 100
    )


    st.html(
        f"""
<div class="college-metric-grid">

    <div class="college-metric-card">

        <div class="college-metric-icon">
            💻
        </div>

        <div class="college-metric-label">
            Problems
        </div>

        <div class="college-metric-value">
            {len(problems)}
        </div>

        <div class="college-metric-caption">
            Placement coding challenges
        </div>

    </div>


    <div class="college-metric-card">

        <div class="college-metric-icon">
            ✅
        </div>

        <div class="college-metric-label">
            Solved
        </div>

        <div class="college-metric-value">
            {len(completed)}
        </div>

        <div class="college-metric-caption">
            Successfully completed
        </div>

    </div>


    <div class="college-metric-card">

        <div class="college-metric-icon">
            📈
        </div>

        <div class="college-metric-label">
            Progress
        </div>

        <div class="college-metric-value">
            {progress_percentage}%
        </div>

        <div class="college-metric-caption">
            Overall coding progress
        </div>

    </div>


    <div class="college-metric-card">

        <div class="college-metric-icon">
            🏆
        </div>

        <div class="college-metric-label">
            Goal
        </div>

        <div class="college-metric-value">
            15
        </div>

        <div class="college-metric-caption">
            Solve every challenge
        </div>

    </div>

</div>
"""
    )


    st.progress(
        progress_percentage
        / 100
    )


    # ======================================================
    # FILTERS
    # ======================================================

    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            🧩 Problem Library
        </div>

        <div class="college-section-subtitle">
            Select a coding challenge
            and start solving
        </div>

    </div>

    <div class="college-section-tag">
        Python
    </div>

</div>
"""
    )


    filter_col1, filter_col2 = (
        st.columns(
            2
        )
    )


    with filter_col1:

        selected_difficulty = (
            st.selectbox(
                "Difficulty",
                [
                    "All",
                    "Easy",
                    "Medium",
                    "Hard",
                ],
                key="coding_difficulty",
            )
        )


    with filter_col2:

        topics = sorted(
            {
                problem[
                    "topic"
                ]

                for problem
                in problems
            }
        )

        selected_topic = (
            st.selectbox(
                "Topic",
                [
                    "All",
                    *topics,
                ],
                key="coding_topic",
            )
        )


    # ======================================================
    # FILTER PROBLEMS
    # ======================================================

    filtered = []

    for problem in problems:

        difficulty_ok = (

            selected_difficulty
            == "All"

            or

            problem[
                "difficulty"
            ]
            == selected_difficulty

        )

        topic_ok = (

            selected_topic
            == "All"

            or

            problem[
                "topic"
            ]
            == selected_topic

        )


        if (
            difficulty_ok
            and topic_ok
        ):

            filtered.append(
                problem
            )


    if not filtered:

        st.warning(
            "No coding problems match the selected filters."
        )

        return


    # ======================================================
    # SELECT PROBLEM
    # ======================================================

    problem_labels = {}

    for problem in filtered:

        solved_icon = (

            "✅"

            if problem[
                "id"
            ]
            in completed

            else "⭕"

        )


        label = (
            f'{solved_icon} '
            f'{problem["id"]}. '
            f'{problem["title"]} '
            f'• {problem["difficulty"]}'
        )


        problem_labels[
            label
        ] = problem


    selected_label = (
        st.selectbox(
            "Select Problem",
            list(
                problem_labels.keys()
            ),
            key="selected_coding_problem",
        )
    )


    problem = problem_labels[
        selected_label
    ]


    # ======================================================
    # PROBLEM HEADER
    # ======================================================

    st.divider()


    title_col, badge_col = (
        st.columns(
            [
                4,
                1,
            ]
        )
    )


    with title_col:

        st.markdown(
            f'## '
            f'{problem["id"]}. '
            f'{problem["title"]}'
        )


    with badge_col:

        st.write(
            (
                f'{difficulty_icon(problem["difficulty"])} '
                f'{problem["difficulty"]}'
            )
        )


    st.caption(
        f'📚 Topic: '
        f'{problem["topic"]}'
    )


    # ======================================================
    # PROBLEM STATEMENT
    # ======================================================

    st.markdown(
        "### 📖 Problem Statement"
    )

    st.write(
        problem[
            "description"
        ]
    )


    # ======================================================
    # FORMATS
    # ======================================================

    format1, format2 = (
        st.columns(
            2
        )
    )


    with format1:

        st.markdown(
            "#### 📥 Input Format"
        )

        st.info(
            problem[
                "input_format"
            ]
        )


    with format2:

        st.markdown(
            "#### 📤 Output Format"
        )

        st.info(
            problem[
                "output_format"
            ]
        )


    # ======================================================
    # SAMPLE
    # ======================================================

    st.markdown(
        "### 🧪 Sample Test"
    )


    sample1, sample2 = (
        st.columns(
            2
        )
    )


    with sample1:

        st.caption(
            "Sample Input"
        )

        st.code(
            problem[
                "sample_input"
            ],
            language="text",
        )


    with sample2:

        st.caption(
            "Expected Output"
        )

        st.code(
            problem[
                "sample_output"
            ],
            language="text",
        )


    # ======================================================
    # CODE EDITOR
    # ======================================================

    st.markdown(
        "## 👨‍💻 Python Code Editor"
    )


    editor_state_key = (
        f'college_editor_code_'
        f'{problem["id"]}'
    )


    if (
        editor_state_key
        not in st.session_state
    ):

        st.session_state[
            editor_state_key
        ] = problem[
            "starter_code"
        ]


    code = st.text_area(

        "Python code",

        value=st.session_state[
            editor_state_key
        ],

        height=380,

        key=(
            f'coding_editor_widget_'
            f'{problem["id"]}'
        ),

        label_visibility="collapsed",
    )


    st.session_state[
        editor_state_key
    ] = code


    # ======================================================
    # ACTION BUTTONS
    # ======================================================

    run_col, submit_col, reset_col = (
        st.columns(
            3
        )
    )


    with run_col:

        run_clicked = (
            st.button(
                "▶ Run Sample",
                key=(
                    f'coding_run_'
                    f'{problem["id"]}'
                ),
                use_container_width=True,
            )
        )


    with submit_col:

        submit_clicked = (
            st.button(
                "✅ Submit Solution",
                key=(
                    f'coding_submit_'
                    f'{problem["id"]}'
                ),
                use_container_width=True,
            )
        )


    with reset_col:

        reset_clicked = (
            st.button(
                "↻ Reset Code",
                key=(
                    f'coding_reset_'
                    f'{problem["id"]}'
                ),
                use_container_width=True,
            )
        )


    # ======================================================
    # RESET
    # ======================================================

    if reset_clicked:

        st.session_state[
            editor_state_key
        ] = problem[
            "starter_code"
        ]

        st.session_state.pop(
            (
                f'coding_editor_widget_'
                f'{problem["id"]}'
            ),
            None,
        )

        st.rerun()


    # ======================================================
    # RUN SAMPLE
    # ======================================================

    if run_clicked:

        with st.spinner(
            "Running your code..."
        ):

            result = run_sample(
                code,
                problem,
            )


        st.markdown(
            "### 🖥 Execution Result"
        )


        if result[
            "error"
        ]:

            st.error(
                result[
                    "error"
                ]
            )


        else:

            output_col, expected_col = (
                st.columns(
                    2
                )
            )


            with output_col:

                st.caption(
                    "Your Output"
                )

                st.code(
                    result[
                        "output"
                    ]
                    or "(no output)",
                    language="text",
                )


            with expected_col:

                st.caption(
                    "Expected Output"
                )

                st.code(
                    result[
                        "expected"
                    ],
                    language="text",
                )


            if result[
                "passed"
            ]:

                st.success(
                    "✅ Sample test passed."
                )


            else:

                st.error(
                    "❌ Sample test failed."
                )


    # ======================================================
    # SUBMISSION
    # ======================================================

    if submit_clicked:

        with st.spinner(
            "Evaluating hidden test cases..."
        ):

            result = (
                evaluate_solution(
                    code,
                    problem,
                )
            )


        st.markdown(
            "## 🎯 Submission Result"
        )


        result_col1, result_col2 = (
            st.columns(
                2
            )
        )


        with result_col1:

            st.metric(
                "Tests Passed",
                (
                    f'{result["passed"]}'
                    f' / '
                    f'{result["total"]}'
                ),
            )


        with result_col2:

            st.metric(
                "Score",
                f'{result["percentage"]}%',
            )


        st.progress(
            result[
                "percentage"
            ]
            / 100
        )


        if result[
            "all_passed"
        ]:

            st.success(
                "🎉 Accepted — all test cases passed!"
            )


            if (
                problem[
                    "id"
                ]
                not in completed
            ):

                completed.append(
                    problem[
                        "id"
                    ]
                )


            st.session_state[
                "college_completed_problems"
            ] = completed


        else:

            st.warning(
                (
                    f'{result["passed"]} '
                    f'of '
                    f'{result["total"]} '
                    f'test cases passed.'
                )
            )


        # ==================================================
        # TEST RESULTS
        # ==================================================

        st.markdown(
            "### 🧪 Test Cases"
        )


        for test in result[
            "tests"
        ]:

            icon = (

                "✅"

                if test[
                    "passed"
                ]

                else "❌"

            )


            with st.expander(
                (
                    f'{icon} '
                    f'Test Case '
                    f'{test["test"]}'
                )
            ):

                st.markdown(
                    "**Input**"
                )

                st.code(
                    test[
                        "input"
                    ],
                    language="text",
                )


                st.markdown(
                    "**Expected Output**"
                )

                st.code(
                    test[
                        "expected"
                    ],
                    language="text",
                )


                st.markdown(
                    "**Your Output**"
                )

                st.code(
                    test[
                        "output"
                    ]
                    or "(no output)",
                    language="text",
                )


                if test[
                    "error"
                ]:

                    st.error(
                        test[
                            "error"
                        ]
                    )


    # ======================================================
    # ALL PROBLEMS
    # ======================================================

    st.divider()


    st.html(
        """
<div class="college-section-header">

    <div>

        <div class="college-section-title">
            📚 All 15 Problems
        </div>

        <div class="college-section-subtitle">
            Complete every problem
            to finish the coding track
        </div>

    </div>

</div>
"""
    )


    easy_count = len(
        [
            p
            for p in problems
            if p[
                "difficulty"
            ]
            == "Easy"
        ]
    )


    medium_count = len(
        [
            p
            for p in problems
            if p[
                "difficulty"
            ]
            == "Medium"
        ]
    )


    hard_count = len(
        [
            p
            for p in problems
            if p[
                "difficulty"
            ]
            == "Hard"
        ]
    )


    diff1, diff2, diff3 = (
        st.columns(
            3
        )
    )


    with diff1:

        st.metric(
            "🟢 Easy",
            easy_count,
        )


    with diff2:

        st.metric(
            "🟡 Medium",
            medium_count,
        )


    with diff3:

        st.metric(
            "🔴 Hard",
            hard_count,
        )


    for item in problems:

        solved = (
            item[
                "id"
            ]
            in completed
        )


        status = (

            "✅"

            if solved

            else "⭕"

        )


        st.write(
            (
                f'{status} '
                f'**{item["id"]}. '
                f'{item["title"]}** '
                f'— '
                f'{difficulty_icon(item["difficulty"])} '
                f'{item["difficulty"]} '
                f'— '
                f'{item["topic"]}'
            )
        )