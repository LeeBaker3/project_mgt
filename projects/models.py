import uuid
from django.db import models
from django.urls import reverse
from customers.models import Customer

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
    customer = models.ForeignKey(
        Customer, related_name='customer', null=True, on_delete=models.SET('deleted'))
    #logo = models.ImageField(upload_to='logos/', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['id'], name='id_index')
        ]

    def __str__(self):
        return self.project_name

    def get_absolute_url(self):
        return reverse("project_detail", args=[str(self.id)])


class Deliverable(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='deliverables'
    )
    deliverable_name = models.CharField(max_length=255)
    deliverable_description = models.TextField(max_length=1000)

    def __str__(self):
        return self.deliverable_name

    def get_absolute_url(self):
        return reverse("deliverable_detail", args=[str(self.id)])
