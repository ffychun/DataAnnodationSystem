from django.db import models

class TaggedLine(models.Model):
    line_number = models.IntegerField()
    tag = models.CharField(max_length=10)