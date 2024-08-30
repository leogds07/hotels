#IMPORTS
from handle_password import load_key, decrypt_message
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

def send_emails(sender, receivers, subject, message, encrypted_password):
    # Decrypt password
    key = load_key()
    pwd = decrypt_message(encrypted_password, key)

    # Start server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # TLS = Transport Layer Security

    # Try to log in
    try:
        server.login(sender, pwd)
        print('Logged in...')
    except smtplib.SMTPAuthenticationError:
        sys.exit('Unable to sign in')

    i = 1  # To keep track of the index

    for receiver in receivers:
        # Create MIMEText object
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject

        # Attach the message body with UTF-8 encoding
        msg.attach(MIMEText(message, 'plain', 'utf-8'))

        try:
            # Send the email
            server.sendmail(sender, receiver, msg.as_string())
            print(f'E-mail n.{i} sent!')
            i += 1

            #wait for 3 secs
            time.sleep(3)

        except smtplib.SMTPException as e:
            print(f"Failed to send email to {receiver}: {str(e)}")

    # Close the server connection
    server.quit()

    #all completed successfully
    print('Process Completed!')