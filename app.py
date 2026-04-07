from flask import Flask, jsonify, render_template, request, redirect, session, url_for, flash
from flask_mail import Mail, Message
import pytesseract
import random
from flask_cors import CORS

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
CORS(app)
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
accepted_officials = []

# User Details Page
@app.route('/user-details', methods=['GET', 'POST'])
def user_details():
    if request.method == 'POST':
        # Later: save user details
        return redirect(url_for('dashboard'))
    return render_template('user_details.html')


# Official Details Page
@app.route('/official-details', methods=['GET', 'POST']) #**********
def official_details():
    if request.method == 'POST':
        # Later: save official details
        return redirect(url_for('dashboard'))

    return render_template('official_details.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



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
                flash("User not found. Please register first.", "error")
                return redirect(url_for('login'))#********

            if user["status"] != "ACCEPTED":#******
                flash("Your account is pending verification.", "error")#****
                return redirect(url_for('login'))#********

            return redirect(url_for('dashboard'))

        else:
            return "Invalid role selected."

    return render_template('login.html')

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

@app.route('/official_dashboard')
def official_dashboard():
    pending_users = [u for u in users_db if u["status"] == "PENDING"]
    accepted_users = [u for u in users_db if u["status"] == "ACCEPTED"]

    return render_template(
        'official_dashboard.html',
        pending_users=pending_users,
        accepted_users=accepted_users
    )


@app.route('/accept-user/<int:index>', methods=['POST'])
def accept_user(index):
    users_db[index]["status"] = "ACCEPTED"

    login_link = url_for('login', _external=True)

    send_user_email(
        email=users_db[index]["email"],
        login_link=login_link,
        accepted=True
    )

    flash("Accepted and email sent!")#**************
    return redirect(url_for('official_dashboard'))

@app.route('/reject-user/<int:index>', methods=['POST'])
def reject_user(index):
    users_db[index]["status"] = "REJECTED"

    send_user_email(
        email=users_db[index]["email"],
        login_link=None,
        accepted=False
    )

    flash("Rejected")
    return redirect(url_for('official_dashboard'))

def send_user_email(email, login_link=None, accepted=True):
    msg = Message(
        subject="SatyaID User Verification",
        recipients=[email]
    )

    if accepted:
        msg.html = f"""
        <p>Hello,</p>
        <p>Your registration has been <b>accepted</b>.</p>
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

        return redirect(url_for("official_login"))#********************

    return render_template("official_register.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html", officials=officials_db)

# @app.route('/logout')
# def logout():
#     return redirect(url_for('login'))

@app.route("/accept/<int:index>")
def accept_official(index):
    if 0 <= index < len(officials_db):
        officials_db[index]["status"] = "ACCEPTED"

        # Send email with login link
        login_link = url_for('official_login', _external=True)  # generates full URL to /login
        send_approval_email(
            email=officials_db[index]["email"],
            login_link=login_link
        )

        flash(f"{officials_db[index]['name']} accepted and email sent!")
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


def send_approval_email(email, login_link):
    msg = Message(
        "SatyaID Approval",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )

    msg.html = f"""
    <p>Hello,</p>
    <p>Your registration has been accepted. Click the link below to login:</p>
    <a href="{login_link}">Login Here</a>
    <p>Thank you,<br>Admin Team</p>
    """

    mail.send(msg)

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route("/official_login", methods=["GET", "POST"])
def official_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        official = next(
            (o for o in officials_db if o["email"] == email and o["password"] == password),
            None
        )
#********************************
        if not official:
            flash("Invalid credentials", "error")
            return redirect(url_for("official_login"))

        if official["status"] != "ACCEPTED":
            flash("Your account is not accepted yet.", "warning")
            return redirect(url_for("official_login"))
         
        session["official_email"] = official["email"]

        return redirect(url_for("official_dashboard"))

    return render_template("official_login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('page1'))

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
#*******************LOGOUT LOGIN

#------------------------------------------------------------------------------------------------
# MAin LOGIC
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from backend.modules.text_verification import verify_text
from backend.modules.template_matching import verify_template
from backend.modules.face_matching import verify_face

import os
@app.route("/verify", methods=["POST"])
def verify_document():

    print("/verify API HIT")

    if "file" not in request.files:
        return jsonify({
            "status": "FAILED",
            "reason": "No file uploaded"
        })

    file = request.files["file"]
    print("File received:", file.filename)

    upload_folder = "backend/uploads"
    os.makedirs(upload_folder, exist_ok=True)

    upload_path = os.path.join(upload_folder, "user_upload.jpg")
    file.save(upload_path)

    # STEP 1: TEXT
    text_result = verify_text(upload_path)

    if text_result["status"] == "FAILED":
        return jsonify({
            "status": "FAILED",
            "reason": text_result["reason"]
        })

    # STEP 2: TEMPLATE
    template_result = verify_template(upload_path)

    if template_result["status"] == "FAILED":
        return jsonify({
            "status": "FAILED",
            "reason": template_result["reason"]
        })

    # STEP 3: FACE
    face_result = verify_face(upload_path, text_result["matched_record"])

    if face_result["status"] == "FAILED":
        return jsonify({
            "status": "FAILED",
            "reason": face_result["reason"]
        })

    return jsonify({
        "status": "PASSED",
        "reason": "All verifications passed"
    })



if __name__ == '__main__':
    app.run(debug=True)