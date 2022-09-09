from django.db import models


class Characters(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    # array of urls
    url = models.TextField()

    # image
    thumbnail = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
