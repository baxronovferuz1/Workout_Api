from rest_framework.exceptions import ValidationError
from django.core.mail import EmailMessage
import threading






class EmailThread(threading.Thread): # elektron pochta muhokamalarini tartibli bo'lishiga yordam beradi

    def __init__(self, email):
        self.email=email
        threading.Thread.__init__(self)


    def run(self):
        self.email.send()




class Email:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data["subject"],
            body=data["body"],
            to=[data["to email"]]

        )
        if data.get("content_type")=="html":
            email.content_subtype="html"
        EmailThread(email).start()
        



