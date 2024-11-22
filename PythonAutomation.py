import os
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.blocking import BlockingScheduler

# Configuration
LOG_FILE = "/var/log/system.log"  # Path to the log file
ERROR_KEYWORDS = ["ERROR", "CRITICAL", "FAILURE"]
ADMIN_EMAIL = "admin@example.com"
SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "your_email@example.com"
SMTP_PASS = "your_password"

def send_alert(email_subject, email_body):
    """Send an alert email to the administrator."""
    msg = MIMEText(email_body)
    msg['Subject'] = email_subject
    msg['From'] = SMTP_USER
    msg['To'] = ADMIN_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, ADMIN_EMAIL, msg.as_string())
        print(f"Alert sent to {ADMIN_EMAIL}")
    except Exception as e:
        print(f"Failed to send alert: {e}")

def monitor_logs():
    """Scan logs for error keywords and send alerts if found."""
    if not os.path.exists(LOG_FILE):
        print(f"Log file not found: {LOG_FILE}")
        return

    try:
        with open(LOG_FILE, 'r') as file:
            lines = file.readlines()

        for line in lines:
            if any(keyword in line for keyword in ERROR_KEYWORDS):
                print(f"Incident detected: {line.strip()}")
                send_alert(
                    "Critical Incident Detected",
                    f"The following incident was detected:\n\n{line.strip()}"
                )
    except Exception as e:
        print(f"Error reading log file: {e}")

# Scheduler setup
scheduler = BlockingScheduler()

# Schedule the monitoring task every 5 minutes
scheduler.add_job(monitor_logs, 'interval', minutes=5)

if __name__ == "__main__":
    print("Starting scheduled log monitoring...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Monitoring stopped.")
