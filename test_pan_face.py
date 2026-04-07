# test_face.py
from backend.modules.face_matching import verify_face

image_path = "backend/database/pan/real/pan1.jpg"

print(verify_face(image_path))