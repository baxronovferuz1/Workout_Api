import re
from rest_framework.exceptions import ValidationError



email_regex=re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
phone_regex=re.compile(r"^9\d{12}$")
username_regex=re.compile(f"^[a-zA-Z0-9_.-]+$")


#fullmatch--obyektlari orasidagi moslikni tekshirish uchun ishlatiladi.

def check_email_or_phone(email_or_phone):
    if re.fullmatch(email_regex,email_or_phone):
        email_or_phone="email"
    elif re.fullmatch(phone_regex,email_or_phone):
        email_or_phone="phone"
    else:
        data={
            'success':False,
            'message':"Email or phone number is incorrect"
        }
        raise ValidationError(data)

    return email_or_phone


def check_user_type(user_input):
    if re.fullmatch(email_regex, user_input):
        user_input='email'
    elif re.fullmatch(phone_regex, user_input):
        user_input='phone'
    elif re.fullmatch(username_regex, user_input):
        user_input='username'
    else:
        data={
            "success":False,
            "message":"Your email,username or phone number is incorrect"
        }
        raise ValidationError(data)
    
    
    return user_input