from django.db import models


# Create your models here.
class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    url = models.URLField()
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Resume(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    skills = models.TextField()
    description = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.full_name
