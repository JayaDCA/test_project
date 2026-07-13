"""Response helpers for the test API."""


def format_response(data, meta=None):
    """Wrap data in a standard envelope."""
    result = {"data": data, "success": True}
    if meta:
        result["meta"] = meta
    return result


def paginate(items, page=1, per_page=10):
    """Return a slice of items with pagination metadata."""
    page = max(1, page)
    per_page = max(1, min(100, per_page))
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "items": items[start:end],
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page,
    }


# BUG: off-by-one — truncates to max_len - 1 visible chars once "..." is appended,
# and doesn't handle max_len <= 3 (produces a negative slice instead of just "...").
# KNOWN_CORRECT: `return text[:max_len - 3] + "..."` guarded by `if max_len <= 3: return "."*max_len`.
def truncate_text(text, max_len=20):
    """Truncate text to max_len characters, appending '...' if cut."""
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


# BUG: mutates the caller's `base` dict in place instead of returning a new merged
# dict — callers that expect merge_dicts to be pure will see their original dict
# silently changed.
# KNOWN_CORRECT: `merged = dict(base); merged.update(override); return merged`.
def merge_dicts(base, override):
    """Merge override into base, returning the merged dict."""
    base.update(override)
    return base


# BUG: raises ZeroDivisionError when b == 0 instead of returning a safe default.
# KNOWN_CORRECT: `if b == 0: return default` before the division.
def safe_divide(a, b, default=0):
    """Divide a by b, returning default if b is zero."""
    return a / b
