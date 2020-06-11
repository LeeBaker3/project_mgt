import uuid
from django.db import models
from django.urls import reverse

# Create your models here.


class Project(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    project_name = models.CharField(max_length=200)
    project_manager = models.CharField(max_length=200)
    project_number = models.CharField(max_length=20)

    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.id)])
