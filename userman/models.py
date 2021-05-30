# Create your models here.
from django.utils.translation import ugettext_lazy as _
import uuid

from django.contrib.auth.models import User
from django.db import models


from utils.models import BaseUUIDModel


class ApiKey(BaseUUIDModel):

    api_key = models.CharField(
        max_length=32, default=uuid.uuid4, unique=True,
        null=True, blank=True)

    user = models.ForeignKey(User, related_name='api_keys', on_delete=models.PROTECT)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this API key should be treated as active.')
                                    )

    def __str__(self):
        return f"{self.user}:{self.id}"
