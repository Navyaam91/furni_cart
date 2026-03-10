import re

def validate_password(password):
    """
    Validates a password based on specific criteria:
    - Minimum length of 6 characters.
    - At least one letter (uppercase or lowercase).
    - At least one number.
    - At least one special character.
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."
    
    return True, ""
