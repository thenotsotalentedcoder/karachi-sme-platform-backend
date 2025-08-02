"""Debug configuration loading."""

from app.config import settings

print("=== CONFIG DEBUG ===")
print(f"API_V1_STR: '{settings.API_V1_STR}'")
print(f"Type: {type(settings.API_V1_STR)}")
print(f"Length: {len(settings.API_V1_STR)}")
print(f"Repr: {repr(settings.API_V1_STR)}")
print(f"Starts with /: {settings.API_V1_STR.startswith('/')}")
print("===================")