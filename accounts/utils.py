
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


    def send_otp_via_email(self, email, first_name):
        subject = 'Your Autoleads OTP Code'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        otp = self.generate_otp()

        # Render HTML content
        html_content = render_to_string('otp.html', {'otp': otp, 'first_name': first_name})

        # Create email
        email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
        email_message.attach_alternative(html_content, 'text/html')
        email_message.send()
        return otp


def send_invite_lint_email(email, link: str, access_code: str, campaign_name: str):
    subject = "View Campaign Access"
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    html_content = render_to_string('view_email.html',
                                    {'link': link, 'access_code': access_code, 'campaign_name': campaign_name})
    email_message = EmailMultiAlternatives(subject, '', from_email, to_email)
    email_message.attach_alternative(html_content, 'text/html')
    email_message.send()

