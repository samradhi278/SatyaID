from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message


app = Flask(__name__)

app.secret_key = 'satyaid_secret_key'   # if not already added

# ---------------- MAIL CONFIG ----------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'satyaid0126@gmail.com'
app.config['MAIL_PASSWORD'] = 'grks audn rwhs grsm'
app.config['MAIL_DEFAULT_SENDER'] = 'satyaid0126@gmail.com'

mail = Mail(app)
# --------------------------------------------

users_db = []

officials_db = []

pending_officials = []
approved_officials = []


# Home / Role Selection Page
#@app.route('/')
#def home():
    #return render_template('page1.html')


# User Details Page
@app.route('/user-details', methods=['GET', 'POST'])
def user_details():
    if request.method == 'POST':
        # Later: save user details
        return redirect(url_for('dashboard'))

    return render_template('user_details.html')


# Official Details Page
@app.route('/official-details', methods=['GET', 'POST'])
def official_details():
    if request.method == 'POST':
        # Later: save official details
        return redirect(url_for('dashboard'))

    return render_template('official_details.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

from flask import Flask, render_template, request, redirect, url_for

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('name').strip().lower()
        role = request.form.get('role').strip().lower()

        # ---------- OFFICIAL LOGIN ----------
        if role == "official":
            official = next(
                (o for o in officials_db if o["email"].lower() == email),
                None
            )

            if not official:
                return "Official not found. Please register first."

            if official["status"] == "PENDING":
                return "Approval pending. Please wait for admin approval."

            if official["status"] == "REJECTED":
                return "Your registration was rejected."

            return redirect(url_for('official_dashboard'))

        # ---------- USER LOGIN ----------
        elif role == "user":
            user = next(
                (u for u in users_db if u["email"].lower() == email),
                None
            )

            if not user:
                return "User not found. Please register first."

            if user["status"] != "APPROVED":
                return "Your account is pending verification."

            return redirect(url_for('dashboard'))

        else:
            return "Invalid role selected."

    return render_template('login.html')

import random

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        application_no = "SATYA" + str(random.randint(10000, 99999))

        users_db.append({
            "name": name,
            "email": email,
            "application_no": application_no,
            "status": "PENDING"
        })

        flash(f"Registration successful! Application No: {application_no}")
        return redirect(url_for('login'))

    return render_template('register.html')


# Dummy user verification storage
verified_users = set()

@app.route('/official-dashboard')
def official_dashboard():
    pending_users = [u for u in users_db if u["status"] == "PENDING"]
    approved_users = [u for u in users_db if u["status"] == "APPROVED"]

    return render_template(
        'official_dashboard.html',
        pending_users=pending_users,
        approved_users=approved_users
    )


@app.route('/approve-user/<int:index>', methods=['POST'])
def approve_user(index):
    users_db[index]["status"] = "APPROVED"

    login_link = url_for('login', _external=True)

    send_user_email(
        email=users_db[index]["email"],
        login_link=login_link,
        approved=True
    )

    flash("Decision made")
    return redirect(url_for('official_dashboard'))


@app.route('/reject-user/<int:index>', methods=['POST'])

@app.route('/reject-user/<int:index>', methods=['POST'])
def reject_user(index):
    users_db[index]["status"] = "REJECTED"

    send_user_email(
        email=users_db[index]["email"],
        login_link=None,
        approved=False
    )

    flash("Decision made")
    return redirect(url_for('official_dashboard'))

def send_user_email(email, login_link=None, approved=True):
    msg = Message(
        subject="SatyaID User Verification",
        recipients=[email]
    )

    if approved:
        msg.html = f"""
        <p>Hello,</p>
        <p>Your registration has been <b>approved</b>.</p>
        <p>You can now login using the link below:</p>
        <a href="{login_link}">Login to SatyaID</a>
        <p>Thank you,<br>SatyaID Team</p>
        """
    else:
        msg.html = """
        <p>Hello,</p>
        <p>Your registration has been <b>rejected</b>.</p>
        <p>Please contact support for more information.</p>
        <p>Thank you,<br>SatyaID Team</p>
        """

    mail.send(msg)



@app.route('/', methods=['GET', 'POST'])
def page1():
    if request.method == 'POST':
        role = request.form.get('role')
        if role == 'USER':
            return redirect(url_for('register'))
        elif role == 'OFFICIAL':
            return redirect(url_for('official_register'))
    return render_template('page1.html')

# Handle role selection
@app.route('/next', methods=['POST']) 
def next_page(): 
    role = request.form.get('role') 
    if role == 'User': 
        return redirect(url_for('register')) 
    elif role == 'Official': 
        return redirect(url_for('official_register')) 
    return redirect(url_for('page1.html'))

@app.route("/official_register", methods=["GET", "POST"])
def official_register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        officials_db.append({
            "name": name,
            "email": email,
            "password": request.form["password"],
            "status": "PENDING"
        })

        return "Registration submitted. Await admin approval."

    return render_template("official_register.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html", officials=officials_db)
@app.route("/approve/<int:index>")
def approve_official(index):
    if 0 <= index < len(officials_db):
        officials_db[index]["status"] = "APPROVED"

        # Send email with login link
        login_link = url_for('official_login', _external=True)  # generates full URL to /login
        send_approval_email(
            email=officials_db[index]["email"],
            login_link=login_link
        )

        flash(f"{officials_db[index]['name']} approved and email sent!")
        return redirect(url_for("admin_dashboard"))
    else:
        flash("Invalid official index!")
        return redirect(url_for("admin_dashboard"))

@app.route("/reject/<int:index>")
def reject_official(index):
    if 0 <= index < len(officials_db):
        officials_db[index]["status"] = "REJECTED"
        flash(f"{officials_db[index]['name']} rejected!")
    else:
        flash("Invalid official index!")

    return redirect(url_for("admin_dashboard"))


from flask_mail import Message
def send_approval_email(email, login_link):
    msg = Message(
        "SatyaID Approval",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )

    msg.html = f"""
    <p>Hello,</p>
    <p>Your registration has been approved. Click the link below to login:</p>
    <a href="{login_link}">Login Here</a>
    <p>Thank you,<br>Admin Team</p>
    """

    mail.send(msg)

# import cv2
# import pytesseract
import os

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# def extract_text(image_path):
#     img = cv2.imread(image_path)
#     if img is None:
#         return ""

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     text = pytesseract.image_to_string(gray)
#     return text.lower()


@app.route("/official-login", methods=["GET", "POST"])
def official_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        official = next(
            (o for o in officials_db if o["email"] == email and o["password"] == password),
            None
        )

        if not official:
            return "Invalid credentials"

        if official["status"] != "APPROVED":
            return "Your account is not approved yet."

        return redirect(url_for("official_dashboard"))

    return render_template("official_login.html")

#------------------------------------------------------------------------------------------------

import cv2
import pytesseract
import os
from PIL import Image
import imagehash


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return ""

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.lower()


#@app.route("/official-login", methods=["GET", "POST"])
#def official_login():
    #if request.method == "POST":
        #email = request.form.get("email")
        #password = request.form.get("password")

        #official = next(
            #(o for o in officials_db if o["email"] == email and o["password"] == password),
            #None
        #)

        #if not official:
            #return "Invalid credentials"

        #if official["status"] != "APPROVED":
            #return "Your account is not approved yet."

        #return redirect(url_for("official_dashboard"))

    #return render_template("official_login.html")

def get_phash(image_path):
    img = Image.open(image_path).convert("RGB")
    return imagehash.phash(img)


def is_real_document(uploaded_image, reference_image):
    uploaded_hash = get_phash(uploaded_image)
    reference_hash = get_phash(reference_image)

    distance = uploaded_hash - reference_hash

    # Threshold: smaller = more similar
    if distance <= 10:
        return True
    return False

@app.route("/verify", methods=["POST"])
def verify_document():
    file = request.files["document"]
    doc_type = request.form.get("doc_type")

    upload_path = "uploads/user_upload.png"
    file.save(upload_path)

    if doc_type == "pan":
        reference = "reference/pan_real.png"
        status = "Verified" if is_real_document(upload_path, reference) else "Rejected"
        doc_name = "PAN Card"

    elif doc_type == "aadhaar":
        reference = "reference/aadhaar_real.png"
        status = "Verified" if is_real_document(upload_path, reference) else "Rejected"
        doc_name = "Aadhaar Card"

    else:
        status = "Rejected"
        doc_name = "Unknown Document"

    report = {
        "doc": doc_name,
        "status": status
    }

    return render_template("dashboard.html", report=report)


if __name__ == '__main__':
    app.run(debug=True)