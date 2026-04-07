import cv2
import os

# -------- ORB FEATURE MATCHING --------
def compare_images(img1_path, img2_path):
    
    img1 = cv2.imread(img1_path, 0)
    img2 = cv2.imread(img2_path, 0)

    if img1 is None or img2 is None:
        return 0

    # Initialize ORB
    orb = cv2.ORB_create()

    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    if des1 is None or des2 is None:
        return 0

    # Matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = bf.match(des1, des2)

    # Sort matches
    matches = sorted(matches, key=lambda x: x.distance)

    # Take good matches
    good_matches = matches[:50]

    return len(good_matches)


# -------- MAIN TEMPLATE MATCH FUNCTION --------
def verify_template(uploaded_image_path):
    
    reference_folder = "backend/database/pan"

    best_score = 0

    for file in os.listdir(reference_folder):

    # Skip non-image files
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        ref_path = os.path.join(reference_folder, file)

        score = compare_images(uploaded_image_path, ref_path)

        ref_path = os.path.join(reference_folder, file)

        if score > best_score:
            best_score = score

    # Decision threshold
    if best_score > 20:
        return {
            "status": "PASSED",
            "reason": "Template structure matches",
            "score": best_score
        }
    else:
        return {
            "status": "FAILED",
            "reason": "Template mismatch (possible tampering)",
            "score": best_score
        }