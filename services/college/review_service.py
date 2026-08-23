# ==========================================================
# TALENTSPHERE ELEVATE
# GITHUB PORTFOLIO REVIEW SERVICE
# ==========================================================

import os
import re
from urllib.parse import urlparse

import requests


GITHUB_API = "https://api.github.com"


# ==========================================================
# HEADERS
# ==========================================================

def get_headers():

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "TalentSphere-Elevate",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Optional:
    # Add GITHUB_TOKEN to environment variables
    # for higher GitHub API limits.

    token = os.getenv(
        "GITHUB_TOKEN"
    )

    if token:

        headers[
            "Authorization"
        ] = f"Bearer {token}"

    return headers


# ==========================================================
# EXTRACT USERNAME
# ==========================================================

def extract_github_username(value):

    if not value:
        return None

    value = str(
        value
    ).strip()


    # ------------------------------------------------------
    # Handle plain username
    # ------------------------------------------------------

    if re.fullmatch(
        r"[A-Za-z0-9-]+",
        value,
    ):

        return value


    # ------------------------------------------------------
    # Add scheme if needed
    # ------------------------------------------------------

    if not value.startswith(
        (
            "http://",
            "https://",
        )
    ):

        value = (
            "https://"
            + value
        )


    try:

        parsed = urlparse(
            value
        )

        hostname = (
            parsed.netloc
            .lower()
            .replace(
                "www.",
                "",
            )
        )


        if hostname != "github.com":

            return None


        parts = [
            part
            for part
            in parsed.path.split("/")
            if part
        ]


        if not parts:

            return None


        username = parts[0]


        if not re.fullmatch(
            r"[A-Za-z0-9-]+",
            username,
        ):

            return None


        return username


    except Exception:

        return None


# ==========================================================
# GITHUB REQUEST
# ==========================================================

def github_get(
    endpoint,
    params=None,
):

    try:

        response = requests.get(
            f"{GITHUB_API}{endpoint}",
            headers=get_headers(),
            params=params,
            timeout=12,
        )


        if response.status_code == 404:

            return {
                "success": False,
                "status": 404,
                "error": (
                    "GitHub profile or resource was not found."
                ),
                "data": None,
            }


        if response.status_code == 403:

            return {
                "success": False,
                "status": 403,
                "error": (
                    "GitHub API rate limit reached. "
                    "Please try again later or configure "
                    "a GITHUB_TOKEN environment variable."
                ),
                "data": None,
            }


        if not response.ok:

            return {
                "success": False,
                "status": response.status_code,
                "error": (
                    f"GitHub returned HTTP "
                    f"{response.status_code}."
                ),
                "data": None,
            }


        return {
            "success": True,
            "status": response.status_code,
            "error": "",
            "data": response.json(),
        }


    except requests.RequestException as error:

        return {
            "success": False,
            "status": 0,
            "error": (
                "Unable to connect to GitHub: "
                f"{error}"
            ),
            "data": None,
        }


# ==========================================================
# PROFILE
# ==========================================================

def get_github_profile(
    username,
):

    result = github_get(
        f"/users/{username}"
    )

    return result


# ==========================================================
# REPOSITORIES
# ==========================================================

def get_github_repositories(
    username,
):

    repositories = []

    page = 1


    while page <= 3:

        result = github_get(
            f"/users/{username}/repos",
            params={
                "per_page": 100,
                "page": page,
                "sort": "updated",
            },
        )


        if not result[
            "success"
        ]:

            return result


        data = result[
            "data"
        ]


        repositories.extend(
            data
        )


        if len(data) < 100:

            break


        page += 1


    # Ignore forks for portfolio scoring

    original_repositories = [

        repo
        for repo in repositories
        if not repo.get(
            "fork",
            False,
        )

    ]


    return {
        "success": True,
        "status": 200,
        "error": "",
        "data": original_repositories,
    }


# ==========================================================
# README CHECK
# ==========================================================

def repository_has_readme(
    owner,
    repo_name,
):

    result = github_get(
        f"/repos/{owner}/{repo_name}/readme"
    )

    return result[
        "success"
    ]


# ==========================================================
# LANGUAGE ANALYSIS
# ==========================================================

def get_language_summary(
    repositories,
):

    language_count = {}


    for repo in repositories:

        language = repo.get(
            "language"
        )

        if not language:
            continue


        language_count[
            language
        ] = (
            language_count.get(
                language,
                0,
            )
            + 1
        )


    return dict(
        sorted(
            language_count.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )


# ==========================================================
# REPOSITORY QUALITY
# ==========================================================

def analyze_repository_quality(
    username,
    repositories,
):

    total = len(
        repositories
    )


    if total == 0:

        return {
            "readme_count": 0,
            "description_count": 0,
            "topic_count": 0,
            "star_count": 0,
            "fork_count": 0,
            "portfolio_repositories": [],
        }


    readme_count = 0

    description_count = 0

    topic_count = 0

    star_count = 0

    fork_count = 0


    # Avoid making too many API requests.
    # Review README for max 15 latest repos.

    repos_for_readme = repositories[
        :15
    ]


    readme_names = set()


    for repo in repos_for_readme:

        name = repo.get(
            "name"
        )

        if (
            name
            and repository_has_readme(
                username,
                name,
            )
        ):

            readme_count += 1

            readme_names.add(
                name
            )


    portfolio_repositories = []


    for repo in repositories:

        if repo.get(
            "description"
        ):

            description_count += 1


        if repo.get(
            "topics"
        ):

            topic_count += 1


        star_count += int(
            repo.get(
                "stargazers_count"
            )
            or 0
        )


        fork_count += int(
            repo.get(
                "forks_count"
            )
            or 0
        )


        portfolio_repositories.append(
            {
                "name":
                    repo.get(
                        "name",
                        "",
                    ),

                "description":
                    repo.get(
                        "description"
                    )
                    or "",

                "language":
                    repo.get(
                        "language"
                    )
                    or "Not specified",

                "stars":
                    int(
                        repo.get(
                            "stargazers_count"
                        )
                        or 0
                    ),

                "forks":
                    int(
                        repo.get(
                            "forks_count"
                        )
                        or 0
                    ),

                "has_readme":
                    repo.get(
                        "name"
                    )
                    in readme_names,

                "updated_at":
                    repo.get(
                        "updated_at"
                    )
                    or "",

                "url":
                    repo.get(
                        "html_url"
                    )
                    or "",
            }
        )


    return {
        "readme_count":
            readme_count,

        "description_count":
            description_count,

        "topic_count":
            topic_count,

        "star_count":
            star_count,

        "fork_count":
            fork_count,

        "portfolio_repositories":
            portfolio_repositories,
    }


# ==========================================================
# SCORE CALCULATION
# ==========================================================

def calculate_github_scores(
    profile,
    repositories,
    quality,
    languages,
):

    total_repos = len(
        repositories
    )


    # ------------------------------------------------------
    # PROFILE SCORE
    # ------------------------------------------------------

    profile_fields = [

        profile.get(
            "name"
        ),

        profile.get(
            "bio"
        ),

        profile.get(
            "location"
        ),

        profile.get(
            "blog"
        ),

        profile.get(
            "company"
        ),

    ]


    profile_completed = sum(
        1
        for value in profile_fields
        if str(
            value
            or ""
        ).strip()
    )


    profile_score = round(
        profile_completed
        / len(profile_fields)
        * 100
    )


    # ------------------------------------------------------
    # REPOSITORY SCORE
    # ------------------------------------------------------

    if total_repos >= 10:

        repository_score = 100

    elif total_repos >= 7:

        repository_score = 85

    elif total_repos >= 5:

        repository_score = 70

    elif total_repos >= 3:

        repository_score = 55

    elif total_repos >= 1:

        repository_score = 35

    else:

        repository_score = 0


    # ------------------------------------------------------
    # DOCUMENTATION SCORE
    # ------------------------------------------------------

    reviewed_count = min(
        total_repos,
        15,
    )


    if reviewed_count:

        readme_ratio = (
            quality[
                "readme_count"
            ]
            / reviewed_count
        )

        description_ratio = (
            quality[
                "description_count"
            ]
            / total_repos
        )


        documentation_score = round(
            (
                readme_ratio
                * 70
            )
            +
            (
                description_ratio
                * 30
            )
        )

    else:

        documentation_score = 0


    documentation_score = min(
        100,
        documentation_score,
    )


    # ------------------------------------------------------
    # LANGUAGE DIVERSITY
    # ------------------------------------------------------

    language_total = len(
        languages
    )


    if language_total >= 5:

        technology_score = 100

    elif language_total == 4:

        technology_score = 90

    elif language_total == 3:

        technology_score = 75

    elif language_total == 2:

        technology_score = 60

    elif language_total == 1:

        technology_score = 40

    else:

        technology_score = 0


    # ------------------------------------------------------
    # PROJECT QUALITY
    # ------------------------------------------------------

    star_score = min(
        quality[
            "star_count"
        ]
        * 5,
        35,
    )


    topic_score = (

        min(
            quality[
                "topic_count"
            ]
            / max(
                total_repos,
                1,
            )
            * 30,
            30,
        )

    )


    description_quality = (

        min(
            quality[
                "description_count"
            ]
            / max(
                total_repos,
                1,
            )
            * 35,
            35,
        )

    )


    project_quality_score = round(
        star_score
        + topic_score
        + description_quality
    )


    # ------------------------------------------------------
    # ACTIVITY
    # ------------------------------------------------------

    followers = int(
        profile.get(
            "followers"
        )
        or 0
    )


    public_repos = int(
        profile.get(
            "public_repos"
        )
        or 0
    )


    activity_score = min(
        100,
        round(
            (
                min(
                    public_repos,
                    15,
                )
                / 15
                * 70
            )
            +
            (
                min(
                    followers,
                    10,
                )
                / 10
                * 30
            )
        ),
    )


    # ------------------------------------------------------
    # OVERALL
    # ------------------------------------------------------

    overall = round(

        profile_score
        * 0.15

        +

        repository_score
        * 0.20

        +

        documentation_score
        * 0.20

        +

        technology_score
        * 0.15

        +

        project_quality_score
        * 0.15

        +

        activity_score
        * 0.15

    )


    overall = max(
        0,
        min(
            100,
            overall,
        ),
    )


    return {
        "overall":
            overall,

        "profile":
            profile_score,

        "repositories":
            repository_score,

        "documentation":
            documentation_score,

        "technologies":
            technology_score,

        "quality":
            project_quality_score,

        "activity":
            activity_score,
    }


# ==========================================================
# STRENGTHS AND RECOMMENDATIONS
# ==========================================================

def build_github_recommendations(
    profile,
    repositories,
    quality,
    languages,
    scores,
):

    strengths = []

    improvements = []


    # ------------------------------------------------------
    # PROFILE
    # ------------------------------------------------------

    if scores[
        "profile"
    ] >= 70:

        strengths.append(
            "Your GitHub profile contains good professional information."
        )

    else:

        improvements.append(
            "Complete your GitHub name, bio, location and portfolio/website information."
        )


    # ------------------------------------------------------
    # REPOSITORIES
    # ------------------------------------------------------

    if len(
        repositories
    ) >= 5:

        strengths.append(
            "You have a useful number of public portfolio repositories."
        )

    else:

        improvements.append(
            "Add at least 4–6 meaningful public repositories demonstrating your strongest skills."
        )


    # ------------------------------------------------------
    # README
    # ------------------------------------------------------

    reviewed_count = min(
        len(
            repositories
        ),
        15,
    )


    if (
        reviewed_count
        and quality[
            "readme_count"
        ]
        >= max(
            1,
            reviewed_count
            // 2,
        )
    ):

        strengths.append(
            "Several repositories contain README documentation."
        )

    else:

        improvements.append(
            "Add professional README files explaining problem statement, features, setup, technology stack and screenshots."
        )


    # ------------------------------------------------------
    # DESCRIPTION
    # ------------------------------------------------------

    if (
        repositories
        and quality[
            "description_count"
        ]
        / len(
            repositories
        )
        >= 0.6
    ):

        strengths.append(
            "Most repositories contain descriptions."
        )

    else:

        improvements.append(
            "Add short, meaningful descriptions to every important repository."
        )


    # ------------------------------------------------------
    # TECHNOLOGIES
    # ------------------------------------------------------

    if len(
        languages
    ) >= 3:

        strengths.append(
            "Your repositories demonstrate multiple programming technologies."
        )

    else:

        improvements.append(
            "Show stronger technical breadth through projects using technologies relevant to your target role."
        )


    # ------------------------------------------------------
    # PROJECT QUALITY
    # ------------------------------------------------------

    if scores[
        "quality"
    ] >= 65:

        strengths.append(
            "Your repository metadata indicates good portfolio quality."
        )

    else:

        improvements.append(
            "Improve repository topics, descriptions, documentation and project presentation."
        )


    # ------------------------------------------------------
    # PINNING
    # ------------------------------------------------------

    improvements.append(
        "Pin your 4–6 strongest projects on your GitHub profile so recruiters can find them immediately."
    )


    improvements.append(
        "For placement projects, include screenshots, architecture, installation steps, features and demo links in README files."
    )


    return strengths, improvements


# ==========================================================
# COMPLETE REVIEW
# ==========================================================

def review_github_profile(
    github_url,
):

    username = extract_github_username(
        github_url
    )


    if not username:

        return {
            "success": False,
            "error": (
                "Enter a valid GitHub profile URL, for example: "
                "https://github.com/username"
            ),
        }


    # ------------------------------------------------------
    # PROFILE
    # ------------------------------------------------------

    profile_result = get_github_profile(
        username
    )


    if not profile_result[
        "success"
    ]:

        return {
            "success": False,
            "error": profile_result[
                "error"
            ],
        }


    profile = profile_result[
        "data"
    ]


    # ------------------------------------------------------
    # REPOSITORIES
    # ------------------------------------------------------

    repository_result = (
        get_github_repositories(
            username
        )
    )


    if not repository_result[
        "success"
    ]:

        return {
            "success": False,
            "error": repository_result[
                "error"
            ],
        }


    repositories = repository_result[
        "data"
    ]


    # ------------------------------------------------------
    # ANALYSIS
    # ------------------------------------------------------

    languages = (
        get_language_summary(
            repositories
        )
    )


    quality = (
        analyze_repository_quality(
            username,
            repositories,
        )
    )


    scores = (
        calculate_github_scores(
            profile,
            repositories,
            quality,
            languages,
        )
    )


    strengths, improvements = (
        build_github_recommendations(
            profile,
            repositories,
            quality,
            languages,
            scores,
        )
    )


    return {
        "success":
            True,

        "error":
            "",

        "username":
            username,

        "profile":
            profile,

        "repositories":
            repositories,

        "repository_details":
            quality[
                "portfolio_repositories"
            ],

        "languages":
            languages,

        "quality":
            quality,

        "scores":
            scores,

        "strengths":
            strengths,

        "improvements":
            improvements,
    }