from django.shortcuts import render


def index(request):

    context = {'request': request}
    return render(request, 'index.html', context)

def about(request):

    context = {'request': request}
    return render(request, 'about.html', context)
