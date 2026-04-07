from backend.modules.face_matching import verify_face

matched_record = {
    "image": "pan1.jpg"
}

result = verify_face("backend/database/pan/real/pan1.jpg", matched_record)

print(result)