import hashlib


# ==========================================================
# HASH PASSWORD
# ==========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ==========================================================
# VERIFY PASSWORD
# ==========================================================

def verify_password(
    password,
    stored_password,
):

    entered_password_hash = hash_password(
        password
    )

    return entered_password_hash == stored_password