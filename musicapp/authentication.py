from datetime import timedelta
from datetime import datetime
import pytz
# from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.utils.timezone import utc
from rest_framework.exceptions import AuthenticationFailed
import pdb


class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):

        model = self.get_model()

        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
            
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - timedelta(minutes=5):
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)