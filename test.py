import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Cấu hình thông tin máy chủ SMTP
smtp_host = 'ns.name.vn'
smtp_port = 587
smtp_user = 'noreply@ns.name.vn'
smtp_password = 'CBNZkaVns9ECv8S'

# Tạo email thử nghiệm
msg = MIMEMultipart()
msg['From'] = smtp_user
msg['To'] = 'vuthaind@gmail.com'
msg['Subject'] = 'Test Email'
body = 'This is a test email to check SMTP configuration.'
msg.attach(MIMEText(body, 'plain'))

try:
    # Tạo kết nối đến máy chủ SMTP
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()  # Bật mã hóa TLS
    server.login(smtp_user, smtp_password)  # Đăng nhập
    server.sendmail(smtp_user, 'vuthaind@gmail.com', msg.as_string())  # Gửi email
    print('Email sent successfully')
except Exception as e:
    print(f'Error: {e}')
finally:
    server.quit()
