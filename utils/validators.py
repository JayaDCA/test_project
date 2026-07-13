"""Input validators for the test API."""
import re


# BUG: this regex requires at least one char before @, but allows empty local part
# via the outer condition — and critically does NOT reject empty string at all.
# KNOWN_CORRECT: should explicitly check `if not email or not email.strip()`
# first, then use regex r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
_EMAIL_RE = re.compile(r"[^@]+@[^@]+")   # BUG: too permissive, e.g. "@" passes


def validate_email(email: str):
    """Return True if the email is valid, otherwise False.

    Validation rules (kept minimal and strict):
    - Exactly one '@'.
    - No whitespace anywhere (leading/trailing or internal).
    - Local-part length 1-64, does not start/end with '.', and has no consecutive dots.
    - Domain can be an IP-literal ([...]) validated via ipaddress, or a dot-separated
      name with at least one dot and labels that are 1-63 chars, letters/digits/hyphen,
      not starting/ending with hyphen, no underscores; final TLD label at least 2 chars.
    """
    # Must be a string
    if not isinstance(email, str):
        return False

    # Reject any whitespace (including leading/trailing) — do not auto-trim
    if re.search(r"\s", email):
        return False

    # Require exactly one '@'
    if email.count("@") != 1:
        return False

    local, domain = email.split("@", 1)

    # Local-part checks
    if len(local) < 1 or len(local) > 64:
        return False
    # must not start or end with dot
    if local[0] == "." or local[-1] == ".":
        return False
    # no consecutive dots
    if ".." in local:
        return False
    # allowed characters in local (RFC-inspired subset)
    if not re.fullmatch(r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+", local):
        return False

    # Domain checks
    # IP-literal: [IPv6:...] or [x.x.x.x]
    if domain.startswith("[") and domain.endswith("]"):
        inner = domain[1:-1]
        # allow optional IPv6: prefix
        if inner.lower().startswith("ipv6:"):
            ip_text = inner[5:]
        else:
            ip_text = inner
        try:
            # validate IP (IPv4 or IPv6)
            import ipaddress
            ipaddress.ip_address(ip_text)
        except Exception:
            return False
        return True

    # Regular domain name: require at least one dot (no single-label domains)
    if "." not in domain:
        return False
    # no leading/trailing dot
    if domain[0] == "." or domain[-1] == ".":
        return False
    # no consecutive dots
    if ".." in domain:
        return False

    labels = domain.split(".")
    # TLD must be at least 2 chars
    if len(labels[-1]) < 2:
        return False

    label_re = re.compile(r"^[A-Za-z0-9-]{1,63}$")
    for label in labels:
        # label length
        if len(label) < 1 or len(label) > 63:
            return False
        # allowed chars and no underscores
        if not label_re.fullmatch(label):
            return False
        # label cannot start or end with hyphen
        if label[0] == "-" or label[-1] == "-":
            return False

    return True


def validate_name(name: str):
    """Return error string or None if valid."""
    if not name or not name.strip():
        return "name is required"
    if len(name.strip()) < 2:
        return "name must be at least 2 characters"
    if len(name) > 100:
        return "name must be at most 100 characters"
    return None


# BUG: accepts negative prices and non-numeric strings that happen to parse via
# float() (e.g. "nan", "inf") — returns None (valid) for both.
# KNOWN_CORRECT: reject non-finite floats and require price >= 0 explicitly.
def validate_price(price):
    """Return error string or None if the price is valid."""
    try:
        price = float(price)
    except (TypeError, ValueError):
        return "price must be a number"
    return None
