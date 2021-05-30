from django.core.mail import EmailMessage


class Email:

    @staticmethod
    def send_email(data):
        email = EmailMessage(to=[data['email']], subject=data['subject'],
                             body=data['body'])
        email.send()
