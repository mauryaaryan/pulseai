import re

def validate_audio_file(file_path: str) -> tuple[bool, str]:
    """Check if the provided file is valid."""
    if not file_path:
        return False, "No file path provided."
    if not file_path.endswith('.wav'):
        return False, "Only WAV files are supported."
    return True, ""

def sanitize_string(text: str) -> str:
    """Basic SQL-injection defense string sanitizer."""
    return re.sub(r'[;\'\"]', '', text)
