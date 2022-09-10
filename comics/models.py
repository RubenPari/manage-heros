from django.db import models


class Comic(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    isbn = models.CharField(max_length=13)
    ean = models.CharField(max_length=13)
    format = models.CharField(max_length=255)
    pageCount = models.IntegerField()
    resourceURI = models.TextField()
    # array of urls
    urls = models.TextField()
    thumbnail = models.TextField()

    def __str__(self):
        return self.title
