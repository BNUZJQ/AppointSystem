from django.http import HttpResponseRedirect
from django.utils.decorators import available_attrs
from django.utils.six import wraps


def login_required(view_func):
    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            return view_func(request)

        return HttpResponseRedirect('/')

    return _wrapped_view
