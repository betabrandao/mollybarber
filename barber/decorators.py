from django.shortcuts import redirect
from functools import wraps

def barber_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'barber'):
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view