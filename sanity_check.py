import os
import sys

BAD_KEYWORDS = [
    "gpt-40",
    "gpt -40",
    "gpt40",
    "utils",
    "client.chat.completions",
]

ALLOWED_MODEL = "gpt-4o-mini"

errors = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

                for bad in BAD_KEYWORDS:
                    if bad in content:
                        errors.append(f"❌ FOUND '{bad}' in {path}")

                if "model=" in content and ALLOWED_MODEL not in content:
                    errors.append(f"⚠️ MODEL CHECK {path} → not '{ALLOWED_MODEL}'")

# Report
if errors:
    print("\n🚨 SANITY CHECK FAILED\n")
    for e in errors:
        print(e)
    sys.exit(1)
else:
    print("\n✅ SANITY CHECK PASSED")
    print("✔ No utils")
    print("✔ Correct model")
    print("✔ Safe to deploy\n")
