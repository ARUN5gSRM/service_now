from django.db import models

class Ticket(models.Model):
    user_email = models.EmailField()
    agent_name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agent_name} -> {self.user_email}"
