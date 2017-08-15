from musicapp.models import Band, Musician, Album, BandMember
from rest_framework import viewsets
from musicapp.serializers import BandSerializer, MusicianSerializer, AlbumSerializer, BandMemberSerializer
from rest_framework.decorators import detail_route, list_route
import pdb 


class BandViewSet(viewsets.ModelViewSet):
    
    queryset = Band.objects.all()
    serializer_class = BandSerializer

    @detail_route()
    def musicians(self, request, pk=None):

        """
        Returns a list of all the musicians belonging to the band
        URL bands/pk/musicians/
        """
        band = Band.objects.get(pk=pk)
        band_members = band.band_musicians.all()
        musicians = [m.musician for m in band_members]
        page = self.paginate_queryset(musicians)
        if page is None:
            serializer = MusicianSerializer(
                objs, context={'request': request}, many=True
            )
            return Response(serializer.data)
        else:
            serializer = MusicianSerializer(
                page, context={'request': request}, many=True
            )
            return self.get_paginated_response(serializer.data)

    @detail_route()
    def albums(self, request, pk=None):

        """
        Returns a list of all the band's albums
        URL bands/pk/albums/
        """
        band = Band.objects.get(pk=pk)
        albums = band.album_set.all()
        page = self.paginate_queryset(albums)
        if page is None:
            serializer = AlbumSerializer(
                objs, context={'request': request}, many=True
            )
            return Response(serializer.data)
        else:
            serializer = AlbumSerializer(
                page, context={'request': request}, many=True
            )
            return self.get_paginated_response(serializer.data)


class MusicianViewSet(viewsets.ModelViewSet):
    
    queryset = Musician.objects.all()
    serializer_class = MusicianSerializer

    @list_route()
    def notInBand(self, request):

        """
        Musicians who are not in any band
        """
        musicians = Musician.objects.filter(band_member__isnull=True)
        page = self.paginate_queryset(musicians)
        if page is None:
            serializer = MusicianSerializer(
                objs, context={'request': request}, many=True
            )
            return Response(serializer.data)
        else:
            serializer = MusicianSerializer(
                page, context={'request': request}, many=True
            )
            return self.get_paginated_response(serializer.data)


class AlbumViewSet(viewsets.ModelViewSet):

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class BandMemberViewSet(viewsets.ModelViewSet):

    queryset = BandMember.objects.all()
    serializer_class = BandMemberSerializer