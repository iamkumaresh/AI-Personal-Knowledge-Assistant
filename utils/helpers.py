import datetime

def clean_html(html_raw: str) -> str:
    """
    Strips leading and trailing whitespace from each line and removes blank lines.
    This prevents Markdown parsers from escaping indented lines as code blocks.
    """
    lines = [line.strip() for line in html_raw.split("\n") if line.strip()]
    return "".join(lines)

def format_file_size(size_bytes: int) -> str:
    """Format file size in bytes to a human-readable string (KB/MB)."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def get_greeting() -> str:
    """Return a warm, localized greeting based on the current hour of the day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good Morning"
    elif hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

def truncate_text(text: str, max_chars: int = 40) -> str:
    """Truncate text and append ellipsis if it exceeds the maximum length."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars - 3] + "..."

def format_date(date_str: str) -> str:
    """Parse and format a standard ISO date string into a beautiful readable format."""
    try:
        dt = datetime.datetime.fromisoformat(date_str)
        return dt.strftime("%b %d, %Y - %I:%M %p")
    except Exception:
        return date_str
