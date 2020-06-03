from hashlib import md5
from django.db import models
from django.contrib.auth.models import User


class URL(models.Model):
    t_id = models.AutoField(primary_key=True)
    full_url = models.URLField(unique=True)
    url_hash = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.t_id:
            self.url_hash = md5(self.full_url.encode()).hexdigest()[:10]
        return super().save(*args, **kwargs)


class URLWithCredentials(models.Model):
    t_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    full_url = models.URLField()
    url_hash = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.t_id:
            self.url_hash = md5(self.full_url.encode()).hexdigest()[:10]
        return super().save(*args, **kwargs)

