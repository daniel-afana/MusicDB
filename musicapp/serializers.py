from rest_framework import serializers
from musicapp.models import Band, Musician, Album, BandMember


class BandMemberSerializer(serializers.HyperlinkedModelSerializer):

    musician = serializers.HyperlinkedRelatedField(view_name='musician-detail', 
        queryset=Musician.objects.all())
    band = serializers.HyperlinkedRelatedField(view_name='band-detail', 
        queryset=Band.objects.all())
    joined = serializers.DateField(required = False)

    class Meta:
        model = BandMember
        fields = ('url', 'musician', 'band', 'joined')


class MusicianField(serializers.RelatedField):

    def to_representation(self, value):
        return 'Joined: {} Musician: {}'.format(value.joined, value.musician)


class BandSerializer(serializers.HyperlinkedModelSerializer):

    band_musicians = MusicianField(many=True, read_only=True)

    founded = serializers.DateField(required=False)

    class Meta:
        model = Band
        fields = ('url', 'name', 'description', 'founded', 'band_musicians')


class BandField(serializers.RelatedField):

    def to_representation(self, value):
        return 'Joined: {} Band: {}'.format(value.joined, value.band)


class MusicianSerializer(serializers.HyperlinkedModelSerializer):

    band_member = BandField(many=True, read_only=True)

    class Meta:
        model = Musician
        fields = ('url', 'first_name', 'second_or_father_name', 'last_name', 'slug', 'band_member')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Album
        fields = ('url', 'title', 'released', 'band')


