from rest_framework.exceptions import ValidationError
from django.core.mail import EmailMessage
import threading
import phonenumbers






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
        





    #  PHONE


def phone_checker(p_number):
    if not(p_number and isinstance(p_number,str) and p_number.isdigit()):
        raise ValidationError("Your phone number isn't valid")
    

def phone_parser(p_number, c_code=None):
    try:
        phone_checker(p_number)
        p_number="+"+p_number
        return phonenumbers.parse(p_number, c_code)
    
    except Exception as e:
        return ValidationError("Your phone isn't valid")