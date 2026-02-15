from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        USER = "user", "User"
        ADMIN = "admin", "Admin"
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True,db_index=True,)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER,)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE,)

    def __str__(self):
        return self.get_username()
    

# class FaceEmbedding(models.Model):
#     user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='embeddings')
#     phone_number = models.CharField(max_length=20, blank=True, null=True)       
#     embedding = models.JSONField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Embedding for {self.user.username} ({self.id})"

# class Attendance(models.Model):
#     STATUS_CHOICES = (
#         ('present', 'Present'),
#         ('absent', 'Absent'),
#         ('late', 'Late'),
#     )
#     user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='attendance')
#     date = models.DateField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'date')

#     def __str__(self):
#         return f"{self.user.username} - {self.date} - {self.status}"
