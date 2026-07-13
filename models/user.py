"""User model for the test API."""
from dataclasses import dataclass, field
from utils.validators import validate_email, validate_name

_id_counter = 0


def _next_id():
    global _id_counter
    _id_counter += 1
    return _id_counter


@dataclass
class User:
    name: str
    email: str
    id: int = field(default_factory=_next_id)

    def validate(self):
        """Return error string or None if valid."""
        err = validate_name(self.name)
        if err:
            return err
        # BUG: validate_email("") returns None (no error) — empty email is accepted
        # KNOWN_CORRECT: validate_email should return an error for empty strings.
        err = validate_email(self.email)
        if err:
            return err
        return None


class UserStore:
    def __init__(self):
        self._store = {}

    def add(self, user: User):
        self._store[user.id] = user

    def get(self, user_id: int):
        return self._store.get(user_id)

    def all(self):
        return list(self._store.values())
