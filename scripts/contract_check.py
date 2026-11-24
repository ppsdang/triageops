"""Gate 1 check: the contract accepts good data and rejects bad data."""
from pydantic import ValidationError

from app.models import ComplaintIn, TriageResult

good_ai = {"category": "payments", "priority": 4, "team": "payments"}
bad_ai = {"category": "payment", "priority": "High", "team": "payment team"}

print("Good AI answer  ->", TriageResult.model_validate(good_ai))

for name, model, data in [
    ("Bad AI answer  ", TriageResult, bad_ai),
    ("Bad request    ", ComplaintIn, {"complaint": "hi", "coupon": "FREE100"}),
]:
    try:
        model.model_validate(data)
    except ValidationError as error:
        print(f"{name} -> REJECTED, {error.error_count()} problems:")
        for problem in error.errors():
            print("      ", problem["loc"], "-", problem["msg"])
