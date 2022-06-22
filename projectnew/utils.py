def show_toolbar(request):
    return request.META.get('HTTP_DEBUG', None) == 'DEBUG_HEADER'
