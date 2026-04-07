import cv2
import os
import numpy as np

# Load face cascade
face_cascade = cv2.CascadeClassifier("backend/models/haarcascade_frontalface_default.xml")


# -------- FACE EXTRACTION --------
def extract_face(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return None

    # Take first detected face
    (x, y, w, h) = faces[0]
    face = gray[y:y+h, x:x+w]

    # Resize for comparison
    face = cv2.resize(face, (100, 100))

    return face


# -------- FACE COMPARISON --------
def compare_faces(face1, face2):
    if face1 is None or face2 is None:
        return 0

    # Difference
    diff = cv2.absdiff(face1, face2)

    score = np.sum(diff)

    # Convert to similarity (lower diff = better)
    similarity = max(0, 100 - (score / 1000))

    return float(similarity)


# -------- MAIN FUNCTION --------
def verify_face(uploaded_image_path, matched_record):

    reference_folder = "backend/database/pan/real"
    reference_image_path = os.path.join(reference_folder, matched_record["image"])

    face1 = extract_face(uploaded_image_path)
    face2 = extract_face(reference_image_path)

    score = compare_faces(face1, face2)

    if score > 60:
        return {
            "status": "PASSED",
            "reason": "Face matches with official record",
            "score": score
        }
    else:
        return {
            "status": "FAILED",
            "reason": "Face does not match",
            "score": score
        }