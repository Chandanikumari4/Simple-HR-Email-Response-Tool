from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# ==========================================
# EMAIL CONFIGURATION (EDIT THIS)
# ==========================================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"   # Gmail app password


# ==========================================
# EMAIL TEMPLATES
# ==========================================
def get_selection_template(name, position):
    return f"""
Dear {name},

We are pleased to inform you that you have been selected for the position of {position}.

Please reply to this email to confirm your acceptance.

Best regards,
HR Team
"""


def get_rejection_template(name, position):
    return f"""
Dear {name},

Thank you for applying for the position of {position}.

We regret to inform you that we have decided to move forward with other candidates.

Best regards,
HR Team
"""


# ==========================================
# HOME PAGE
# ==========================================
@app.route("/")
def index():
    return render_template("index.html")


# ==========================================
# PREVIEW PAGE
# ==========================================
@app.route("/preview-page", methods=["POST"])
def preview_page():
    name = request.form["name"]
    email = request.form["email"]
    position = request.form["position"]
    status = request.form["status"]

    if status == "Selected":
        message = get_selection_template(name, position)
    else:
        message = get_rejection_template(name, position)

    return render_template(
        "preview.html",
        name=name,
        email=email,
        position=position,
        status=status,
        message=message
    )


# ==========================================
# SEND EMAIL
# ==========================================
@app.route("/send", methods=["POST"])
def send_email():
    data = request.json

    name = data["name"]
    email = data["email"]
    position = data["position"]
    status = data["status"]

    if status == "Selected":
        body = get_selection_template(name, position)
        subject = "Congratulations! You are Selected"
    else:
        body = get_rejection_template(name, position)
        subject = "Application Update"

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({"success": True, "message": "Email sent successfully!"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


# ==========================================
# RUN SERVER
# ==========================================
if __name__ == "__main__":
    app.run(debug=True)