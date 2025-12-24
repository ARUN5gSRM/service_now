from django.shortcuts import render
from django.http import HttpResponse
from .models import Ticket
from .utils import send_agent_notification

def home(request):
    return HttpResponse("Agent Mail System is running")


def agent_form(request):
    if request.method == "POST":
        user_email = request.POST.get("user_email")
        agent_name = request.POST.get("agent_name")
        status = request.POST.get("status")
        comment = request.POST.get("comment")

        print("FORM DATA:")
        print(user_email, agent_name, status, comment)

        ticket = Ticket.objects.create(
            user_email=user_email,
            agent_name=agent_name,
            status=status,
            comment=comment
        )

        send_agent_notification(ticket)

        return HttpResponse(f"""
        Email sent successfully!<br><br>
        User Email: {user_email}<br>
        Agent Name: {agent_name}<br>
        Status: {status}<br>
        Comment: {comment}
        """)

    return render(request, "agent_form.html")
