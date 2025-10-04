from django.db import models

class Quote(models.Model):
    quote = models.CharField(max_length=200, default = "Enter quote...")
    author = models.CharField(max_length=200, default = "Enter author...")
    tag = models.ManyToManyField('Tag')
    def __str__(self):
        return f"{self.author}: {self.quote[:50]}"
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

