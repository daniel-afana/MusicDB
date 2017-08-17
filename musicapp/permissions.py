from rest_framework.permissions import DjangoModelPermissions

class DjangoModelPermissionsOrAnonReadOnly(DjangoModelPermissions):
    pass
    # Read-only rights for all users
    authenticated_users_only = False
