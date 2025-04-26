import os
import time
import shutil
import smtplib
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

gmail = os.getenv("gmail")
password = os.getenv("password")
gmail_nhan = os.getenv("gmail_nhan")

database = "database/Tue.sqlite3"
backup = "backup"

os.makedirs(backup, exist_ok=True)
def make_backup_filename():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(backup, f"backup_{timestamp}.sqlite3"), timestamp
def send_email(subject, content):
    message = MIMEMultipart()
    message["From"] = gmail
    message["To"] = gmail_nhan
    message["Subject"] = subject
    message.attach(MIMEText(content, "plain"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(gmail, password)
            smtp.send_message(message)
        print("Email đã được gửi thành công.")
    except Exception as error:
        print(f"Lỗi gửi email: {error}")
def perform_backup():
    backup_file, timestamp = make_backup_filename()
    try:
        shutil.copy2(database, backup_file)
        print(f"Backup hoàn tất: {backup_file}")
        send_email(
            subject="Backup Thành Công",
            content=f"Backup đã hoàn thành lúc {timestamp}.\nTên file: {backup_file}"
        )
    except Exception as error:
        print(f"Lỗi backup: {error}")
        send_email(
            subject="Backup Thất Bại",
            content=f"Có lỗi xảy ra khi backup:\n{error}"
        )
perform_backup() # kiểm tra thử ngay lập tức
schedule.every().day.at("00:00").do(perform_backup)
print("Hệ thống backup tự động đã sẵn sàng. Đợi đến 00:00 mỗi ngày.")
while True:
    schedule.run_pending()
    time.sleep(60)
