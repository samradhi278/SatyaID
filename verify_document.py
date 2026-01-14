def verify_document(user_image_path):
    text = extract_text(user_image_path)
    doc_type = detect_document_type(text)

    if doc_type == "unknown":
        return "Invalid or unsupported document"

    folder = f"dataset/{doc_type}"
    max_score = 0

    for file in os.listdir(folder):
        db_img = os.path.join(folder, file)
        score = match_images(user_image_path, db_img)
        max_score = max(max_score, score)

    if max_score > 40:
        return f"{doc_type.upper()} card verified"
    else:
        return f"{doc_type.upper()} card not verified"
