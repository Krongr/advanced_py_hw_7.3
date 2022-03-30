import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class GmailClient():
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    imap_server = 'imap.gmail.com'

    def __init__(self, login, password):
        self.login = login
        self.password = password
 
    def send_email(self, recipients, subject, message_body):
        email = MIMEMultipart()
        email['From'] = self.login
        email['To'] = ', '.join(recipients)
        email['Subject'] = subject
        email.attach(MIMEText(message_body))

        session = smtplib.SMTP(self.smtp_server, self.smtp_port)
        # Identify ourselves to smtp gmail client
        session.ehlo()
        # Secure our email with tls encryption
        session.starttls()
        # Re-identify ourselves as an encrypted connection
        session.ehlo()
        session.login(self.login, self.password)
        result = session.sendmail(email['From'], email['To'], email.as_string())
        session.quit()
        return result

    def recieve_email(self, mailbox, header=None):
        session = imaplib.IMAP4_SSL(self.imap_server)
        session.login(self.login, self.password)
        session.list()
        session.select(mailbox)
        criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
        result, data = session.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = session.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_string(raw_email)
        session.logout()
        return email_message



if __name__ == "__main__":
    gmail_user = GmailClient('login@gmail.com', 'qwerty')
    gmail_user.send_email(
        ['vasya@email.com', 'petya@email.com'],
        'Subject',
        'Message'
    )

    gmail_user.recieve_email('inbox')
