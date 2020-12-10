import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "utdseniordesignteam1060@gmail.com"
sender_email_password = "OUR_EMAIL_PASSWORD"

recipient_email = "utdseniordesignteam1060@gmail.com"


def send_alert_email_to_user(image):
    message_root = MIMEMultipart("related")
    message_root["Subject"] = "Security Notification"
    message_root["From"] = sender_email
    message_root["To"] = recipient_email
    message_root.preamble = "Raspberry Pi Security Camera Notification"

    message_alternative = MIMEMultipart("alternative")
    message_root.attach(message_alternative)
    message_text = MIMEText("Security camera detected a body")
    message_alternative.attach(message_text)

    message_text = MIMEText('<img src="cid:image1">', "html")
    message_alternative.attach(message_text)

    message_image = MIMEImage(image)
    message_image.add_header("Content-ID", "<image1>")
    message_root.attach(message_image)

    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(sender_email, sender_email_password)
    smtp.sendmail(sender_email, recipient_email, message_root.as_string())
    smtp.quit()
