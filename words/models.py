from django.db import models
from django.utils.translation import gettext as _


class Folder(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("name"))


class Word(models.Model):
    content = models.CharField(max_length=255, verbose_name=_("content"))
    folder = models.ForeignKey(
        to=Folder, on_delete=models.CASCADE, verbose_name=_("folder")
    )

    class Meta:
        unique_together = ("content", "folder")
