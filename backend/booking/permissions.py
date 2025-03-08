from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsHostOrReadOnly(BasePermission):
    """
    Custom permission to allow hosts to manage their own objects
    * 1-has_permission : Determines whether user has permission to access the view itself (view level)
    * 2-has_object_permission :Determines whether user has permission to interact with a specific object (object level )
    when 1 return False 2 will not called 
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        # we can use return getattr(request.user.profile, 'role', None) == Role.HOST instead
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods (GET,HEAD,OPTIONS) for all users
        if request.method in SAFE_METHODS:
            return True

        # Check specific object types : Wishlist, PropertyAmenity, PropertyImage
        if hasattr(obj, 'related_property'):
            return obj.related_property.host == request.user

        # if obj have host attribute : Booking, Property
        if hasattr(obj, 'host'):
            return obj.host == request.user

        return False
