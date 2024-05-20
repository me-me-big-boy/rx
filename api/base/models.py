from django.db import models


class BaseModel(models.Model):
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name
