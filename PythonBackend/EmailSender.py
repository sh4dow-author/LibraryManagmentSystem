import smtplib


class Sender:
    def __init__(self, login, password):
        self.login = login
        self.smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        self.smtpObj.starttls()
        self.smtpObj.login(login, password)

    def sendMessage(self, user, message):
        self.smtpObj.sendmail(self.login, user, message)

    def __del__(self):
        self.smtpObj.quit()
