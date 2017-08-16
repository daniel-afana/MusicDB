from musicapp.models import Band, Musician, Album, BandMember
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from musicapp.authentication import ExpiringTokenAuthentication
import pdb
from setup_user_groups import SetupGroups
from django.contrib.auth.models import User, Group


class TestCaseInit(APITestCase):

    def setUp(self):

        self.musician1 = Musician.objects.create(
            first_name='Федор',
            last_name='Чистяков'
        )

        self.band1 = Band.objects.create(name='Ноль')
        
        self.album1 = Album.objects.create(
            title='Песня о безответной любви к Родине',
            released=1991,
            band=self.band1
        )

        super().setUp()


class TestCaseWithUsers(APITestCase):

    def setUp(self):

        s = SetupGroups()
        s.setup_groups()

        eauth = ExpiringTokenAuthentication()

        self.admin1 = "admin1"
        self.adm_password = "adm1pass0000"
        self.admin1 = User.objects.create_user(self.admin1, is_superuser=False, is_staff=False)
        self.admin1.set_password(self.adm_password)
        self.admin1.save()
        self.admin1.groups = (Group.objects.get(name='admins'),)
        self.token_admin = Token.objects.get(user__username='admin1')

        self.editor1 = "editor1"
        self.ed_password = "ed1pass0000"
        self.editor1 = User.objects.create_user(self.editor1, is_superuser=False, is_staff=False)
        self.editor1.set_password(self.ed_password)
        self.editor1.save()
        self.editor1.groups = (Group.objects.get(name='editors'),)
        self.token_editor = Token.objects.get(user__username='editor1')

        self.manager1 = "manager1"
        self.ma_password = "ma1pass0000"
        self.manager1 = User.objects.create_user(self.manager1, is_superuser=False, is_staff=False)
        self.manager1.set_password(self.ma_password)
        self.manager1.save()
        self.manager1.groups = (Group.objects.get(name='managers'),)
        self.token_manager = Token.objects.get(user__username='manager1')

        super().setUp()


class GetAPIRoot(APITestCase):
    
    def test_can_access_api_root(self):
        response = self.client.get(reverse('api-root'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateMusicianList(TestCaseWithUsers):

    def setUp(self):

        super().setUp()

        self.musician_data = { 
            'first_name': 'Федор',
            'last_name': 'Чистяков'
            }

    def test_cannot_create_musician(self):

        'Unauthorized user does not have permission'

        self.response = self.client.post(
            reverse('musician-list'),
            self.musician_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_musician(self):

        'Editor does not have permission'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_editor.key)

        self.response = self.client.post(
            reverse('musician-list'),
            self.musician_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_create_musician(self):

        'Admin can create a musician'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        self.response = self.client.post(
            reverse('musician-list'),
            self.musician_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_can_create_musician(self):

        'Manager can create a musician'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_manager.key)

        self.response = self.client.post(
            reverse('musician-list'),
            self.musician_data,
            format="json")
        
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class CreateBandList(TestCaseWithUsers):

    def setUp(self):

        super().setUp()

        self.band_data = { 
            'name': 'Ноль',
            }

    def test_cannot_create_band(self):

        'Unauthorized user does not have permission'

        self.response = self.client.post(
            reverse('band-list'),
            self.band_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_band(self):

        'Editor does not have permission'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_editor.key)

        self.response = self.client.post(
            reverse('band-list'),
            self.band_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_create_band(self):

        'Admin can create a band'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        self.response = self.client.post(
            reverse('band-list'),
            self.band_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_can_create_band(self):

        'Manager can create a band'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_manager.key)

        self.response = self.client.post(
            reverse('band-list'),
            self.band_data,
            format="json")
        
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class CreateBandMemberList(TestCaseInit, TestCaseWithUsers):

    def setUp(self):

        super().setUp()

        self.band_member_data = { 
            'musician': '/musicians/{}/'.format(self.musician1.pk),
            'band': '/bands/{}/'.format(self.band1.pk),
            'joined': '1901-01-01'
            }

    def test_cannot_create_band_member(self):

        'Unauthorized user does not have permission'

        self.response = self.client.post(
            reverse('bandmember-list'),
            self.band_member_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_band_member(self):

        'Editor does not have permission'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_editor.key)

        self.response = self.client.post(
            reverse('bandmember-list'),
            self.band_member_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_create_band_member(self):

        'Admin can create a band member'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        self.response = self.client.post(
            reverse('bandmember-list'),
            self.band_member_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_can_create_band_member(self):

        'Manager can create a band member'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_manager.key)

        self.response = self.client.post(
            reverse('bandmember-list'),
            self.band_member_data,
            format="json")
        
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class CreateAlbumList(TestCaseInit, TestCaseWithUsers):

    def setUp(self):

        super().setUp()

        self.album_data = { 
            'title': 'Песня о безответной любви к Родине',
            'band': '/bands/{}/'.format(self.band1.pk),
            'released': 1991
            }

    def test_cannot_create_album(self):

        'Unauthorized user does not have permission'

        self.response = self.client.post(
            reverse('album-list'),
            self.album_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_album(self):

        'Manager does not have permission'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_manager.key)

        self.response = self.client.post(
            reverse('album-list'),
            self.album_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_create_album(self):

        'Admin can create an album'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        self.response = self.client.post(
            reverse('album-list'),
            self.album_data,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_can_create_band_member(self):

        'Editor can create an album'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_editor.key)

        self.response = self.client.post(
            reverse('album-list'),
            self.album_data,
            format="json")
        
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class GetMusicianList(TestCaseInit):

    def test_get_all_musicians(self):

        self.response = self.client.get(reverse('musician-list'))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


class GetBandList(TestCaseInit):

    def test_get_all_bands(self):

        self.response = self.client.get(reverse('band-list'))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


class GetAlbumList(TestCaseInit):

    def test_get_all_albums(self):

        self.response = self.client.get(reverse('album-list'))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


class GetMusicianDetail(TestCaseInit):

    def test_get_valid_musician(self):
        self.response = self.client.get(reverse('musician-detail', kwargs={'pk': self.musician1.pk}))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get_invalid_musician(self):
        self.response = self.client.get(
            reverse('musician-detail', kwargs={'pk': 30}))
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)


class GetBandDetail(TestCaseInit):

    def test_get_valid_band(self):
        self.response = self.client.get(reverse('band-detail', kwargs={'pk': self.band1.pk}))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get_invalid_band(self):
        self.response = self.client.get(
            reverse('band-detail', kwargs={'pk': 30}))
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)


class GetAlbumDetail(TestCaseInit):

    def test_get_valid_album(self):
        self.response = self.client.get(reverse('album-detail', kwargs={'pk': self.album1.pk}))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get_invalid_album(self):
        self.response = self.client.get(
            reverse('album-detail', kwargs={'pk': 30}))
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateMusician(TestCaseInit, TestCaseWithUsers):

    def setUp(self):

        super().setUp()

        self.musician_data = { 
            'first_name': 'Anthony',
            'last_name': 'Kiedis'
            }

        self.valid_info = { 
            'first_name': 'Федор',
            'last_name': 'Курочкин'
            }
        
        self.invalid_info = {
            'first_name': 1,
            'last_name': 'Курочкин'
        }

    def test_valid_update_musician(self):

        'Admin can update a musician'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        'Create a musician first'
        self.client.post(
            reverse('musician-list'),
            self.musician_data,
            format="json")

        self.new_musician = Musician.objects.get(first_name='Anthony')

        self.response = self.client.put(
            reverse('musician-detail', kwargs={'pk':self.new_musician.pk}),
            self.valid_info,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
    
    def test_invalid_update_musician(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        self.response = self.client.put(
            reverse('musician-detail', kwargs={'pk': self.new_musician.pk}),
            self.invalid_info,
            format="json")
        
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateBand(TestCaseInit, TestCaseWithUsers):

    def setUp(self):

        super().setUp()

        self.band_data = {'name': 'RHCP',}

        self.valid_info = {'name': 'Нуль',}
        
        self.invalid_info = {'name': 1}

    def test_valid_update_band(self):

        'Admin can update a band'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        'Create a band first'
        self.client.post(
            reverse('band-list'),
            self.band_data,
            format="json")

        self.new_band = Band.objects.get(name='RHCP')

        self.response = self.client.put(
            reverse('band-detail', kwargs={'pk':self.new_band.pk}),
            self.valid_info,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
    
    def test_invalid_update_band(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        self.response = self.client.put(
            reverse('band-detail', kwargs={'pk': self.new_band.pk}),
            self.invalid_info,
            format="json")
        
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateBandMember(TestCaseInit, TestCaseWithUsers):

    def setUp(self):

        super().setUp()

        self.band_member_data = { 
            'musician': '/musicians/{}/'.format(self.musician1.pk),
            'band': '/bands/{}/'.format(self.band1.pk),
            'joined': '1901-01-01'
            }

        self.valid_info = { 
            'musician': '/musicians/{}/'.format(self.musician1.pk),
            'band': '/bands/{}/'.format(self.band1.pk),
            'joined': '1901-01-02'
            }

        self.invalid_info = { 
            'musician': '/musicians/{}/'.format(self.musician1.pk),
            'band': '/bands/{}/'.format(self.band1.pk),
            'joined': '1901'
            }

    def test_valid_update_band_member(self):

        'Admin can update a band member'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        'Create a band member first'
        self.client.post(
            reverse('bandmember-list'),
            self.band_member_data,
            format="json")

        self.new_bandmember = BandMember.objects.get(musician=self.musician1)

        self.response = self.client.put(
            reverse('bandmember-detail', kwargs={'pk':self.new_bandmember.pk}),
            self.valid_info,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
    
    def test_invalid_update_band_member(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        self.response = self.client.put(
            reverse('bandmember-detail', kwargs={'pk': self.new_bandmember.pk}),
            self.invalid_info,
            format="json")
        
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateAlbum(TestCaseInit, TestCaseWithUsers):

    def setUp(self):

        super().setUp()

        self.album_data = { 
            'title': 'Песня о безответной любви к Родине',
            'band': '/bands/{}/'.format(self.band1.pk),
            'released': 1991
            }

        self.valid_info = { 
            'title': 'Updated title',
            'band': '/bands/{}/'.format(self.band1.pk),
            'released': 1991
            }
        
        self.invalid_info = { 
            'title': 'Updated title',
            'band': '/bands/{}/'.format(self.band1.pk),
            'released': 1800
            }

    def test_cannot_update_album(self):

        'Manager does not have permission'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_manager.key)

        'Create an album first'
        self.client.post(
            reverse('album-list'),
            self.album_data,
            format="json")
        
        self.new_album = Album.objects.get(title='Песня о безответной любви к Родине')

        self.response = self.client.put(
            reverse('album-detail', kwargs={'pk':self.new_album.pk}),
            self.valid_info,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_update_album(self):

        'Admin can update an album'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        'Create an album first'
        self.client.post(
            reverse('album-list'),
            self.album_data,
            format="json")
        
        self.new_album = Album.objects.get(title='Песня о безответной любви к Родине')

        self.response = self.client.put(
            reverse('album-detail', kwargs={'pk':self.new_album.pk}),
            self.valid_info,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
    
    def test_invalid_update_album(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)

        self.response = self.client.put(
            reverse('album-detail', kwargs={'pk': self.new_album.pk}),
            self.invalid_info,
            format="json")
        
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)