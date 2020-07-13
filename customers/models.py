import uuid
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

# Create your models here.


class Customer(models.Model):
    # Customer Model
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(_("company name"), max_length=50)
    logo = models.ImageField(upload_to='logos/', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("customer_detail", args=[str(self.id)])
