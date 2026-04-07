from backend.modules.template_matching import verify_template

image_path = "backend/database/pan/real/pan1.jpg"

result = verify_template(image_path)

print(result)