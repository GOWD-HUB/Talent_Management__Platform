from pathlib import Path


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================================
# DATABASE
# ==========================================================

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "talentsphere.db"


# ==========================================================
# UPLOADS
# ==========================================================

UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

LINKEDIN_PDF_DIR = UPLOADS_DIR / "linkedin_profiles"
LINKEDIN_PDF_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# ASSETS
# ==========================================================

ASSETS_DIR = BASE_DIR / "assets"
ASSETS_DIR.mkdir(
    parents=True,
    exist_ok=True
)