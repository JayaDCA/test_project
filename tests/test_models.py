"""Tests for models and validators."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.user import User
from models.product import Product
from utils.validators import validate_email, validate_name


def test_validate_name_ok():
    assert validate_name("Alice") is None


def test_validate_name_empty():
    assert validate_name("") is not None


def test_validate_name_short():
    assert validate_name("A") is not None


# FAILS: empty email passes validation due to the regex bug
def test_validate_email_empty():
    result = validate_email("")
    assert result is not None, "empty email should be invalid"  # BUG: currently None


def test_validate_email_valid():
    assert validate_email("alice@example.com") is None


def test_validate_email_no_at():
    assert validate_email("notanemail") is not None


def test_user_validate_ok():
    u = User(name="Alice", email="alice@example.com")
    assert u.validate() is None


def test_user_validate_bad_email():
    u = User(name="Alice", email="notvalid")
    assert u.validate() is not None


def test_product_validate_ok():
    p = Product(name="Widget", price=9.99)
    assert p.validate() is None


def test_product_validate_negative_price():
    p = Product(name="Widget", price=-1)
    assert p.validate() is not None
