import smtplib

class GmailAccount:

    def __init__(self, gmail_user, gmail_password):
        self.server = self.login(gmail_user, gmail_password)


    def login(self, gmail_user, gmail_password):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user , gmail_password)
        except:
            print('ERROR: Something went wrong during login process')

        return server
