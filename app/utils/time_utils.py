from datetime import datetime , timezone , timedelta 

def timestamp_to_iso(timestamp):
    """convert a file timestamp to ISO format."""
    try:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
    except (OSError, TypeError, ValueError):
        return ""

def windows_filetime_to_iso(filetime):
    """convert windows FILETIME to ISO format."""   
    try:
        windows_epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
        converted_time = windows_epoch + timedelta(microseconds=filetime / 10)
        return converted_time.isoformat()
    except (OSError, TypeError, ValueError):
        return ""
    
def now_iso():
    """Return the current UTC time in ISO format"""
    return datetime.now(timezone.utc).isoformat()