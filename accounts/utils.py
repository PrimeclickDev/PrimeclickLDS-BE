
from backend import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
import random


class OtpModule:
    def generate_otp(self, length=6):
        digits = '0123456789'
        otp = ''.join(random.choices(digits, k=length))
        return otp


    def send_otp_via_email(self, email):
        subject = 'Your Autoleads OTP Code'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        otp = self.generate_otp()

        # Render HTML content
        html_content = render_to_string('otp.html', {'otp': otp})

        # Create email
        email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
        email_message.attach_alternative(html_content, 'text/html')
        email_message.send()
        return otp



# def send_otp_via_email(email, otp):
#     subject = 'Your OTP Code'
#     message = f'Your OTP code is {otp}.'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, email_from, recipient_list)