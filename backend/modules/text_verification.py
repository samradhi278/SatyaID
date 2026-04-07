import cv2
import pytesseract
import json
import re
from rapidfuzz import fuzz

# 🔧 Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -------- STEP 1: OCR TEXT EXTRACTION --------
def extract_text(image_path):
    img = cv2.imread(image_path)
    
    if img is None:
        return ""

    # Resize (important for small text)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    # Threshold
    _, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # OCR
    text = pytesseract.image_to_string(gray, config='--psm 6')

    return text.lower()


# -------- STEP 2: EXTRACT PAN DETAILS --------
def extract_pan_details(text):
    
    pan = re.findall(r'[A-Z]{5}[0-9]{4}[A-Z]', text.upper())
    dob = re.findall(r'\d{2}/\d{2}/\d{4}', text)

    return {
        "pan": pan[0] if pan else None,
        "dob": dob[0] if dob else None,
        "raw_text": text
    }


# -------- STEP 3: MATCH WITH DATABASE --------
def match_with_database(extracted_data):
    
    with open("backend/database/pan/pan_data.json", "r") as f:
        database = json.load(f)

    best_match = None
    best_score = 0

    for record in database:
        
        score = 0

        # ✅ PAN match (strongest)
        if extracted_data["pan"] == record["pan"]:
            score += 70

        # ✅ DOB match (only if detected)
        if extracted_data["dob"] is not None:
            if extracted_data["dob"] == record["dob"]:
                score += 20

        # ✅ Name similarity (soft match)
        name_score = fuzz.partial_ratio(extracted_data["raw_text"], record["name"])
        score += (name_score * 0.1)

        if score > best_score:
            best_score = score
            best_match = record

    return best_match, best_score


# -------- FINAL TEXT VERIFICATION FUNCTION --------
def verify_text(image_path):
    
    text = extract_text(image_path)
    extracted_data = extract_pan_details(text)

    # 🔍 DEBUG
    print("----- OCR DEBUG -----")
    print("Extracted PAN:", extracted_data["pan"])
    print("Extracted DOB:", extracted_data["dob"])
    print("Raw Text:\n", extracted_data["raw_text"])
    print("----------------------")

    # ✅ Get best match FIRST
    best_match, score = match_with_database(extracted_data)

    result = {}

    # ❗ PAN not detected
    if extracted_data["pan"] is None:
        result["status"] = "FAILED"
        result["reason"] = "PAN not detected (OCR issue)"

    # ❗ No match in database
    elif best_match is None:
        result["status"] = "FAILED"
        result["reason"] = "No matching PAN found in database"

    # ❗ DOB mismatch (only if OCR detected DOB)
    elif extracted_data["dob"] is not None and extracted_data["dob"] != best_match["dob"]:
        result["status"] = "FAILED"
        result["reason"] = "DOB does not match official record"

    # ❗ Low confidence
    elif score < 60:
        result["status"] = "FAILED"
        result["reason"] = "Low text similarity"

    # ✅ PASS
    else:
        result["status"] = "PASSED"
        result["reason"] = "Text verified successfully"

    result["score"] = score
    result["matched_record"] = best_match

    return result