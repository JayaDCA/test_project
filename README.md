# CodeBenders Benchmark Test Project

A synthetic Flask REST API used by the CodeBenders token savings benchmark.

## Structure

```
test_project/
├── app.py              # Flask app with 6 routes (2 bugs)
├── models/
│   ├── user.py         # User model (1 bug: empty email accepted)
│   └── product.py      # Product model
├── utils/
│   ├── validators.py   # Input validators (1 bug: regex too permissive)
│   └── helpers.py      # Response formatting, pagination
└── tests/
    ├── test_app.py     # Route tests (3 failing due to bugs)
    └── test_models.py  # Model tests (1 failing due to bug)
```

## Known Bugs

| File | Bug | Correct Fix |
|---|---|---|
| `app.py` POST /users | No input validation → KeyError 500 | Check fields, return 400 |
| `app.py` POST /products | No duplicate check → AssertionError 500 | Check `find_by_name`, return 409 |
| `utils/validators.py` | `validate_email("")` returns None (valid) | Check empty string first |

## Running Tests

```bash
pip install flask pytest
pytest tests/ -v
# Expect: 3 failures (the bugs above)
```
