from django.shortcuts import render


def home_view(request):
    return render(request, 'home-masonry.html')


def page_not_found_view(request):
    return render(request, 'page-404.html')


def contact_view(request):
    return render(request, 'page-contact.html')


def about_view(request):
    return render(request, 'page-about.html')


def post_view(request):
    return render(request, 'post-image.html')
