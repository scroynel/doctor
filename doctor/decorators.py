from django.http import Http404

# If User is in group called "Doctor" then user has access to the page
def only_for_doctors(*groups):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists() or request.user.is_staff:
                return function(request, *args, **kwargs)
            raise Http404
        return wrapper
    return decorator