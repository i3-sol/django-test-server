from django.db import models

class Notes(models.Model):
    title = models.CharField(max_length=60)
    content = models.CharField(max_length=160)

    def __str__(self):
        return self.title
    
    