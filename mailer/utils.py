from django.core.mail import send_mail
from django.conf import settings

ANALYST_TEAM_EMAILS = [
    'arunayyappanfirst1@gmail.com',
    'arunayyappan987@gmail.com'
]

def send_agent_notification(ticket):
    subject = f"Ticket Status - {ticket.status}"

    message = f"""
Hello,

Your request has been processed.

User Email: {ticket.user_email}
Agent Name: {ticket.agent_name}
Status: {ticket.status}
Comment: {ticket.comment}

Regards,
Support Team
"""

    recipients = [ticket.user_email] + ANALYST_TEAM_EMAILS

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipients,
        fail_silently=False
    )
