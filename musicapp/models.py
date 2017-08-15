from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Automatically generate a token whenever a new user is created
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Band(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    founded = models.DateField(blank=True, null=True)
    musicians = models.ManyToManyField("Musician", through="BandMember")

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Musician(models.Model):
    
    first_name = models.CharField(max_length=50)
    second_or_father_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=205, blank=True)

    class Meta:
        ordering = ('last_name',)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.slug = self.first_name + ' ' + self.last_name
        super(Musician, self).save(*args, **kwargs)


class Album(models.Model):

    title = models.CharField(max_length=500)
    released = models.DateField()
    band = models.ForeignKey(Band, on_delete=models.CASCADE)

    class Meta:
        ordering = ('released',)

    def __str__(self):
        return self.title


class BandMember(models.Model):

    musician = models.ForeignKey(Musician, on_delete=models.CASCADE, related_name = 'band_member')
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name = 'band_musicians')
    joined = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('musician', 'band')
