from backend.modules.text_verification import verify_text

# Use one of your REAL PAN images
image_path = "backend/database/pan/real/pan1.jpg"

result = verify_text(image_path)

print("----- RESULT -----")
print("Status:", result["status"])
print("Reason:", result["reason"])
print("Score:", result["score"])
print("Matched Record:", result["matched_record"])