import qrcode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import json
from dotenv import load_dotenv
import os
from typing import Dict, Any

load_dotenv()

# Email configuration
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def generate_qr_code(data: Dict[str, Any]) -> bytes:
    """Generate a QR code from the given data."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(data))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def send_email(to_email: str, subject: str, body: str, qr_data: Dict[str, Any]):
    """Send an email with QR code attachment."""
    if not all([EMAIL_USERNAME, EMAIL_PASSWORD]):
        raise ValueError("Email credentials not configured")
    
    # Create message
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject
    
    # Add body
    msg.attach(MIMEText(body, "html"))
    
    # Generate and attach QR code
    qr_img = generate_qr_code(qr_data)
    # TODO: Attach QR code image to email
    
    # Send email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)

def send_registration_confirmation(email: str, event_data: Dict[str, Any], user_data: Dict[str, Any]):
    """Send registration confirmation email with QR code."""
    subject = f"Registration Confirmation - {event_data['title']}"
    body = f"""
    <html>
        <body>
            <h1>Event Registration Confirmation</h1>
            <p>Hello {user_data['name']},</p>
            <p>You have successfully registered for the event:</p>
            <h2>{event_data['title']}</h2>
            <p><strong>Date:</strong> {event_data['date']}</p>
            <p><strong>Time:</strong> {event_data['time']}</p>
            <p><strong>Location:</strong> {event_data['location']}</p>
            <p>Please find your QR code attached to this email. Present this QR code at the event for check-in.</p>
        </body>
    </html>
    """
    
    qr_data = {
        "event_id": str(event_data["_id"]),
        "email": email,
        "name": user_data["name"]
    }
    
    send_email(email, subject, body, qr_data) 