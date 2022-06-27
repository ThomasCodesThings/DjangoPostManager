def getRequestMethod(request):
    return 'GET' if request.method == 'GET' else request.POST.get('_method', 'POST')

