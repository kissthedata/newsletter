import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

NAVER_ID = os.getenv("NAVER_MAIL_ID")
NAVER_PW = os.getenv("NAVER_MAIL_PW")

def send_email(subject, body, to_email, is_html=False):
    msg = EmailMessage()
    msg['From'] = f"{NAVER_ID}@naver.com"
    msg['To'] = to_email
    msg['Subject'] = subject

    if is_html:
        msg.set_content("HTML을 지원하는 메일 클라이언트에서 확인해주세요.")
        msg.add_alternative(body, subtype='html')
    else:
        msg.set_content(body)

    server = smtplib.SMTP('smtp.naver.com', 587)
    server.starttls()
    server.login(NAVER_ID, NAVER_PW)
    server.send_message(msg)
    server.quit()

    print("메일 발송 완료")
