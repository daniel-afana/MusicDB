from django.contrib import admin
from musicapp.models import Band, Musician, Album, BandMember


admin.site.register(Band)
admin.site.register(Musician)
admin.site.register(Album)
admin.site.register(BandMember)