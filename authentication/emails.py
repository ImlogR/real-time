from django.core.mail import send_mail
import random
from django.conf import settings
from authentication.models import CustomUser

def send_otp_via_email(email):
    subject= f'Account verification email'
    otp= random.randint(100000, 999999)
    message= f'Your otp is {otp}'
    emai_from= settings.EMAIL_HOST
    send_mail(subject, message, emai_from, [email])
    user_obj= CustomUser.objects.get(email= email)
    user_obj.otp= otp
    user_obj.save()
