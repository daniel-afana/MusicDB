from rest_framework.permissions import DjangoObjectPermissions

class DjangoObjectPermissionsOrAnonReadOnly(DjangoObjectPermissions):
    pass
    # Read-only rights for all users
    authenticated_users_only = False
