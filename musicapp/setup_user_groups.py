from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from musicapp.models import Band, Musician, Album


class SetupGroups():

    def setup_groups(self):
        admins, created = Group.objects.get_or_create(name='admins')
        admins.permissions.add(
            Permission.objects.get(codename='add_band'),
            Permission.objects.get(codename='add_musician'),
            Permission.objects.get(codename='add_album'),
            Permission.objects.get(codename='add_bandmember'),
            Permission.objects.get(codename='change_band'),
            Permission.objects.get(codename='change_musician'),
            Permission.objects.get(codename='change_album'),
            Permission.objects.get(codename='change_bandmember'),
            Permission.objects.get(codename='delete_band'),
            Permission.objects.get(codename='delete_musician'),
            Permission.objects.get(codename='delete_album'),
            Permission.objects.get(codename='delete_bandmember'),
        )
        admins.save()

        editors, created = Group.objects.get_or_create(name='editors')
        editors.permissions.add(Permission.objects.get(codename='add_album'),)
        editors.save()

        managers, created = Group.objects.get_or_create(name='managers')
        managers.permissions.add(
            Permission.objects.get(codename='add_band'),
            Permission.objects.get(codename='add_musician'),
            Permission.objects.get(codename='add_bandmember'),
        )
        managers.save()