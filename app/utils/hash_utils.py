import hashlib
from pathlib import Path

def calculate_sha256(file_path):
    """Calculate SHA-256 hash for for a file."""
    path = Path(file_path)

    if not path.exists() or not path.is_file():
        return ""
    
    try:
        sha256_hash = hashlib.sha256()

        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(8192), b""):
                sha256_hash.update(chunk)

        return sha256_hash.hexdigest()
    
    except (OSError, PermissionError):
        return ""